from datetime import datetime, timedelta
from typing import Dict
import jwt
from sqlalchemy.orm import Session
from app.modules.user.model import User
from .dto import AuthDTOResponse
from app.modules.auth.exceptions import AuthenticationException
from app.config import settings, pwd_settings
from http import HTTPStatus
from app.config import get_db
from fastapi import Depends, HTTPException
from jwt import DecodeError, decode, encode
from app.modules.auth.dto import AuthDTOResponse, TokenData
from app.modules.auth.exceptions import AuthenticationException
from app.modules.user.repository import UserRepository
from app.main import oauth2_scheme

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
            "username": user.username,
            "exp": datetime.utcnow() + timedelta(days=1),
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return token

    def authenticate(self, username: str, password: str) -> AuthDTOResponse:
        """Authenticate a user and return a token."""
        
        user: User = self.user_repository.find_by_username(username)
        
        if not user or not pwd_settings.pwd_context.verify(password, str(user.password)):
            raise AuthenticationException()

        token = self.token_encode(user)
        return AuthDTOResponse(access_token=token, token_type="Bearer")

    def get_current_user(self, 
        token: str = Depends(oauth2_scheme), 
    ):
        
        try:
            payload = decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            username: str = payload.get('username')

            if not username:
                raise AuthenticationException()

            token_data = TokenData(username=username)
            user = self.user_repository.find_by_username(token_data.username)
            
            if not user:
                raise AuthenticationException()

        # except DecodeError:
        #     raise AuthenticationException()
        except Exception as e:
            raise AuthenticationException()

        return user
