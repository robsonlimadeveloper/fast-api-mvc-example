from pydantic import BaseModel
from typing import Optional

class UserCreateDTO(BaseModel):
    username: str
    password: str

class UserResponseDTO(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True
