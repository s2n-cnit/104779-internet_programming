from enum import Enum
from typing import Annotated, List

from auth import RoleChecker
from db import DB
from fastapi import Depends
from model import Result, User, UserCreate, UserPublic, UserUpdate

from . import router


class __db:
    tags = ["Admin - User"]
    user = DB[User](User, "User")
    allowed_roles_ids = ["admin"]

    def prefix(id: bool = False):
        return "/user" + ("/{id}" if id else "")


class __summary(str, Enum):
    CREATE = "Insert a new user"
    READ_ALL = "Get all the users"
    READ = "Get the details of a user"
    UPDATE = "Update a user"
    DELETE = "Delete a user"


@router.post(__db.prefix(), tags=__db.tags, summary=__summary.CREATE)
async def create(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=__db.allowed_roles_ids))
    ],
    user: UserCreate,
) -> Result:
    return __db.user.create(user, current_user)


@router.get(__db.prefix(), tags=__db.tags, summary=__summary.READ_ALL)
async def read_all(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=__db.allowed_roles_ids))
    ]
) -> List[UserPublic]:
    return __db.user.read_all()


@router.get(__db.prefix(id=True), tags=__db.tags, summary=__summary.READ)
async def read(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=__db.allowed_roles_ids))
    ],
    id: str,
) -> UserPublic:
    return __db.user.read(id)


@router.put(__db.prefix(id=True), tags=__db.tags, summary=__summary.UPDATE)
async def update(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin", "user"]))
    ],
    id: str,
    user: UserUpdate,
) -> Result:
    return __db.user.update(id, user, current_user)


@router.delete(__db.prefix(id=True), tags=__db.tags, summary=__summary.DELETE)
async def delete(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=__db.allowed_roles_ids))
    ],
    id: str,
) -> Result:
    return __db.user.delete(id)
