from typing import Annotated

from auth import RoleChecker
from db import DB
from fastapi import Depends
from model import Result, User, UserPublic

from . import router

db_user = DB[User](User, "User")


tags = ["Me - User"]


@router.get("/", tags=tags, summary="Get my details")
async def me_get(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin", "user"]))
    ],
) -> UserPublic:
    return current_user


@router.delete("/", tags=tags, summary="Remove my account")
async def me_delete(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin", "user"]))
    ],
) -> Result:
    return db_user.delete(current_user.id)
