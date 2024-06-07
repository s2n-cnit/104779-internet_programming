from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from sqlmodel import Field, Relationship, SQLModel, create_engine

# Base


class BasePublic(SQLModel):
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(
        default_factory=datetime.now,
        sa_column_kwargs={"onupdate": datetime.now},
    )
    created_by_id: Optional[str] = Field(foreign_key="user.id")
    updated_by_id: Optional[str] | None = Field(foreign_key="user.id")


# Loan


class LoanCreate(SQLModel):
    customer_id: str = Field(foreign_key="customer.id")
    book_id: str = Field(foreign_key="book.id")


class LoanUpdate(SQLModel):
    pass


class LoanPublic(LoanCreate, BasePublic):
    id: int = Field(
        sa_column=Column("id", Integer, primary_key=True, autoincrement=True)
    )


class Loan(LoanPublic, table=True):
    book: "Book" = Relationship(
        back_populates="loans",
        sa_relationship_kwargs={
            "primaryjoin": "Book.id==Loan.book_id",
            "lazy": "joined",
        },
    )
    customer: "Customer" = Relationship(
        back_populates="loans",
        sa_relationship_kwargs={
            "primaryjoin": "Loan.customer_id==Customer.id",
            "lazy": "joined",
        },
    )
    created_by: "User" = Relationship(
        back_populates="loans_created",
        sa_relationship_kwargs={
            "primaryjoin": "Loan.created_by_id==User.id",
            "lazy": "joined",
        },
    )
    updated_by: "User" = Relationship(
        back_populates="loans_updated",
        sa_relationship_kwargs={
            "primaryjoin": "Loan.updated_by_id==User.id",
            "lazy": "joined",
        },
    )


# Role


class RoleCreate(SQLModel):
    id: str = Field(primary_key=True)
    description: str | None = None


class RoleUpdate(RoleCreate):
    pass


class RolePublic(RoleCreate, BasePublic):
    pass


class Role(RolePublic, table=True):
    users: List["User"] = Relationship(
        back_populates="role",
        sa_relationship_kwargs={
            "primaryjoin": "Role.id==User.role_id",
            "lazy": "joined",
        },
    )
    created_by: "User" = Relationship(
        back_populates="roles_created",
        sa_relationship_kwargs={
            "primaryjoin": "Role.created_by_id==User.id",
            "lazy": "joined",
        },
    )
    updated_by: "User" = Relationship(
        back_populates="roles_updated",
        sa_relationship_kwargs={
            "primaryjoin": "Role.updated_by_id==User.id",
            "lazy": "joined",
        },
    )


# User


class UserCreate(SQLModel):
    id: str = Field(primary_key=True)
    first_name: str
    last_name: str
    email: str = Field(sa_column=Column("email", String, unique=True))
    password: str
    role_id: str = Field(foreign_key="role.id")
    disabled: bool = False
    bio: str | None = None
    age: int | None = None


class UserUpdate(UserCreate):
    pass


class UserPublic(BasePublic):
    id: str = Field(primary_key=True)
    first_name: str
    last_name: str
    email: str = Field(sa_column=Column("email", String, unique=True))
    role_id: str = Field(foreign_key="role.id")
    disabled: bool = False
    bio: str | None = None
    age: int | None = None


