from datetime import datetime
from enum import Enum
from typing import List, Optional, Self

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


# TaskTag


class TaskTag(SQLModel, table=True):
    id: int = Field(
        sa_column=Column("id", Integer, primary_key=True, autoincrement=True)
    )
    task_id: int = Field(foreign_key="task.id")
    tag_id: int = Field(foreign_key="tag.id")
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    created_by_id: Optional[str] = Field(foreign_key="user.id")
    created_by: "User" = Relationship(
        back_populates="task_tags_created",
        sa_relationship_kwargs={
            "primaryjoin": "TaskTag.created_by_id==User.id",
            "lazy": "joined",
        },
    )


# Task


class Status(Enum):
    COMPLETED = "completed"
    STARTED = "started"
    TODO = "todo"


class TaskCreate(SQLModel):
    name: str
    category_id: int = Field(foreign_key="category.id")
    status: Status = Field(default=Status.TODO)
    started_date: Optional[datetime] = Field(default=None)
    completed_date: Optional[datetime] = Field(default=None)


class TaskUpdate(SQLModel):
    name: Optional[str] = None
    category_id: Optional[int] = Field(foreign_key="category.id", default=None)
    status: Optional[Status] = Field(default=None)
    started_date: Optional[datetime] = Field(default=None)
    completed_date: Optional[datetime] = Field(default=None)


class TaskPublic(TaskCreate, BasePublic):
    id: int = Field(
        sa_column=Column("id", Integer, primary_key=True, autoincrement=True)
    )


class Task(TaskPublic, table=True):
    tags: "Tag" = Relationship(back_populates="tasks", link_model=TaskTag)
    category: "Category" = Relationship(
        back_populates="tasks",
        sa_relationship_kwargs={
            "primaryjoin": "Task.category_id==Category.id",
            "lazy": "joined",
        },
    )
    created_by: "User" = Relationship(
        back_populates="tasks_created",
        sa_relationship_kwargs={
            "primaryjoin": "Task.created_by_id==User.id",
            "lazy": "joined",
        },
    )
    updated_by: "User" = Relationship(
        back_populates="tasks_updated",
        sa_relationship_kwargs={
            "primaryjoin": "Task.updated_by_id==User.id",
            "lazy": "joined",
        },
    )

    def additional_updates(self: Self) -> Self:
        match self.status:
            case Status.TODO:
                self.started_date = None
                self.completed_date = None
            case Status.STARTED:
                self.started_date = datetime.now()
                self.completed_date = None
            case Status.COMPLETED:
                self.completed_date = datetime.now()


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
    tags_created: list["Tag"] = Relationship(
        back_populates="created_by",
        sa_relationship_kwargs={
            "primaryjoin": "Tag.created_by_id==User.id",
            "lazy": "joined",
        },
    )
    tags_updated: list["Tag"] = Relationship(
        back_populates="updated_by",
        sa_relationship_kwargs={
            "primaryjoin": "Tag.updated_by_id==User.id",
            "lazy": "joined",
        },
    )
    task_tags_created: list["TaskTag"] = Relationship(
        back_populates="created_by",
        sa_relationship_kwargs={
            "primaryjoin": "TaskTag.created_by_id==User.id",
            "lazy": "joined",
        },
    )
    categories_created: list["Category"] = Relationship(
        back_populates="created_by",
        sa_relationship_kwargs={
            "primaryjoin": "Category.created_by_id==User.id",
            "lazy": "joined",
        },
    )
    categories_updated: list["Category"] = Relationship(
        back_populates="updated_by",
        sa_relationship_kwargs={
            "primaryjoin": "Category.updated_by_id==User.id",
            "lazy": "joined",
        },
    )
    tasks_created: list["Task"] = Relationship(
        back_populates="created_by",
        sa_relationship_kwargs={
            "primaryjoin": "Task.created_by_id==User.id",
            "lazy": "joined",
        },
    )
    tasks_updated: list["Task"] = Relationship(
        back_populates="updated_by",
        sa_relationship_kwargs={
            "primaryjoin": "Task.updated_by_id==User.id",
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


# Category


class CategoryCreate(SQLModel):
    name: str


class CategoryUpdate(CategoryCreate):
    pass


class CategoryPublic(CategoryCreate, BasePublic):
    id: int = Field(
        sa_column=Column("id", Integer, primary_key=True, autoincrement=True)
    )


class Category(CategoryPublic, table=True):
    tasks: list[Task] = Relationship(
        back_populates="category",
        sa_relationship_kwargs={
            "primaryjoin": "Task.category_id==Category.id",
            "lazy": "joined",
        },
    )
    created_by: User = Relationship(
        back_populates="categories_created",
        sa_relationship_kwargs={
            "primaryjoin": "Category.created_by_id==User.id",
            "lazy": "joined",
        },
    )
    updated_by: User = Relationship(
        back_populates="categories_updated",
        sa_relationship_kwargs={
            "primaryjoin": "Category.updated_by_id==User.id",
            "lazy": "joined",
        },
    )


# Tag


class TagCreate(SQLModel):
    name: str


class TagUpdate(TagCreate):
    pass


class TagPublic(TagCreate, BasePublic):
    id: int = Field(
        sa_column=Column("id", Integer, primary_key=True, autoincrement=True)
    )


class Tag(TagPublic, table=True):
    tasks: List[Task] = Relationship(back_populates="tags", link_model=TaskTag)
    created_by: User = Relationship(
        back_populates="tags_created",
        sa_relationship_kwargs={
            "primaryjoin": "Tag.created_by_id==User.id",
            "lazy": "joined",
        },
    )
    updated_by: User = Relationship(
        back_populates="tags_updated",
        sa_relationship_kwargs={
            "primaryjoin": "Tag.updated_by_id==User.id",
            "lazy": "joined",
        },
    )


# Result


class Result(BaseModel):
    action: str
    target: str
    id: str | int
    success: bool
    error: bool
    # timestamp: datetime # FIXME not JSON serializable

    def __init__(
        self: Self,
        target: str,
        id: Optional[str | int],
        action: str,
        success: bool = True,
    ) -> Self:
        super().__init__(
            action=action,
            target=target,
            id=id,
            # timestamp=datetime.now(), # FIXME not JSON serializable
            success=success,
            error=not success,
        )


# Token


class Token[Type: SQLModel](BaseModel):
    access_token: str | None = None
    refresh_token: str | None = None


sqlite_file_name = "yatms.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=False)

SQLModel.metadata.create_all(engine)
