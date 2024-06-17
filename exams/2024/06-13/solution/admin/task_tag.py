from typing import Annotated

from auth import RoleChecker
from db import DB
from fastapi import Depends
from model import Result, Tag, Task, TaskTag, User

from . import router

db_task_tag = DB[TaskTag](TaskTag, "TaskTag")
db_task = DB[Task](Task, "Task")
db_tag = DB[Tag](Tag, "Task")

tags = ["Admin - Task / Tag"]


@router.post("/task-tag", tags=tags, summary="Add a new tag to the task")
async def me_create_task_tag(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin"]))
    ],
    task_tag: TaskTag,
) -> Result:
    db_task.read(task_tag.task_id)
    db_tag.read(task_tag.tag_id)
    return db_task_tag.create(task_tag, current_user)


@router.delete(
    "/task-tag/{task_tag_id}", tags=tags, summary="Remove a tag from the task"
)
async def me_delete_task_tag(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin"]))
    ],
    task_tag_id: int,
) -> Result:
    db_task_tag.read(task_tag_id)
    return db_task_tag.delete(task_tag_id)
