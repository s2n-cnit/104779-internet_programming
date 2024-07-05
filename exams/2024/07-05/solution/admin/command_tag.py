from enum import Enum
from typing import Annotated, List

from auth import RoleChecker
from db import DB
from fastapi import Depends
from model import Command, CommandTag, Result, Tag, User

from . import router


class __db:
    tags = ["Admin - Command / Tag"]
    command_tag = DB[CommandTag](CommandTag, "CommandTag")
    command = DB[Command](Command, "Command")
    tag = DB[Tag](Tag, "Tag")
    allowed_roles_ids = ["admin"]

    def prefix(id: bool = False):
        return "/command-tag" + ("/{id}" if id else "")


class __summary(str, Enum):
    CREATE = "Add a new tag to the command"
    READ_ALL = "Get all the command - tag relationships"
    READ = "Get the details of a command - tag relationship"
    DELETE = "Remove a tag from the command"


@router.post(__db.prefix(), tags=__db.tags, summary=__summary.CREATE)
async def create(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=__db.allowed_roles_ids))
    ],
    command_tag: CommandTag,
) -> Result:
    __db.command.read(command_tag.command_id)
    __db.tag.read(command_tag.tag_id)
    return __db.command_tag.create(command_tag, current_user)


@router.get(__db.prefix(), tags=__db.tags, summary=__summary.READ_ALL)
async def read_all(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=__db.allowed_roles_ids))
    ]
) -> List[CommandTag]:
    return __db.command_tag.read_all()


@router.get(__db.prefix(id=True), tags=__db.tags, summary=__summary.READ)
async def read(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=__db.allowed_roles_ids))
    ],
    id: int,
) -> CommandTag:
    return __db.command_tag.read(id)


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
    __db.command_tag.read(id)
    return __db.command_tag.delete(id)
