from pydantic import BaseModel
from typing import Optional

class UserCreateDTO(BaseModel):
    username: str
    password: str

class UserResponseDTO(BaseModel):
    id: int
    username: str

    class ConfigDict:
        from_attributes = True

class UserUpdateDTO(BaseModel):
    username: Optional[str]
    password: Optional[str]

