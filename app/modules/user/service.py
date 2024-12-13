
from app.core.service_abstract import ServiceAbstract
from app.modules.user.model import User
from app.modules.user.repository import UserRepository
from app.modules.user.dto import UserCreateDTO, UserResponseDTO, UserUpdateDTO
from typing import List, Optional
from app.config import pwd_settings

class UserService(ServiceAbstract):
    def __init__(self, repository: UserRepository):
        super(UserService, self).__init__(repository)
        self.repository = repository

    def get_by_id(self, id: int) -> Optional[UserResponseDTO]:
        return self.repository.find_by_id(id)

    def get_all(self, skip: int = 0, limit: int = 10) -> List[UserResponseDTO]:
        return self.repository.find_all()
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        return self.repository.find_by_username(username)

    def register(self, dto: dict) -> Optional[UserResponseDTO]:
        if self.get_user_by_username(dto["username"]):
            raise ValueError("Username already registered")
        dto["password"] = pwd_settings.pwd_context.hash(dto["password"])
        return self.repository.save(User(**dto))

    def update(self, id: int, dto: dict) -> Optional[UserResponseDTO]:
        user = self.repository.find_by_id(id)
        if not user:
            raise ValueError("User not found")
        return self.repository.update(id, User(**dto))

    def delete(self, id: int) -> bool:
        return self.repository.delete(id)
