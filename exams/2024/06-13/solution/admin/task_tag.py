from enum import Enum
from typing import Annotated, List

from auth import RoleChecker
from db import DB
from fastapi import Depends
from model import Result, Tag, Task, TaskTag, User

from . import router


class __db:
    tags = ["Admin - Task / Tag"]
    task_tag = DB[TaskTag](TaskTag, "TaskTag")
    task = DB[Task](Task, "Task")
    tag = DB[Tag](Tag, "Tag")
    allowed_roles_ids = ["admin"]

    def prefix(id: bool = False):
        return "/task-tag" + ("/{id}" if id else "")


class __summary(str, Enum):
    CREATE = "Add a new tag to the task"
    READ_ALL = "Get all the task - tag relationships"
    READ = "Get the details of a task - tag relationship"
    DELETE = "Remove a tag from the task"


@router.post(__db.prefix(), tags=__db.tags, summary=__summary.CREATE)
async def create(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=__db.allowed_roles_ids))
    ],
    task_tag: TaskTag,
) -> Result:
    __db.task.read(task_tag.task_id)
    __db.tag.read(task_tag.tag_id)
    return __db.task_tag.create(task_tag, current_user)


@router.get(__db.prefix(), tags=__db.tags, summary=__summary.READ_ALL)
async def read_all(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=__db.allowed_roles_ids))
    ]
) -> List[TaskTag]:
    return __db.task_tag.read_all()


@router.get(__db.prefix(id=True), tags=__db.tags, summary=__summary.READ)
async def read(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=__db.allowed_roles_ids))
    ],
    id: int,
) -> TaskTag:
    return __db.task_tag.read(id)


@router.delete(
    __db.prefix(id=True),
    tags=__db.tags,
    summary=__summary.DELETE,
)
async def delete(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=__db.allowed_roles_ids))
    ],
    id: int,
) -> Result:
    __db.task_tag.read(id)
    return __db.task_tag.delete(id)
