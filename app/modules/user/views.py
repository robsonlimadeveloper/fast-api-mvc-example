from fastapi import APIRouter, Depends, HTTPException
from app.modules.user.service import UserService
from app.modules.user.repository import UserRepository
from app.modules.user.exceptions import NameDuplicateException
from app.config import SessionLocal
from app.modules.user.dto import UserCreateDTO, UserResponseDTO, UserUpdateDTO
from typing import List
from app.main import oauth2_scheme
from fastapi_pagination import Page, paginate, add_pagination
from fastapi import status

user_service = UserService(UserRepository())
router = APIRouter(prefix="/users", tags=["Users"])

@router.post(
        path="/register",
        response_model=UserResponseDTO,
        status_code=status.HTTP_201_CREATED,
        description="Register a new user.",
        tags=["Users"])
def register(user_dto: UserCreateDTO, token: str = Depends(oauth2_scheme)):
    """Register user."""
    return user_service.register(user_dto.model_dump())

@router.get(path="/{user_id}",
            response_model=UserResponseDTO,
            status_code=status.HTTP_200_OK,
            description="Get user by id.",
            tags=["Users"])
async def get_user_by_id(user_id: int, token: str = Depends(oauth2_scheme)):
    """Get user by id."""
    return user_service.get_by_id(user_id)
    
@router.get(path="/users/",
            response_model=Page[UserResponseDTO],
            status_code=status.HTTP_200_OK,
            description="Get all users with pagination.",
            tags=["Users"])
def get_users():
    """Get all users."""
    users = user_service.get_all()
    return paginate(users)

@router.put(path="/{user_id}",
            response_model=UserResponseDTO,
            status_code=status.HTTP_200_OK,
            description="Update user by id.",
            tags=["Users"])
async def update_user(user_id: int, user_dto: UserUpdateDTO, token: str = Depends(oauth2_scheme)):
    """Update user by id."""
    user = user_service.get_by_id(user_id)
    return user_service.update(user_id, user_dto.model_dump())

@router.delete(
        path="/{user_id}",
        response_model=UserResponseDTO,
        status_code=status.HTTP_200_OK,
        description="Delete user by id.",
        tags=["Users"])
async def delete_user(user_id: int, token: str = Depends(oauth2_scheme)):
    """Delete user by id."""
    return user_service.delete(user_id, token)
