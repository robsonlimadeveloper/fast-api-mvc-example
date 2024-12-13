from fastapi import APIRouter, Depends, HTTPException
from app.modules.user.service import UserService
from app.modules.user.repository import UserRepository
from app.modules.user.dto import UserCreateDTO, UserResponseDTO
from app.config import SessionLocal
from app.modules.user.dto import UserCreateDTO, UserResponseDTO
from typing import List
from app.modules.auth.service import AuthService
from app.modules.user.model import User
from app.main import oauth2_scheme

user_service = UserService(UserRepository())
router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register", response_model=UserResponseDTO)
def register(user_dto: UserCreateDTO, token: str = Depends(oauth2_scheme)):
    try:
        return user_service.register(user_dto.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{user_id}", response_model=UserResponseDTO)
async def get_user_by_id(user_id: int, token: str = Depends(oauth2_scheme)):
    user = user_service.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/", response_model=List[UserResponseDTO])
async def get_all_users(token: str = Depends(oauth2_scheme)):
    return user_service.get_all()
