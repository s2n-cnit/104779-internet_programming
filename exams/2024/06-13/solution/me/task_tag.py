from enum import Enum
from typing import Annotated, List

from auth import RoleChecker
from db import DB
from fastapi import Depends
from model import Result, Tag, Task, TaskTag, User

from . import router


class __db:
    tags = ["Me - Task / Tag"]
    task_tag = DB[TaskTag](TaskTag, "TaskTag")
    task = DB[Task](Task, "Task")
    tag = DB[Tag](Tag, "Task")
    allowed_roles_ids = ["admin", "user"]

    def prefix(id: bool = False, created: bool = False, updated: bool = False):
        return (
            "/task-tag"
            + ("/{id}" if id else "")
            + ("/{created}" if created else "")
            + ("/{updated}" if updated else "")
        )


class __summary(str, Enum):
    CREATE = "Add a new tag to the task"
    READ_ALL_CREATED = "Get all the created task-tag relationships"
    READ = "Get the details of a task-tag relationship"
    DELETE = "Remove a tag from the task"


@router.post(__db.prefix(), tags=__db.tags, summary=__summary.CREATE)
async def create(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=__db.allowed_roles_ids))
    ],
    task_tag: TaskTag,
) -> Result:
    __db.task.read_personal(
        task_tag.task_id,
        current_user.tasks_created + current_user.tasks_updated,
    )
    __db.tag.read_personal(
        task_tag.tag_id,
        current_user.tags_created + current_user.tags_updated,
    )
    return __db.task_tag.create(task_tag, current_user)


@router.get(
    __db.prefix(created=True),
    tags=__db.tags,
    summary=__summary.READ_ALL_CREATED,
)
async def read_all_created(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=__db.allowed_roles_ids))
    ],
) -> List[TaskTag]:
    return current_user.task_tags_created


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
) -> TaskTag:
    return __db.task_tag.read_personal(id, current_user.task_tags_created)


@router.delete(__db.prefix(id=True), tags=__db.tags, summary=__summary.DELETE)
async def delete(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=__db.allowed_roles_ids))
    ],
    id: int,
) -> Result:
    __db.task_tag.read_personal(
        id,
        current_user.task_tags_created,
    )
    return __db.task_tag.delete(id)
