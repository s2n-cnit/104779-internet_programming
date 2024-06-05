from datetime import datetime
from typing import ClassVar, List, Optional, Tuple

from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from sqlmodel import Field, Relationship, SQLModel, create_engine
from utils import require


class Loan(SQLModel, table=True):
    id: int = Field(
        sa_column=Column("id", Integer, primary_key=True, autoincrement=True)
    )
    customer_id: str = Field(foreign_key="customer.id")
    book_id: str = Field(foreign_key="book.id")

    created_by_id: str = Field(foreign_key="user.id")
    created_at: Optional[datetime] = Field(default_factory=datetime.now)

    updated_by_id: str = Field(foreign_key="user.id")
    updated_at: Optional[datetime] = Field(
        default_factory=datetime.now,
        sa_column_kwargs={"onupdate": datetime.now},
    )

    book: "Book" = Relationship(back_populates="loans")
    # customer: "Loan" = Relationship(back_populates="loans")
    created_by: "User" = Relationship(back_populates="loans")

    create_fields: ClassVar[Tuple] = ("customer_id", "book_id")
    update_fields: ClassVar[Tuple] = ()
    public_fields: ClassVar[Tuple] = (
        "id",
        "customer_id",
        "book_id",
        "created_at",
        "updated_at",
    )


class Role(SQLModel, table=True):
    id: str = Field(primary_key=True)
    description: str | None = None

    created_by_id: str = Field(foreign_key="user.id")
    created_at: Optional[datetime] = Field(default_factory=datetime.now)

    updated_by_id: str = Field(foreign_key="user.id")
    updated_at: Optional[datetime] = Field(
        default_factory=datetime.now,
        sa_column_kwargs={"onupdate": datetime.now},
    )

    users: List["User"] = Relationship(back_populates="role")

    create_fields: ClassVar[Tuple] = ("id", "description")
    update_fields: ClassVar[Tuple] = ("id", "description")
    public_fields: ClassVar[Tuple] = (
        "id",
        "description",
        "created_by_id",
        "created_at",
        "updated_by_id",
        "updated_at",
    )


class User(SQLModel, table=True):
    id: str = Field(primary_key=True)
    first_name: str
    last_name: str
    email: str = Field(sa_column=Column("email", String, unique=True))
    password: str
    role_id: str = Field(foreign_key="role.id")
    disabled: bool = False
    bio: str | None = None
    age: int | None = None

    created_by_id: str = Field(foreign_key="user.id")
    created_at: Optional[datetime] = Field(default_factory=datetime.now)

    updated_by_id: str = Field(foreign_key="user.id")
    updated_at: Optional[datetime] = Field(
        default_factory=datetime.now,
        sa_column_kwargs={"onupdate": datetime.now},
    )

    books: list["Book"] = Relationship(back_populates="created_by")
    customers: list["Customer"] = Relationship(back_populates="created_by")
    loans: list["Loan"] = Relationship(back_populates="created_by")
    role: Role = Relationship(back_populates="users")

    create_fields: ClassVar[Tuple] = (
        "id",
        "first_name",
        "last_name",
        "email",
        "password",
        "role_id",
        "disabled",
        "bio",
        "age",
    )
    update_fields: ClassVar[Tuple] = (
        "id",
        "first_name",
        "last_name",
        "email",
        "password",
        "role_id",
        "disabled",
        "bio",
        "age",
    )
    public_fields: ClassVar[Tuple] = (
        "id",
        "first_name",
        "last_name",
        "email",
        "role_id",
        "disabled",
        "bio",
        "age",
        "created_by_id",
        "created_at",
        "updated_by_id",
        "updated_at",
    )


class Customer(SQLModel, table=True):
    id: str = Field(
        sa_column=Column("id", Integer, primary_key=True, autoincrement=True)
    )
    first_name: str
    last_name: str
    email: str = Field(sa_column=Column("email", String, unique=True))

    created_by_id: str = Field(foreign_key="user.id")
    created_at: Optional[datetime] = Field(default_factory=datetime.now)

    updated_by_id: str = Field(foreign_key="user.id")
    updated_at: Optional[datetime] = Field(
        default_factory=datetime.now,
        sa_column_kwargs={"onupdate": datetime.now},
    )

    # books: list["Book"] = Relationship(
    #     back_populates="customers", link_model=Loan
    # )
    # loans: list[Loan] = Relationship(back_populates="customer")
    created_by: User = Relationship(back_populates="customers")

    create_fields: ClassVar[Tuple] = ("first_name", "last_name", "email")
    update_fields: ClassVar[Tuple] = ("first_name", "last_name", "email")
    public_fields: ClassVar[Tuple] = (
        "id",
        "first_name",
        "last_name",
        "email",
        "created_by_id",
        "created_at",
        "updated_by_id",
        "updated_at",
    )


class Book(SQLModel, table=True):
    id: str = Field(
        sa_column=Column("id", Integer, primary_key=True, autoincrement=True)
    )
    title: str
    author: str
    publisher: str
    date: datetime

    created_by_id: str = Field(foreign_key="user.id")
    created_at: Optional[datetime] = Field(default_factory=datetime.now)

    updated_by_id: str = Field(foreign_key="user.id")
    updated_at: Optional[datetime] = Field(
        default_factory=datetime.now,
        sa_column_kwargs={"onupdate": datetime.now},
    )

    # customers: List[Customer] = Relationship(
    #     back_populates="books", link_model=Loan
    # )
    loans: List[Loan] = Relationship(back_populates="book")
    created_by: User = Relationship(back_populates="books")

    create_fields: ClassVar[Tuple] = ("title", "author", "publisher", "date")
    update_fields: ClassVar[Tuple] = ("title", "author", "publisher", "date")
    public_fields: ClassVar[Tuple] = (
        "id",
        "title",
        "author",
        "publisher",
        "date",
        "created_by_id",
        "created_at",
        "updated_by_id",
        "updated_at",
    )


BookCreate = require(Book, *Book.create_fields)
BookUpdate = require(Book, *Book.update_fields)
BookPublic = require(Book, *Book.public_fields)


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
