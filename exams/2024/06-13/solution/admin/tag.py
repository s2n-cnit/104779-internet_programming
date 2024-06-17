from typing import Annotated, List

from auth import RoleChecker
from db import DB
from fastapi import Depends
from model import Result, Tag, TagCreate, TagPublic, TagUpdate, User

from . import router

db_tag = DB[Tag](Tag, "Tag")

tags = ["Admin - Tag"]


@router.post("/tag", tags=tags, summary="Insert a new tag")
async def admin_create_tag(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin"]))
    ],
    tag: TagCreate,
) -> Result:
    return db_tag.create(tag, current_user)


@router.get("/tag", tags=tags, summary="Get all the tags")
async def admin_read_tags(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin"]))
    ]
) -> List[TagPublic]:
    return db_tag.read_all()


@router.get("/tag/{tag_id}", tags=tags, summary="Get the details of a tag")
async def admin_read_tag(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin"]))
    ],
    tag_id: int,
) -> TagPublic:
    return db_tag.read(tag_id)


@router.put("/tag/{tag_id}", tags=tags, summary="Update a tag")
async def admin_update_tag(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin"]))
    ],
    tag_id: int,
    tag: TagUpdate,
) -> Result:
    return db_tag.update(tag_id, tag, current_user)


@router.delete("/tag/{tag_id}", tags=tags, summary="Delete a tag")
async def admin_delete_tag(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin"]))
    ],
    tag_id: int,
) -> Result:
    return db_tag.delete(tag_id)
