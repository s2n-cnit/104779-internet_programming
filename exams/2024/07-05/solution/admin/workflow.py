from enum import Enum
from threading import Thread
from typing import Annotated, List

from auth import RoleChecker
from db import DB, Action
from fastapi import Depends
from model import (Command, Result, User, Workflow, WorkflowCreate,
                   WorkflowPublic, WorkflowUpdate)
from utils import threaded

from . import router


class __db:
    tags = ["Admin - Workflow"]
    workflow = DB[Workflow](Workflow, "Workflow")
    command = DB[Command](Command, "Command")
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
    ],
    id: int,
) -> Result:
    return _execute(id, Action.STARTED, current_user)


@router.put(
    __db.prefix(id=True, stop=True), tags=__db.tags, summary=__summary.STOP
)
async def stop(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=__db.allowed_roles_ids))
    ],
    id: int,
) -> Result:
    return _execute(id, Action.STOPPED, current_user)


def _execute(id: str, action: Action, current_user: User):
    workflow = __db.workflow.read(id).check_not_empty()
    for command in workflow.commands:
        match action:
            case Action.STARTED:
                _t = command.start()
                command.started_by_id = current_user
                _waiting_execution(_t, command, current_user)
            case Action.STOPPED:
                command.stop()
                command.stopped_by_id = current_user
        __db.command.update(command.id, command, current_user)
    return Result(
        action=action,
        target=workflow.model_text,
        id=workflow.id,
    )


@threaded
def _waiting_execution(
    thread: Thread, command: Command, current_user: User
) -> None:
    if thread.is_alive():
        thread.join()
        __db.command.update(command.id, command, current_user)

# FIXME avoid repeating code in me and admin
