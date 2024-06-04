from datetime import datetime
from typing import List

from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from sqlmodel import Field, Relationship, SQLModel, create_engine


class Loan(SQLModel, table=True):
    id: int = Field(
        sa_column=Column("id", Integer, primary_key=True, autoincrement=True)
    )
    customer_id: str = Field(foreign_key="customer.id")
    book_id: str = Field(foreign_key="book.id")

    created_by_id: str = Field(foreign_key="user.id")
    created_at: datetime

    book: "Book" = Relationship(back_populates="loans")
    customer: "Loan" = Relationship(back_populates="loans")
    created_by: "User" = Relationship(back_populates="loans")


class Role(SQLModel, table=True):
    id: str = Field(primary_key=True)
    description: str | None = None

    users: List["User"] = Relationship(back_populates="role")


class User(SQLModel, table=True):
    id: str = Field(primary_key=True)
    first_name: str
    last_name: str
    email: str = Field(sa_column=Column("email", String, unique=True))
    hashed_password: str
    role_id: str = Field(foreign_key="role.id")
    disabled: bool = False
    creation_at: datetime = datetime.now()
    bio: str | None = None
    age: int | None = None

    books: list["Book"] = Relationship(back_populates="created_by")
    customers: list["Customer"] = Relationship(back_populates="created_by")
    loans: list["Loan"] = Relationship(back_populates="created_by")
    role: Role = Relationship(back_populates="users")


class Customer(SQLModel, table=True):
    id: str = Field(
        sa_column=Column("id", Integer, primary_key=True, autoincrement=True)
    )
    first_name: str
    last_name: str
    email: str = Field(sa_column=Column("email", String, unique=True))

    created_by_id: str = Field(foreign_key="user.id")
    created_at: datetime = datetime.now()

    books: list["Book"] = Relationship(
        back_populates="customers", link_model=Loan
    )
    loans: list["Loan"] = Relationship(back_populates="customer")
    created_by: User = Relationship(back_populates="customers")


class Book(SQLModel, table=True):
    id: str = Field(
        sa_column=Column("id", Integer, primary_key=True, autoincrement=True)
    )
    title: str
    author: str
    publisher: str
    publication_date: datetime

    created_by_id: str = Field(foreign_key="user.id")
    created_at: datetime = datetime.now()

    customers: List[Customer] = Relationship(
        back_populates="books", link_model=Loan
    )
    loans: List[Loan] = Relationship(back_populates="book")
    created_by: User = Relationship(back_populates="books")


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


sqlite_file_name = "yalb.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

SQLModel.metadata.create_all(engine)
