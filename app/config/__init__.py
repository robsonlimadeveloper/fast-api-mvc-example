from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from pydantic_settings import BaseSettings, SettingsConfigDict
from passlib.context import CryptContext

# Load environment variables
class Settings(BaseSettings):
    DATABASE_URL: str = ""
    SECRET_KEY: str = "supersecretkey"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

class PwdSettings:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    return SessionLocal()

# Initialize settings and database components
settings = Settings()
pwd_settings = PwdSettings()

# Database setup
engine = create_engine(settings.DATABASE_URL)  # Use echo=True for debugging
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
session = get_db()
