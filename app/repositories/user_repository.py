from sqlalchemy.orm import Session
from app.models.user import User
from app.config import pwd_settings


class UserRepository:
    @staticmethod
    def get_user_by_id(user_id: int):
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_all_users(skip: int = 0, limit: int = 10):
        return db.query(User).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_user_by_username(db: Session, username: str):
        return db.query(User).filter(User.username == username).first()
