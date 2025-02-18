from fastapi import Depends
from app.config import session
from app.core.repository_abstract import RepositoryAbstract
from .model import User


class UserRepository(RepositoryAbstract):
    """Class to manage user data."""
    
    def __init__(self):
        super(UserRepository, self).__init__(User)
        self.session = session

    def find_by_username(self, username: str) -> User:
        """Return User by username."""
        return self.session.query(User).filter(User.username == username).first()
    
    def find_by_email(self, email: str) -> User:
        """Return User by email."""
        return self.session.query(User).filter(User.email == email).first()
