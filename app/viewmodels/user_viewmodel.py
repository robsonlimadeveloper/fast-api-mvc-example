from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository

class UserViewModel:
    def __init__(self, db: Session):
        self.db = db

    def register_user(self, username: str, password: str):
        if UserRepository.get_user_by_username(self.db, username):
            return None, "Username already registered"
        user = UserRepository.create_user(self.db, username, password)
        return user, None