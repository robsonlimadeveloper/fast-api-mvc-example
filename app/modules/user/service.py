from injector import inject
from app.core.service_abstract import ServiceAbstract
from app.models import user
from app.modules.user.repository import UserRepository
from app.modules.user.dto import UserCreateDTO, UserResponseDTO
from sqlalchemy.orm import Session
from typing import List, Optional

class UserService(ServiceAbstract):
    @inject
    def __init__(self, repository: UserRepository):
        super(UserService, self).__init__(repository)
        self.repository = repository

    def get_by_id(self, id: int) -> Optional[UserResponseDTO]:
        return self.repository.find_by_id(id)

    def get_all(self, skip: int = 0, limit: int = 10) -> List[UserResponseDTO]:
        return self.repository.find_all()

    def register(self, dto: UserCreateDTO) -> Optional[UserResponseDTO]:
        if self.repository.find_by_username(dto.username):
            raise ValueError("Username already registered")
        # hashed_password = get_password_hash(user_dto.password)
        return self.repository.save(dto)
        

    def update(self, id: int, dto: UserResponseDTO) -> Optional[UserResponseDTO]:
        user = self.repository.find_by_id(id)


    def delete(self, id: int) -> bool:
        return self.repository.delete(id)
