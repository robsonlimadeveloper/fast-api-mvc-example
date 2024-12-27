
from app.core.service_abstract import ServiceAbstract
from app.modules.user.exceptions import NameDuplicateException, UserNotFoundException, UserNotDeleteYourselfException
from app.modules.user.model import User
from app.modules.user.repository import UserRepository
from app.modules.user.dto import UserResponseDTO
from app.modules.auth.service import AuthService
from typing import List
from app.config import pwd_settings

class UserService(ServiceAbstract):
    def __init__(self, repository: UserRepository):
        super(UserService, self).__init__(repository)
        self.repository = repository

    def __verify_user_exists(self, id: int) -> User:
        user = self.repository.find_by_id(id)

        if not user:
            raise UserNotFoundException()

        return user

    def get_by_id(self, id: int) -> User:
        """Get user by id.

        Args:
            id (int): User ID to search.

        Raises:
            UserNotFoundException: If user not found.

        Returns:
            Optional[UserResponseDTO]: User data.
        """
        return self.__verify_user_exists(id)

    def get_all(self, skip: int = 0, limit: int = 10) -> List[UserResponseDTO]:
        """Get all users with pagination.

        Args:
            skip (int, optional): Number of records to skip. Defaults to 0.
            limit (int, optional): Maximum number of records to return. Defaults to 10.

        Returns:
            List[UserResponseDTO]: List of user response DTOs.
        """
        return self.repository.find_all()
    
    def get_user_by_username(self, username: str) -> User:
        
        """Get user by username.

        Args:
            username (str): Username to search.

        Raises:
            UserNotFoundException: If user not found.

        Returns:
            Optional[User]: User data.
        """
        user = self.repository.find_by_username(username)

        if not user:
            raise UserNotFoundException()

        return user

    def register(self, dto: dict) -> User:
        """Register user.

        Args:
            dto (dict): User data to register.

        Raises:
            NameDuplicateException: If username already exists.

        Returns:
            Optional[UserResponseDTO]: Registered user.
        """

        if self.repository.find_by_username(dto["username"]):
            raise NameDuplicateException()

        dto["password"] = pwd_settings.pwd_context.hash(dto["password"])

        return self.repository.save(User(**dto))

    def update(self, id: int, dto: dict) -> User:
        """Update user.

        Args:
            id (int): User ID to update.
            dto (dict): User data to update.

        Raises:
            UserNotFoundException: If user not found.

        Returns:
            Optional[UserResponseDTO]: Updated user.
        """
        user = self.__verify_user_exists(id)

        dto["password"] = pwd_settings.pwd_context.hash(dto["password"])
        user = self.repository.update(id, dto)
        return user

    def __verify_id_user_logged(self, id: int, token: str):
        auth_service = AuthService(self.repository)
        current_user: User = auth_service.get_current_user_by_token(token=token)
        
        if current_user.__dict__["id"] == id:
            raise UserNotDeleteYourselfException()

    def delete(self, id: int, token: str) -> User:
        """Delete user by id.

        Args:
            id (int): User ID to delete.

        Returns:
            bool: True if deleted, False otherwise.
        """

        # self.__verify_id_user_logged(id, token)

        user: User = self.__verify_user_exists(id)

        if not user:
            raise UserNotFoundException()
        
        return self.repository.delete(user)

    
