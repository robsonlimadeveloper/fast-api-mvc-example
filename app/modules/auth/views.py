"""Auth views."""
from fastapi import APIRouter, Depends, HTTPException, status
from app.modules.auth.service import AuthService
from app.modules.auth.dto import AuthDTOResponse
from app.modules.auth.exceptions import AuthenticationException
from app.modules.user.repository import UserRepository
from fastapi.security import OAuth2PasswordRequestForm
from typing_extensions import Annotated

router = APIRouter(prefix="/auth", tags=["Auth"])

auth_service = AuthService(UserRepository())

@router.post(
        path="/token",
        response_model=AuthDTOResponse,
        status_code=status.HTTP_200_OK,
        description="Authenticate a user and return a token.",
        tags=["Auth"])
async def token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> AuthDTOResponse: 
    """Authenticate a user and return a token."""
    return AuthDTOResponse.model_validate(auth_service.authenticate(form_data.username, form_data.password))
    
    