from fastapi import APIRouter, Depends
from app.modules.user.service import UserService
from app.modules.user.repository import UserRepository
from app.config import SessionLocal
from app.modules.user.dto import UserCreateDTO, UserResponseDTO, UserUpdateDTO
from typing import List
from fastapi_pagination import Page, paginate, add_pagination
from fastapi import status
from app.main import security

user_service = UserService(UserRepository())
router = APIRouter(prefix="/v1/api/users", tags=["Users"])

@router.post(
        path="/",
        response_model=UserResponseDTO,
        status_code=status.HTTP_201_CREATED,
        description="Register a new user.",
        tags=["Users"],
        dependencies=[Depends(security)])
def add_user(user_dto: UserCreateDTO):
    """Register user."""
    return UserResponseDTO.model_validate(user_service.register(user_dto.model_dump()))

@router.get(path="/{user_id}",
            response_model=UserResponseDTO,
            status_code=status.HTTP_200_OK,
            description="Get user by id.",
            tags=["Users"],
            dependencies=[Depends(security)])
async def get_user_by_id(user_id: int):
    """Get user by id."""
    return UserResponseDTO.model_validate(user_service.get_by_id(user_id))
    
@router.get(path="/",
            response_model=Page[UserResponseDTO],
            status_code=status.HTTP_200_OK,
            description="Get all users with pagination.",
            tags=["Users"],
            dependencies=[Depends(security)])
def get_all_users():
    """Get all users."""
    users = user_service.get_all()
    return paginate(users)

@router.put(path="/{user_id}",
            response_model=UserResponseDTO,
            status_code=status.HTTP_200_OK,
            description="Update user by id.",
            tags=["Users"],
            dependencies=[Depends(security)])
async def update_user_by_id(user_id: int, user_dto: UserUpdateDTO):
    """Update user by id."""
    user = user_service.get_by_id(user_id)
    return UserResponseDTO.model_validate(user_service.update(user_id, user_dto.model_dump()))

@router.delete(
        path="/{user_id}",
        response_model=UserResponseDTO,
        status_code=status.HTTP_200_OK,
        description="Delete user by id.",
        tags=["Users"],
        dependencies=[Depends(security)])
async def delete_user_by_id(user_id: int):
    """Delete user by id."""
    return UserResponseDTO.model_validate(user_service.delete(user_id))
