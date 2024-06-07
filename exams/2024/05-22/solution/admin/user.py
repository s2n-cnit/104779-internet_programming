from typing import Annotated, List

from auth import RoleChecker
from db import DB
from fastapi import Depends
from model import Result, User, UserCreate, UserUpdate, UserPublic

from . import router

db_user = DB[User](User, "User")


@router.post("/user", tags=["User"], summary="Create a new user")
async def admin_create_user(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin"]))
    ],
    user: UserCreate,
) -> Result:
    return db_user.create(user, current_user)


@router.get("/user", tags=["User"], summary="Get all the users")
async def admin_read_users(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin"]))
    ]
) -> List[UserPublic]:
    return db_user.read_all()


@router.get(
    "/user/{user_id}", tags=["User"], summary="Get the details of a user"
)
async def admin_read_user(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin"]))
    ],
    user_id: str,
) -> UserPublic:
    return db_user.read(user_id)


@router.put("/user/{user_id}", tags=["User"], summary="Update a user")
async def admin_update_user(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin", "user"]))
    ],
    user_id: str,
    user: UserUpdate,
) -> Result:
    return db_user.update(user, current_user)


@router.delete("/user/{user_id}", tags=["User"], summary="Delete a user")
async def admin_delete_user(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin"]))
    ],
    user_id: str,
) -> Result:
    return db_user.delete(user_id)
