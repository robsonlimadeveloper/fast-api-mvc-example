from datetime import datetime, timedelta
from typing import Dict
import jwt
from app.modules.user.model import User
from app.modules.auth.exceptions import AuthenticationException
from app.config import settings, pwd_settings
from fastapi import HTTPException, status
from jwt import DecodeError, decode, encode
from app.modules.auth.dto import TokenData
from app.modules.auth.exceptions import AuthenticationException
from app.modules.user.repository import UserRepository
from app.modules.auth.google import oauth
from starlette.requests import Request
from starlette.datastructures import URL
from app.core.logging import logger
import uuid

class AuthService:
    """Auth service class."""

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    def hash_password(self, password: str) -> str:
        """Hash a password."""
        return pwd_settings.pwd_context.hash(password)

    def token_encode(self, user: User) -> str:
        """Generate a JWT token for a user."""
        payload = {
            "sub": user.id,
            "user_id": user.id,
            "exp": datetime.utcnow() + timedelta(days=1),
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return token

    def authenticate(self, username: str, password: str) -> dict:
        """Authenticate a user and return a token."""
        
        user: User = self.user_repository.find_by_username(username)
        
        if not user or not pwd_settings.pwd_context.verify(password, str(user.password)):
            raise AuthenticationException()

        token = self.token_encode(user)
        return {"access_token": token, "token_type": "Bearer"}

    def get_current_user_by_token(self, 
        token: str 
    ):
        """Get current user by token."""
        
        try:
            payload = decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            user_id: str = payload.get('user_id')

            if not user_id:
                raise AuthenticationException()

            token_data = TokenData(user_id=int(user_id))
            user = self.user_repository.find_by_id(token_data.user_id)
            
            if not user:
                raise AuthenticationException()

        except DecodeError as e:
            logger.error(f"Error decoding token: {e}")
            raise AuthenticationException()
        except Exception as e:
            logger.error(f"Error getting current user by token: {e}")
            raise AuthenticationException()

        return user

    async def google_authorize_access_token(self, request: Request):
        """Google authorize access token."""
        try:
            token = await oauth.google.authorize_access_token(request)
            user_info = token.get('userinfo')

            user = self.user_repository.find_by_email(user_info['email'])

            if not user:

                #create username by name and uuid
                username = user_info['name'].replace(" ", "_")
                username = f"{username}_{str(uuid.uuid4())[:8]}"

                user = User(
                    username=user_info['name'],
                    email=user_info['email'],
                    password=self.hash_password(user_info['sub']),
                )
                user = self.user_repository.save(user)
                logger.info(f"New user created: {user.username}")

            token = self.token_encode(user)

            return {"access_token": token, "token_type": "Bearer"}

        except Exception as e:
            logger.error(f"Error authorizing access token: {e}")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
    async def google_authorize_redirect(self, request: Request, redirect_uri: URL):
        """Google authorize redirect."""
        try:
            return await oauth.google.authorize_redirect(request, redirect_uri)
        except Exception as e:
            logger.error(f"Error authorizing redirect: {e}")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        
