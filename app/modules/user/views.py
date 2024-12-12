from fastapi import APIRouter, Depends, HTTPException
from app.modules.user.service import UserService
from app.modules.user.repository import UserRepository
from app.modules.user.dto import UserCreateDTO, UserResponseDTO
from app.database import SessionLocal
from app.modules.user.dto import UserCreateDTO, UserResponseDTO


user_service = UserService(UserRepository())
router = APIRouter()

@router.post("/register", response_model=UserResponseDTO)
def register(user_dto: UserCreateDTO):
    try:
        return user_service.register(user_dto)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/users/{user_id}", response_model=UserResponseDTO)
def get_user_by_id(user_id: int):
    user = user_service.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
