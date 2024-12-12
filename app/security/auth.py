from datetime import datetime, timedelta
import jwt
from app.config import settings, pwd_settings


def create_access_token(data: dict):
    print("create token")
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def verify_password(plain_password, hashed_password):
    return pwd_settings.Config.pwd_context.verify(plain_password, hashed_password, scheme="bcrypt")


def get_password_hash(password):
    return pwd_settings.Config.pwd_context.hash(password, scheme="bcrypt", rounds=10)