from datetime import datetime
from typing import List

from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from sqlmodel import Field, Relationship, SQLModel, create_engine


class UserRoom(SQLModel, table=True):
    user_id: str = Field(foreign_key="user.id", primary_key=True)
    room_id: str = Field(foreign_key="room.id", primary_key=True)
    join_at: datetime


class Role(SQLModel, table=True):
    id: str = Field(primary_key=True)
    description: str | None = None

    users: List["User"] = Relationship(back_populates="role")


class User(SQLModel, table=True):
    id: str = Field(primary_key=True)
    first_name: str
    last_name: str
    email: str = Field(sa_column=Column("email", String, unique=True))
    password: str
    role_id: str = Field(foreign_key="role.id")
    disabled: bool = False
    creation_at: datetime = datetime.now()
    bio: str | None = None
    age: int | None = None

    role: Role = Relationship(back_populates="users")
    rooms: list["Room"] = Relationship(
        back_populates="users", link_model=UserRoom
    )
    messages: list["Message"] = Relationship(back_populates="user")


class Room(SQLModel, table=True):
    id: str = Field(primary_key=True)
    max_user: int | None = None
    creation_at: datetime = datetime.now()

    users: List[User] = Relationship(
        back_populates="rooms", link_model=UserRoom
    )
    messages: List["Message"] = Relationship(back_populates="room")


class Message(SQLModel, table=True):
    id: int = Field(
        sa_column=Column("id", Integer, primary_key=True, autoincrement=True)
    )
    user_id: str = Field(foreign_key="user.id")
    room_id: str = Field(foreign_key="room.id")
    sent_at: datetime
    content: str

    user: User = Relationship(back_populates="messages")
    room: Room = Relationship(back_populates="messages")


class Result[Type: SQLModel](BaseModel):
    success: bool
    detail: str
    timestamp: datetime
    data: Type

    def __init__(
        self: "Result[Type]",
        detail: str,
        data: str,
        success: bool = True,
    ) -> "Result[Type]":
        super().__init__(
            success=success, detail=detail, timestamp=datetime.now(), data=data
        )


class Token[Type: SQLModel](BaseModel):
    access_token: str | None = None
    refresh_token: str | None = None


sqlite_file_name = "yacr.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

SQLModel.metadata.create_all(engine)
