from app.database import SessionLocal
from app.repositories.user_repository import UserRepository
from app.security.auth import get_password_hash
from app.config import pwd_settings

def create_admin_user():
    db = SessionLocal()
    if not UserRepository.get_user_by_username(db, "admin"):
        UserRepository.create_user(db, "admin", "1234")
    db.close()