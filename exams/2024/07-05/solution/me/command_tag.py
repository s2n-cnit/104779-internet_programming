from enum import Enum
from typing import Annotated, List

from auth import RoleChecker
from db import DB
from fastapi import Depends
from model import Command, CommandTag, Result, User

from . import router


class __db:
    tags = ["Me - Command / Tag"]
    command_tag = DB[CommandTag](CommandTag, "CommandTag")
    command = DB[Command](Command, "Command")
    tag = DB[Command](Command, "Command")
    allowed_roles_ids = ["admin", "user"]

    def prefix(id: bool = False, created: bool = False, updated: bool = False):
        return (
            "/command-tag"
            + ("/{id}" if id else "")
            + ("/created" if created else "")
            + ("/updated" if updated else "")
        )


class __summary(str, Enum):
    CREATE = "Add a new tag to the command"
    READ_ALL_CREATED = "Get all the created command-tag relationships"
    READ = "Get the details of a command-tag relationship"
    DELETE = "Remove a tag from the command"


@router.post(__db.prefix(), tags=__db.tags, summary=__summary.CREATE)
async def create(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=__db.allowed_roles_ids))
    ],
    command_tag: CommandTag,
) -> Result:
    __db.command.read_personal(
        command_tag.Command_id,
        current_user.Commands_created + current_user.Commands_updated,
    )
    __db.tag.read_personal(
        command_tag.tag_id,
        current_user.tags_created + current_user.commands_updated,
    )
    return __db.command_tag.create(command_tag, current_user)


@router.get(
    __db.prefix(created=True),
    tags=__db.tags,
    summary=__summary.READ_ALL_CREATED,
)
async def read_all_created(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=__db.allowed_roles_ids))
    ],
) -> List[Command]:
    return current_user.command_tags_created


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
) -> CommandTag:
    return __db.command_tag.read_personal(
        id, current_user.command_tags_created
    )


@router.delete(__db.prefix(id=True), tags=__db.tags, summary=__summary.DELETE)
async def delete(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=__db.allowed_roles_ids))
    ],
    id: int,
) -> Result:
    __db.command_tag.read_personal(
        id,
        current_user.command_tags_created,
    )
    return __db.command_tag.delete(id)
