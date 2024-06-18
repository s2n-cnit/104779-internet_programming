from typing import Annotated, List

from auth import RoleChecker
from db import DB
from fastapi import Depends
from model import Result, Tag, Task, TaskTag, User

from . import router

db_task_tag = DB[TaskTag](TaskTag, "TaskTag")
db_task = DB[Task](Task, "Task")
db_tag = DB[Tag](Tag, "Task")

tags = ["Me - Task / Tag"]


@router.post("/task-tag", tags=tags, summary="Add a new tag to the task")
async def me_create_task_tag(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin", "user"]))
    ],
    task_tag: TaskTag,
) -> Result:
    db_task.read_personal(
        task_tag.task_id,
        current_user.tasks_created + current_user.tasks_updated,
    )
    db_tag.read_personal(
        task_tag.tag_id,
        current_user.tags_created + current_user.tags_updated,
    )
    return db_task_tag.create(task_tag, current_user)


@router.get(
    "/task-tag/created",
    tags=tags,
    summary="Get all the created task-tag relationships",
)
async def me_read_task_tags_created(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin", "user"]))
    ],
) -> List[TaskTag]:
    return current_user.task_tags_created


@router.get(
    "/task-tag/{task_tag_id}",
    tags=tags,
    summary="Get the details of a task-tag relationship",
)
async def me_read_task_tag(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin", "user"]))
    ],
    task_tag_id: int,
) -> TaskTag:
    return db_task_tag.read_personal(
        task_tag_id, current_user.task_tags_created
    )


@router.delete(
    "/task-tag/{task_tag_id}", tags=tags, summary="Remove a tag from the task"
)
async def me_delete_task_tag(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin", "user"]))
    ],
    task_tag_id: int,
) -> Result:
    db_task_tag.read_personal(
        task_tag_id,
        current_user.task_tags_created,
    )
    return db_task_tag.delete(task_tag_id)
