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
    tags = ["Me - Task"]
    task = DB[Task](Task, "Task")
    category = DB[Category](Category, "Category")
    allowed_roles_ids = ["admin", "user"]

    def prefix(id: bool = False, created: bool = False, updated: bool = False):
        return (
            "/tag"
            + ("/{id}" if id else "")
            + ("/{created}" if created else "")
            + ("/{updated}" if updated else "")
        )


class __summary(str, Enum):
    CREATE = "Insert a new task"
    READ_ALL_CREATED = "Get all the created task"
    READ_ALL_UPDATED = "Get all the updated task"
    READ = "Get the details of a task"
    UPDATE = "Update a task"


@router.post(__db.prefix(), tags=__db.tags, summary=__summary.CREATE)
async def create(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=__db.allowed_roles_ids))
    ],
    task: TaskCreate,
) -> Result:
    __db.category.read_personal(
        task.category_id,
        current_user.categories_created + current_user.categories_updated,
    )
    return __db.task.create(task, current_user)


@router.get(
    __db.prefix(created=True),
    tags=__db.tags,
    summary=__summary.READ_ALL_CREATED,
)
async def read_all_created(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=__db.allowed_roles_ids))
    ],
) -> List[TaskPublic]:
    return current_user.tasks_created


@router.get(
    __db.prefix(updated=True),
    tags=__db.tags,
    summary=__summary.READ_ALL_UPDATED,
)
async def read_all_updated(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=__db.allowed_roles_ids))
    ],
) -> List[TaskPublic]:
    return current_user.tasks_updated


@router.get(
    __db.prefix(id=True),
    tags=__db.tags,
    summary=__summary.READ,
)
async def read(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=__db.allowed_roles_ids))
    ],
    id: int,
) -> TaskPublic:
    return __db.task.read_personal(id, current_user.tasks_created)


@router.put(__db.prefix(id=True), tags=__db.tags, summary=__summary.UPDATE)
async def update(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=__db.allowed_roles_ids))
    ],
    id: int,
    task: TaskUpdate,
) -> Result:
    __db.task.read_personal(id, current_user.tasks_created)
    return __db.task.update(id, task, current_user)
