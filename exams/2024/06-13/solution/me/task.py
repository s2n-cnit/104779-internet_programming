from typing import Annotated, List

from auth import RoleChecker
from db import DB
from fastapi import Depends
from model import Result, Task, TaskCreate, TaskPublic, TaskUpdate, User

from . import router

db_task = DB[Task](Task, "Task")

tags = ["Me - Task"]


@router.post("/task", tags=tags, summary="Insert a new task")
async def admin_create_task(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin", "user"]))
    ],
    task: TaskCreate,
) -> Result:
    return db_task.create(task, current_user)


@router.get(
    "/task/created",
    tags=tags,
    summary="Get all the created tasks",
)
async def me_read_tasks_created(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin", "user"]))
    ],
) -> List[TaskPublic]:
    return current_user.tasks_created


@router.get(
    "/task/updated",
    tags=tags,
    summary="Get all the updated tasks",
)
async def me_read_tasks_updated(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin", "user"]))
    ],
) -> List[TaskPublic]:
    return current_user.tasks_updated


@router.get(
    "/task/{task_id}",
    tags=tags,
    summary="Get the details of the task",
)
async def me_read_task(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin", "user"]))
    ],
    task_id: int,
) -> TaskPublic:
    return db_task.read_personal(task_id, current_user.tasks_created)


@router.put("/task/{task_id}", tags=tags, summary="Update a task")
async def me_update_task(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin", "user"]))
    ],
    task_id: int,
    task: TaskUpdate,
) -> Result:
    db_task.read_personal(task_id, current_user.tasks_created)
    return db_task.create(task, current_user)
