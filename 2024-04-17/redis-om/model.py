from datetime import datetime
from typing import Optional

from database import BaseModel
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy_utils import ArrowType, EmailType


class User(BaseModel):
    __tablename__ = "User"

    username = Column(String, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(EmailType, unique=True, index=True)
    join_datetime = Column(ArrowType)
    is_active = Column(Boolean, default=False)
    bio = Column(String, nullable=True)
    age = Column(Integer, nullable=True)


class Room(BaseModel):
    __tablename__ = "room"

    name = Column(String, primary_key=True)
    max_user = Column(Integer, nullable=True)


class Message(BaseModel):
    __tablename__ = "message"

    timestamp = Column(ArrowType)
    content = Column(String)
