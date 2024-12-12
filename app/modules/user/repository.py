"""User repository."""
from injector import inject
from sqlalchemy.orm import Session
from app.core.repository_abstract import RepositoryAbstract
from .model import User
from app import db

class UserRepository(RepositoryAbstract):
    """Class to manage user data."""

    @inject
    def __init__(self):
        super(UserRepository, self).__init__(User)

    def find_by_username_and_password(self, username: str, password: str) -> User:
        """Return user by username and password."""
        return (
            db.query(User)
            .filter(User.username == username)
            .filter(User.password == password)
            .first()
        )

    def find_by_username(self, username: str) -> User:
        """Return User by username."""
        return db.query(User).filter(User.username == username).first()
