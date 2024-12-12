from pydantic_settings import BaseSettings
from passlib.context import CryptContext

#load environment variables
class Settings(BaseSettings):
    DATABASE_URL: str = ""
    SECRET_KEY: str = "supersecretkey"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

class PwdSettings(BaseSettings):
    
    class Config:
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

settings = Settings()
pwd_settings = PwdSettings()