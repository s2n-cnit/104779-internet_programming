from enum import Enum
from typing import Annotated, List

from auth import RoleChecker
from db import DB
from fastapi import Depends
from model import (
    Category,
    Result,
    Task,
    TaskCreate,
    TaskPublic,
    TaskUpdate,
    User,
)

from . import router


class __db:
    tags = ["Admin - Task"]
    task = DB[Task](Task, "Task")
    category = DB[Category](Category, "Category")
    allowed_roles_ids = ["admin"]

    def prefix(id: bool = False):
        return "/task" + ("/{id}" if id else "")


class __summary(str, Enum):
    CREATE = "Insert a new task"
    READ_ALL = "Get all the tasks"
    READ = "Get the details of a task"
    UPDATE = "Update a task"
    DELETE = "Delete a task"


@router.post(__db.prefix(), tags=__db.tags, summary=__summary.CREATE)
async def create(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=__db.allowed_roles_ids))
    ],
    task: TaskCreate,
) -> Result:
    __db.category.read(task.category_id)
    return __db.task.create(task, current_user)


@router.get(__db.prefix(), tags=__db.tags, summary=__summary.READ_ALL)
async def read_all(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=__db.allowed_roles_ids))
    ]
) -> List[TaskPublic]:
    return __db.task.read_all()


@router.get(__db.prefix(id=True), tags=__db.tags, summary=__summary.READ)
async def read(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=__db.allowed_roles_ids))
    ],
    id: int,
) -> TaskPublic:
    return __db.task.read(id)


@router.put(__db.prefix(id=True), tags=__db.tags, summary=__summary.DELETE)
async def update(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=__db.allowed_roles_ids))
    ],
    id: int,
    task: TaskUpdate,
) -> Result:
    return __db.task.update(id, task, current_user)


@router.delete(__db.prefix(id=True), tags=__db.tags, summary=__summary.DELETE)
async def delete(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=__db.allowed_roles_ids))
    ],
    id: int,
) -> Result:
    return __db.task.delete(id)
