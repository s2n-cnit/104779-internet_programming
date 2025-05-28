from enum import Enum
from typing import Annotated

from auth import RoleChecker
from db import DB
from fastapi import Depends
from model import Result, User, UserPublic

from . import router


class __db:
    tags = ["Me - User"]
    user = DB[User](User, "User")
    allowed_roles_ids = ["admin", "user"]

    def prefix(id: bool = False, created: bool = False, updated: bool = False):
        return (
            "/"
            + ("/{id}" if id else "")
            + ("/{created}" if created else "")
            + ("/{updated}" if updated else "")
        )


class __summary(str, Enum):
    READ = "Get my details"
    DELETE = "Remove my account"


@router.get(__db.prefix(), tags=__db.tags, summary=__summary.READ)
async def read(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=__db.allowed_roles_ids))
    ],
) -> UserPublic:
    return current_user


@router.delete(__db.prefix(), tags=__db.tags, summary=__summary.DELETE)
async def delete(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=__db.allowed_roles_ids))
    ],
) -> Result:
    return __db.user.delete(current_user.id)
