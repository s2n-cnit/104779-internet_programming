from typing import Annotated, List

from auth import RoleChecker
from db import DB
from fastapi import Depends
from model import Result, Tag, TagCreate, TagPublic, TagUpdate, User

from . import router

db_tag = DB[Tag](Tag, "Tag")

tags = ["Me - Tag"]


@router.post("/tag", tags=tags, summary="Insert a new tag")
async def me_create_tag(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin", "user"]))
    ],
    tag: TagCreate,
) -> Result:
    return db_tag.create(tag, current_user)


@router.get(
    "/tag/created",
    tags=tags,
    summary="Get all the created tags",
)
async def me_read_tags_created(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin", "user"]))
    ],
) -> List[TagPublic]:
    return current_user.tags_created


@router.get(
    "/tag/updated",
    tags=tags,
    summary="Get all the updated tags",
)
async def me_read_tags_updated(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin", "user"]))
    ],
) -> List[TagPublic]:
    return current_user.tags_updated


@router.get(
    "/tag/{tag_id}",
    tags=tags,
    summary="Get the details of the tag",
)
async def me_read_tag(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin", "user"]))
    ],
    tag_id: int,
) -> TagPublic:
    return db_tag.read_personal(tag_id, current_user.tags_created)


@router.put("/tag/{tag_id}", tags=tags, summary="Update a tag")
async def me_update_tag(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin", "user"]))
    ],
    tag_id: int,
    tag: TagUpdate,
) -> Result:
    db_tag.read_personal(tag_id, current_user.tags_created)
    return db_tag.update(tag_id, tag, current_user)
