from enum import Enum
from typing import Annotated, List

from auth import RoleChecker
from db import DB, Action
from fastapi import Depends
from model import (
    Command,
    Result,
    User,
    Workflow,
    WorkflowCreate,
    WorkflowPublic,
    WorkflowUpdate,
)

from . import router


class __db:
    tags = ["Admin - Workflow"]
    workflow = DB[Workflow](Workflow, "Workflow")
    allowed_roles_ids = ["admin"]

    def prefix(id: bool = False, start: bool = False, stop: bool = False):
        return (
            "/workflow"
            + ("/{id}" if id else "")
            + ("/start" if start else "")
            + ("/stop" if stop else "")
        )


class __summary(str, Enum):
    CREATE = "Insert a new workflow"
    READ_ALL = "Get all the workflow"
    READ = "Get the details of a workflow"
    UPDATE = "Update a workflow"
    DELETE = "Delete a workflow"
    START = "Start a workflow"
    STOP = "Stop a workflow"


@router.post(__db.prefix(), tags=__db.tags, summary=__summary.CREATE)
async def create(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=__db.allowed_roles_ids))
    ],
    workflow: WorkflowCreate,
) -> Result:
    return __db.workflow.create(workflow, current_user)


@router.get(__db.prefix(), tags=__db.tags, summary=__summary.READ_ALL)
async def read_all(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=__db.allowed_roles_ids))
    ]
) -> List[WorkflowPublic]:
    return __db.workflow.read_all()


@router.get(__db.prefix(id=True), tags=__db.tags, summary=__summary.READ)
async def read(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=__db.allowed_roles_ids))
    ],
    id: int,
) -> WorkflowPublic:
    return __db.workflow.read(id)


@router.put(__db.prefix(id=True), tags=__db.tags, summary=__summary.DELETE)
async def update(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=__db.allowed_roles_ids))
    ],
    id: int,
    workflow: WorkflowUpdate,
) -> Result:
    return __db.workflow.update(id, workflow, current_user)


@router.delete(__db.prefix(id=True), tags=__db.tags, summary=__summary.DELETE)
async def delete(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=__db.allowed_roles_ids))
    ],
    id: int,
) -> Result:
    return __db.workflow.delete(id)


@router.put(
    __db.prefix(id=True, start=True), tags=__db.tags, summary=__summary.START
)
async def start(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=__db.allowed_roles_ids))
    ]
) -> Result:
    workflow = __db.workflow.read(id).check_not_empty()
    map(Command.start, workflow.commands)
    return Result(
        action=Action.STARTED,
        target=workflow.model_text,
        id=workflow.id,
    )


@router.put(
    __db.prefix(id=True, stop=True), tags=__db.tags, summary=__summary.STOP
)
async def stop(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=__db.allowed_roles_ids))
    ]
) -> Result:
    workflow = __db.workflow.read(id).check_not_empty()
    map(Command.stop, workflow.commands)
    return Result(
        action=Action.STOPPED,
        target=workflow.model_text,
        id=workflow.id,
    )
