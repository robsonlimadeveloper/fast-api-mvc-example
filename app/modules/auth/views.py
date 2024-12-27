"""Auth views."""
from fastapi import APIRouter, Depends, status, Request
from app.modules.auth.service import AuthService
from app.modules.auth.dto import AuthDTOResponse
from app.modules.user.repository import UserRepository
from fastapi.security import OAuth2PasswordRequestForm
from typing_extensions import Annotated
from app.modules.auth.google import oauth

router = APIRouter(prefix="/v1/api/auth", tags=["Auth"])

auth_service = AuthService(UserRepository())

@router.post(
        path="/token",
        response_model=AuthDTOResponse,
        status_code=status.HTTP_200_OK,
        description="Authenticate a user and return a token.",
        tags=["Auth"])
async def create_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> AuthDTOResponse: 
    """Authenticate a user and return a token."""
    return AuthDTOResponse.model_validate(auth_service.authenticate(form_data.username, form_data.password))

@router.get("/google/login")
async def google_login(request: Request):
    """Google login."""
    redirect_uri = request.url_for("google_callback")
    return await auth_service.google_authorize_redirect(request, redirect_uri)

@router.get("/google/callback")
async def google_callback(request: Request):
    """Google callback."""
    return AuthDTOResponse.model_validate(await auth_service.google_authorize_access_token(request))