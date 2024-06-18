from enum import Enum
from typing import Annotated, List

from auth import RoleChecker
from db import DB
from fastapi import Depends
from model import Result, Tag, TagCreate, TagPublic, TagUpdate, User

from . import router


class __db:
    tags = ["Me - Tag"]
    tag = DB[Tag](Tag, "Tag")
    allowed_roles_ids = ["admin", "user"]

    def prefix(id: bool = False, created: bool = False, updated: bool = False):
        return (
            "/tag"
            + ("/{id}" if id else "")
            + ("/{created}" if created else "")
            + ("/{updated}" if updated else "")
        )


class __summary(str, Enum):
    CREATE = "Insert a new tag"
    READ_ALL_CREATED = "Get all the created tags"
    READ_ALL_UPDATED = "Get all the updated tags"
    READ = "Get the details of a tag"
    UPDATE = "Update a tag"


@router.post(__db.prefix(), tags=__db.tags, summary="Insert a new tag")
async def create(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=__db.allowed_roles_ids))
    ],
    tag: TagCreate,
) -> Result:
    return __db.tag.create(tag, current_user)


@router.get(
    __db.prefix(created=True),
    tags=__db.tags,
    summary=__summary.READ_ALL_CREATED,
)
async def read_all_created(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=__db.allowed_roles_ids))
    ],
) -> List[TagPublic]:
    return current_user.tags_created


@router.get(
    __db.prefix(updated=True),
    tags=__db.tags,
    summary=__summary.READ_ALL_UPDATED,
)
async def read_all_updated(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=__db.allowed_roles_ids))
    ],
) -> List[TagPublic]:
    return current_user.tags_updated


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
) -> TagPublic:
    return db_tag.read_personal(id, current_user.tags_created)


@router.put(__db.prefix(id=True), tags=__db.tags, summary=__summary.UPDATE)
async def me_update_tag(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=__db.allowed_roles_ids))
    ],
    id: int,
    tag: TagUpdate,
) -> Result:
    __db.tag.read_personal(id, current_user.tags_created)
    return __db.tag.update(id, tag, current_user)
