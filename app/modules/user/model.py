# app/modules/user/model.py
import email
from sqlalchemy import Column, Integer, String
from app.main import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True, nullable=False, unique=True)
    username = Column(String(50), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
