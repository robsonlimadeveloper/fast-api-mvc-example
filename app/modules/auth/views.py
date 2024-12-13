import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.modules.auth.service import AuthService
from app.modules.auth.dto import AuthDTORequest, AuthDTOResponse
from app.modules.auth.exceptions import AuthenticationException
from app.modules.user.service import UserService
from app.modules.user.repository import UserRepository
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing_extensions import Annotated

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Auth"])

auth_service = AuthService(UserService(UserRepository()))

@router.post("/token", response_model=AuthDTOResponse, status_code=status.HTTP_200_OK)
async def token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    """Authenticate a user and return a token."""
    try:
        return auth_service.authenticate(form_data.username, form_data.password)
    except AuthenticationException as e:
        logger.error("Erro de autenticação: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e)
        )
    