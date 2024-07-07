from enum import Enum
from typing import Annotated, List

from auth import RoleChecker
from db import DB
from fastapi import Depends
from model import (Category, Command, CommandCreate, CommandPublic,
                   CommandUpdate, Result, User, Workflow)

from . import router


class __db:
    tags = ["Admin - Command"]
    command = DB[Command](Command, "Command")
    workflow = DB[Workflow](Workflow, "Workflow")
    category = DB[Category](Category, "Category")
    allowed_roles_ids = ["admin"]

    def prefix(id: bool = False):
        return "/command" + ("/{id}" if id else "")


class __summary(str, Enum):
    CREATE = "Insert a new command"
    READ_ALL = "Get all the command"
    READ = "Get the details of a command"
    UPDATE = "Update a command"
    DELETE = "Delete a command"


@router.post(__db.prefix(), tags=__db.tags, summary=__summary.CREATE)
async def create(
    current_user: Annotated[
        User,
        Depends(RoleChecker(allowed_role_ids=__db.allowed_roles_ids))],
    command: CommandCreate,
) -> Result:
    __db.workflow.read(command.workflow_id)
    __db.category.read(command.category_id)
    return __db.command.create(command, current_user)


@router.get(__db.prefix(), tags=__db.tags, summary=__summary.READ_ALL)
async def read_all(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=__db.allowed_roles_ids))
    ]
) -> List[CommandPublic]:
    return __db.command.read_all()


@router.get(__db.prefix(id=True), tags=__db.tags, summary=__summary.READ)
async def read(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=__db.allowed_roles_ids))
    ],
    id: int,
) -> CommandPublic:
    return __db.command.read(id)


@router.put(__db.prefix(id=True), tags=__db.tags, summary=__summary.DELETE)
async def update(
    current_user: Annotated[
        User,
        Depends(RoleChecker(allowed_role_ids=__db.allowed_roles_ids))],
    id: int,
    command: CommandUpdate,
) -> Result:
    if command.workflow_id is not None:
        __db.workflow.read(command.workflow_id)
    if command.category_id is not None:
        __db.category.read(command.category_id)
    return __db.command.update(id, command, current_user)


@router.delete(__db.prefix(id=True), tags=__db.tags, summary=__summary.DELETE)
async def delete(
    current_user: Annotated[
        User,
        Depends(RoleChecker(allowed_role_ids=__db.allowed_roles_ids))],
    id: int,
) -> Result:
    return __db.command.delete(id)
