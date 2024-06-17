from typing import Annotated, List

from auth import RoleChecker
from db import DB
from fastapi import Depends
from model import Result, Task, TaskCreate, TaskPublic, TaskUpdate, User

from . import router

db_task = DB[Task](Task, "Task")

tags = ["Admin - Task"]


@router.post("/task", tags=tags, summary="Insert a new task")
async def admin_create_task(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin"]))
    ],
    task: TaskCreate,
) -> Result:
    return db_task.create(task, current_user)


@router.get("/task", tags=tags, summary="Read all tasks")
async def admin_read_tasks(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin"]))
    ]
) -> List[TaskPublic]:
    return db_task.read_all()


@router.get("/task/{task_id}", tags=tags, summary="Get the details of a task")
async def admin_read_task(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin"]))
    ],
    task_id: int,
) -> TaskPublic:
    return db_task.read(task_id)


@router.put("/task/{task_id}", tags=tags, summary="Update a task")
async def admin_update_task(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin"]))
    ],
    task_id: int,
    task: TaskUpdate,
) -> Result:
    return db_task.update(task_id, task, current_user)


@router.delete("/task/{task_id}", tags=tags, summary="Delete a task")
async def admin_delete_task(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin"]))
    ],
    task_id: int,
) -> Result:
    return db_task.delete(task_id)
