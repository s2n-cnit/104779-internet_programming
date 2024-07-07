from datetime import datetime
from enum import Enum
from random import randrange, seed
from time import sleep
from typing import List, Optional, Self

from config import db_path, echo_engine, logger
from error import ConflictException, EmptyException
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from sqlmodel import Field, Relationship, SQLModel, create_engine
from utils import threaded

# Base

seed()


class BasePublic(SQLModel):
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(
        default_factory=datetime.now,
        sa_column_kwargs={"onupdate": datetime.now},
    )
    created_by_id: Optional[str] = Field(foreign_key="user.id")
    updated_by_id: Optional[str] = Field(foreign_key="user.id")


# CommandTag


class CommandTag(SQLModel, table=True):
    id: int = Field(
        sa_column=Column("id", Integer, primary_key=True, autoincrement=True)
    )
    command_id: int = Field(foreign_key="command.id")
    tag_id: int = Field(foreign_key="tag.id")
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    created_by_id: Optional[str] = Field(foreign_key="user.id")
    created_by: "User" = Relationship(
        back_populates="command_tags_created",
        sa_relationship_kwargs={
            "primaryjoin": "CommandTag.created_by_id==User.id",
            "lazy": "joined",
        },
    )


# Workflow


class WorkflowCreate(SQLModel):
    name: str


class WorkflowUpdate(SQLModel):
    name: str


class WorkflowPublic(WorkflowCreate, BasePublic):
    id: int = Field(
        sa_column=Column("id", Integer, primary_key=True, autoincrement=True)
    )


class Workflow(WorkflowPublic, table=True):
    commands: list["Command"] = Relationship(
        back_populates="category",
        sa_relationship_kwargs={
            "primaryjoin": "Command.workflow_id==Workflow.id",
            "lazy": "joined",
        },
    )
    created_by: "User" = Relationship(
        back_populates="workflows_created",
        sa_relationship_kwargs={
            "primaryjoin": "Workflow.created_by_id==User.id",
            "lazy": "joined",
        },
    )
    updated_by: "User" = Relationship(
        back_populates="workflows_updated",
        sa_relationship_kwargs={
            "primaryjoin": "Workflow.updated_by_id==User.id",
            "lazy": "joined",
        },
    )

    def check_not_empty(self: Self) -> Self:
        if len(self.command) == 0:
            raise EmptyException(target="Workflow", id=self.id)
        return self


# Command


class CommandStatus(Enum):
    COMPLETED = "completed"
    STARTED = "started"
    STOPPED = "stopped"
    NOT_EXECUTED = "not-executed"


class CommandCreate(SQLModel):
    path: str
    category_id: int = Field(foreign_key="category.id")
    workflow_id: int = Field(foreign_key="workflow.id")


class CommandUpdate(SQLModel):
    path: Optional[str] = None
    category_id: Optional[int] = Field(foreign_key="category.id", default=None)
    workflow_id: Optional[int] = Field(foreign_key="workflow.id", default=None)


class CommandPublic(CommandCreate, BasePublic):
    id: int = Field(
        sa_column=Column("id", Integer, primary_key=True, autoincrement=True)
    )
    started_at: Optional[datetime] = Field(default=None)
    started_by_id: Optional[str] = Field(foreign_key="user.id")
    completed_at: Optional[datetime] = Field(default=None)
    stopped_at: Optional[datetime] = Field(default=None)
    stopped_by_id: Optional[str] = Field(foreign_key="user.id")
    status: CommandStatus = Field(default=CommandStatus.NOT_EXECUTED)


class Command(CommandPublic, table=True):
    tags: List["Tag"] = Relationship(
        back_populates="commands", link_model=CommandTag
    )
    category: "Category" = Relationship(
        back_populates="commands",
        sa_relationship_kwargs={
            "primaryjoin": "Command.category_id==Category.id",
            "lazy": "joined",
        },
    )
    workflow: "Workflow" = Relationship(
        back_populates="commands",
        sa_relationship_kwargs={
            "primaryjoin": "Command.workflow_id==Workflow.id",
            "lazy": "joined",
        },
    )
    created_by: "User" = Relationship(
        back_populates="commands_created",
        sa_relationship_kwargs={
            "primaryjoin": "Command.created_by_id==User.id",
            "lazy": "joined",
        },
    )
    updated_by: "User" = Relationship(
        back_populates="commands_updated",
        sa_relationship_kwargs={
            "primaryjoin": "Command.updated_by_id==User.id",
            "lazy": "joined",
        },
    )

    def start(self: Self) -> None:
        if self.status == CommandStatus.STARTED:
            raise ConflictException(target="Command", id=self.id)
        self.started_at = datetime.now()
        self.completed_at = None
        self.stopped_at = None
        self.status = CommandStatus.STARTED
        logger.info(f"Command {self.path} started")
        return self._execute()

    def stop(self: Self) -> None:
        self.completed_at = datetime.now()
        if self.status in [CommandStatus.STOPPED, CommandStatus.NOT_EXECUTED]:
            raise ConflictException(target="Command", id=self.id)
        self.stopped_at = datetime.now()
        self.status = CommandStatus.STOPPED
        logger.info(f"Command {self.path} stopped")

    @threaded
    def _execute(self: Self) -> None:
        _t = randrange(10) * 1000
        for i in range(_t, 0, -1):
            if self.stopped_at is not None:
                return None
            logger.info(f"Command {self.path} in execution... (-{i}) seconds")
            sleep(i * 1000)
        self.completed_at = datetime.now()
        self.status = CommandStatus.COMPLETED

# Role


class RoleCreate(SQLModel):
    id: str = Field(primary_key=True)
    description: str | None = None


class RoleUpdate(RoleCreate):
    pass


class RolePublic(RoleCreate, BasePublic):
    pass


class Role(RolePublic, table=True):
    pass


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
    command_tags_created: list["CommandTag"] = Relationship(
        back_populates="created_by",
        sa_relationship_kwargs={
            "primaryjoin": "CommandTag.created_by_id==User.id",
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
    workflows_created: list["Workflow"] = Relationship(
        back_populates="created_by",
        sa_relationship_kwargs={
            "primaryjoin": "Workflow.created_by_id==User.id",
            "lazy": "joined",
        },
    )
    workflows_updated: list["Workflow"] = Relationship(
        back_populates="updated_by",
        sa_relationship_kwargs={
            "primaryjoin": "Workflow.updated_by_id==User.id",
            "lazy": "joined",
        },
    )
    commands_created: list["Command"] = Relationship(
        back_populates="created_by",
        sa_relationship_kwargs={
            "primaryjoin": "Command.created_by_id==User.id",
            "lazy": "joined",
        },
    )
    commands_updated: list["Command"] = Relationship(
        back_populates="updated_by",
        sa_relationship_kwargs={
            "primaryjoin": "Command.updated_by_id==User.id",
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
    commands: list[Command] = Relationship(
        back_populates="category",
        sa_relationship_kwargs={
            "primaryjoin": "Command.category_id==Category.id",
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
    commands: List[Command] = Relationship(
        back_populates="tags", link_model=CommandTag
    )
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


engine = create_engine(f"sqlite:///{db_path}", echo=echo_engine)
SQLModel.metadata.create_all(engine)
