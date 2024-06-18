from enum import Enum
from typing import Annotated, List

from auth import RoleChecker
from db import DB
from fastapi import Depends
from model import Result, Tag, TagCreate, TagPublic, TagUpdate, User

from . import router


class __db:
    tags = ["Admin - Tag"]
    tag = DB[Tag](Tag, "Tag")
    allowed_roles_ids = ["admin"]

    def prefix(id: bool = False):
        return "/tag" + ("/{id}" if id else "")


class __summary(str, Enum):
    CREATE = "Insert a new tag"
    READ_ALL = "Get all the tags"
    READ = "Get the details of a tag"
    UPDATE = "Update a tag"
    DELETE = "Delete a tag"


@router.post(__db.prefix(), tags=__db.tags, summary=__summary.CREATE)
async def create(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=__db.allowed_roles_ids))
    ],
    tag: TagCreate,
) -> Result:
    return __db.tag.create(tag, current_user)


@router.get("/tag", tags=__db.tags, summary=__summary.READ_ALL)
async def read_all(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=__db.allowed_roles_ids))
    ]
) -> List[TagPublic]:
    return __db.tag.read_all()


@router.get(__db.prefix(id=True), tags=__db.tags, summary=__summary.READ)
async def read(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=__db.allowed_roles_ids))
    ],
    id: int,
) -> TagPublic:
    return __db.tag.read(id)


@router.put(__db.prefix(id=True), tags=__db.tags, summary=__summary.UPDATE)
async def update(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=__db.allowed_roles_ids))
    ],
    id: int,
    tag: TagUpdate,
) -> Result:
    return __db.tag.update(id, tag, current_user)


@router.delete(__db.prefix(id=True), tags=__db.tags, summary=__summary.DELETE)
async def delete(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin"]))
    ],
    id: int,
) -> Result:
    return __db.tag.delete(id)
