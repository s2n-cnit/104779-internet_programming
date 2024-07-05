from enum import Enum
from typing import Annotated, List

from auth import RoleChecker
from db import DB
from fastapi import Depends
from model import Command, Result, User, Workflow, WorkflowCommand

from . import router


class __db:
    tags = ["Admin - Workflow / Command"]
    workflow_command = DB[WorkflowCommand](WorkflowCommand, "WorkflowCommand")
    workflow = DB[Workflow](Workflow, "Workflow")
    command = DB[Command](Command, "Command")
    allowed_roles_ids = ["admin"]

    def prefix(id: bool = False):
        return "/workflow-command" + ("/{id}" if id else "")


class __summary(str, Enum):
    CREATE = "Add a new command to the workflow"
    READ_ALL = "Get all the workflow - command relationships"
    READ = "Get the details of a workflow - command relationship"
    DELETE = "Remove a command from the workflow"


@router.post(__db.prefix(), tags=__db.tags, summary=__summary.CREATE)
async def create(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=__db.allowed_roles_ids))
    ],
    workflow_command: WorkflowCommand,
) -> Result:
    __db.workflow.read(workflow_command.command_id)
    __db.command.read(workflow_command.tag_id)
    return __db.workflow_command.create(workflow_command, current_user)


@router.get(__db.prefix(), tags=__db.tags, summary=__summary.READ_ALL)
async def read_all(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=__db.allowed_roles_ids))
    ]
) -> List[WorkflowCommand]:
    return __db.workflow_command.read_all()


@router.get(__db.prefix(id=True), tags=__db.tags, summary=__summary.READ)
async def read(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=__db.allowed_roles_ids))
    ],
    id: int,
) -> WorkflowCommand:
    return __db.workflow_command.read(id)


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
    __db.workflow_command.read(id)
    return __db.workflow_command.delete(id)
