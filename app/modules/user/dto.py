from pydantic import BaseModel, Field
from typing import Optional

class UserCreateDTO(BaseModel):
    username: str = Field(min_length=5, max_length=50)
    password: str = Field(min_length=6, max_length=10)
    email: str = Field(min_length=5, max_length=255)

class UserResponseDTO(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True

class UserUpdateDTO(BaseModel):
    username: str = Field(min_length=5, max_length=50)
    password: Optional[str]
    email: str = Field(min_length=5, max_length=255)