class User(UserCreate, BasePublic, table=True):
    books_created: list["Book"] = Relationship(
        back_populates="created_by",
        sa_relationship_kwargs={
            "primaryjoin": "Book.created_by_id==User.id",
            "lazy": "joined",
        },
    )
    books_updated: list["Book"] = Relationship(
        back_populates="updated_by",
        sa_relationship_kwargs={
            "primaryjoin": "Book.updated_by_id==User.id",
            "lazy": "joined",
        },
    )
    customers_created: list["Customer"] = Relationship(
        back_populates="created_by",
        sa_relationship_kwargs={
            "primaryjoin": "Customer.created_by_id==User.id",
            "lazy": "joined",
        },
    )
    customers_updated: list["Customer"] = Relationship(
        back_populates="updated_by",
        sa_relationship_kwargs={
            "primaryjoin": "Customer.updated_by_id==User.id",
            "lazy": "joined",
        },
    )
    loans_created: list["Loan"] = Relationship(
        back_populates="created_by",
        sa_relationship_kwargs={
            "primaryjoin": "Loan.created_by_id==User.id",
            "lazy": "joined",
        },
    )
    loans_updated: list["Loan"] = Relationship(
        back_populates="updated_by",
        sa_relationship_kwargs={
            "primaryjoin": "Loan.updated_by_id==User.id",
            "lazy": "joined",
        },
    )
    role: Role = Relationship(
        back_populates="users",
        sa_relationship_kwargs={
            "primaryjoin": "User.role_id==Role.id",
            "lazy": "joined",
        },
    )
    roles_created: list["Role"] = Relationship(
        back_populates="created_by",
        sa_relationship_kwargs={
            "primaryjoin": "Role.created_by_id==User.id",
            "lazy": "joined",
        },
    )
    roles_updated: list["Role"] = Relationship(
        back_populates="updated_by",
        sa_relationship_kwargs={
            "primaryjoin": "Role.updated_by_id==User.id",
            "lazy": "joined",
        },
    )


# Customer


class CustomerCreate(SQLModel):
    first_name: str
    last_name: str
    email: str = Field(sa_column=Column("email", String, unique=True))


class CustomerUpdate(CustomerCreate):
    pass


class CustomerPublic(CustomerCreate, BasePublic):
    id: int = Field(
        sa_column=Column("id", Integer, primary_key=True, autoincrement=True)
    )


class Customer(CustomerPublic, table=True):
    books: list["Book"] = Relationship(
        back_populates="customers",
        link_model=Loan,
    )
    loans: list[Loan] = Relationship(
        back_populates="customer",
        sa_relationship_kwargs={
            "primaryjoin": "Loan.customer_id==Customer.id",
            "lazy": "joined",
        },
    )
    created_by: User = Relationship(
        back_populates="customers_created",
        sa_relationship_kwargs={
            "primaryjoin": "Customer.created_by_id==User.id",
            "lazy": "joined",
        },
    )
    updated_by: User = Relationship(
        back_populates="customers_updated",
        sa_relationship_kwargs={
            "primaryjoin": "Customer.updated_by_id==User.id",
            "lazy": "joined",
        },
    )


# Book


class BookCreate(SQLModel):
    title: str
    author: str
    publisher: str
    date: datetime


class BookUpdate(BookCreate):
    pass


class BookPublic(BookCreate, BasePublic):
    id: int = Field(
        sa_column=Column("id", Integer, primary_key=True, autoincrement=True)
    )


class Book(BookPublic, table=True):
    customers: List[Customer] = Relationship(
        back_populates="books",
        link_model=Loan,
    )
    loans: List[Loan] = Relationship(
        back_populates="book",
        sa_relationship_kwargs={
            "primaryjoin": "Book.id==Loan.book_id",
            "lazy": "joined",
        },
    )
    created_by: User = Relationship(
        back_populates="books_created",
        sa_relationship_kwargs={
            "primaryjoin": "Book.created_by_id==User.id",
            "lazy": "joined",
        },
    )
    updated_by: User = Relationship(
        back_populates="books_updated",
        sa_relationship_kwargs={
            "primaryjoin": "Book.updated_by_id==User.id",
            "lazy": "joined",
        },
    )


# Result


class Result(BaseModel):
    success: bool
    detail: str
    timestamp: datetime

    def __init__(
        self: "Result",
        detail: str,
        success: bool = True,
    ) -> "Result":
        super().__init__(
            success=success, detail=detail, timestamp=datetime.now()
        )


# Token


class Token[Type: SQLModel](BaseModel):
    access_token: str | None = None
    refresh_token: str | None = None


sqlite_file_name = "yalb.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

SQLModel.metadata.create_all(engine)
