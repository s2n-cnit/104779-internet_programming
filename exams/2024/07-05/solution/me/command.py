from enum import Enum
from typing import Annotated, List

from auth import RoleChecker
from db import DB
from fastapi import Depends
from model import (Category, Command, CommandCreate, CommandPublic,
                   CommandUpdate, Result, User, Workflow)

from . import router


class __db:
    tags = ["Me - Command"]
    command = DB[Command](Command, "Command")
    workflow = DB[Workflow](Workflow, "Workflow")
    category = DB[Category](Category, "Category")
    allowed_roles_ids = ["admin", "user"]

    def prefix(id: bool = False, created: bool = False, updated: bool = False):
        return ("/command" + ("/{id}" if id else "") +
                ("/created" if created else "") +
                ("/updated" if updated else ""))


class __summary(str, Enum):
    CREATE = "Insert a new command"
    READ_ALL_CREATED = "Get all the created command"
    READ_ALL_UPDATED = "Get all the updated command"
    READ = "Get the details of a command"
    UPDATE = "Update a command"
    ADD_TAG = "Add a tag to the command"
    RM_TAG = "Remove a tag from the command"


@router.post(__db.prefix(), tags=__db.tags, summary=__summary.CREATE)
async def create(
    current_user: Annotated[
        User,
        Depends(RoleChecker(allowed_role_ids=__db.allowed_roles_ids))],
    command: CommandCreate,
) -> Result:
    __db.workflow.read_personal(
        command.workflow_id,
        current_user.workflows_created + current_user.workflows_updated,
    )
    __db.category.read_personal(
        command.category_id,
        current_user.categories_created + current_user.categories_updated,
    )
    return __db.command.create(command, current_user)


@router.get(
    __db.prefix(created=True),
    tags=__db.tags,
    summary=__summary.READ_ALL_CREATED,
)
async def read_all_created(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=__db.allowed_roles_ids))
    ],
) -> List[CommandPublic]:
    return current_user.commands_created


@router.get(
    __db.prefix(updated=True),
    tags=__db.tags,
    summary=__summary.READ_ALL_UPDATED,
)
async def read_all_updated(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=__db.allowed_roles_ids))
    ],
) -> List[CommandPublic]:
    return current_user.commands_updated


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
) -> CommandPublic:
    return __db.command.read_personal(id, current_user.commands_created)


@router.put(__db.prefix(id=True), tags=__db.tags, summary=__summary.UPDATE)
async def update(
    current_user: Annotated[
        User,
        Depends(RoleChecker(allowed_role_ids=__db.allowed_roles_ids))],
    id: int,
    command: CommandUpdate,
) -> Result:
    __db.command.read_personal(id, current_user.commands_created)
    if command.workflow_id is not None:
        __db.workflow.read_personal(
            command.workflow_id,
            current_user.workflows_created + current_user.workflows_updated,
        )
    if command.category_id is not None:
        __db.category.read_personal(
            command.category_id,
            current_user.categories_created + current_user.categories_updated,
        )
    return __db.command.update(id, command, current_user)

@router.put(__db.prefix(id=True, tag=True), tags=__db.tags, summary=__summary.ADD_TAG)
async def add_tag(
    current_user: Annotated[
        User,
        Depends(RoleChecker(allowed_role_ids=__db.allowed_roles_ids))],
    command_id: int,
    tag_id: int):
    __db.command.read_personal(id, current_user.commands_created)
    __db.tag.read_personal(id, current_user.tags_created)
    command_tag = CommandTag(command_id=command_id, tag=tag_id)
    _db.command_tag.create(command_tag, current_user)

@router.delete(__db.prefix(id=True, tag=True), tags=__db.tags, summary=__summary.RM_TAG)
async def rm_tag(
    current_user: Annotated[
        User,
        Depends(RoleChecker(allowed_role_ids=__db.allowed_roles_ids))],
    id: int,
    _db.command_tag.delete(command_tag.id)
