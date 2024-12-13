# app/models/user.py
# app/modules/user/model.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from app.main import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True, nullable=False, unique=True)
    username = Column(String(50), nullable=False)
    password = Column(String(255), nullable=False)
