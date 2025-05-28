from enum import Enum
from typing import Annotated, List

from auth import RoleChecker
from db import DB
from fastapi import Depends
from model import (
    Category,
    CategoryCreate,
    CategoryPublic,
    CategoryUpdate,
    Result,
    User,
)

from . import router


class __db:
    tags = ["Me - Category"]
    category = DB[Category](Category, "Category")
    allowed_roles_ids = ["admin", "user"]

    def prefix(id: bool = False, created: bool = False, updated: bool = False):
        return (
            "/category"
            + ("/{id}" if id else "")
            + ("/created" if created else "")
            + ("/updated" if updated else "")
        )


class __summary(str, Enum):
    CREATE = "Insert a new category"
    READ_ALL_CREATED = "Get all the created categories"
    READ_ALL_UPDATED = "Get all the updated categories"
    READ = "Get the details of a category"
    UPDATE = "Update a category"


@router.post(__db.prefix(), tags=__db.tags, summary=__summary.CREATE)
async def create(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=__db.allowed_roles_ids))
    ],
    category: CategoryCreate,
) -> Result:
    return __db.category.create(category, current_user)


@router.get(
    __db.prefix(created=True),
    tags=__db.tags,
    summary=__summary.READ_ALL_CREATED,
)
async def read_all_created(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=__db.allowed_roles_ids))
    ],
) -> List[CategoryPublic]:
    return current_user.categories_created


@router.get(
    __db.prefix(updated=True),
    tags=__db.tags,
    summary=__summary.READ_ALL_UPDATED,
)
async def read_all_updated(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=__db.allowed_roles_ids))
    ],
) -> List[CategoryPublic]:
    return current_user.categories_updated


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
) -> CategoryPublic:
    return __db.category.read_personal(id, current_user.categories_created)


@router.put(
    __db.prefix(id=True),
    tags=__db.tags,
    summary=__summary.UPDATE,
)
async def update(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=__db.allowed_roles_ids))
    ],
    id: int,
    category: CategoryUpdate,
) -> Result:
    __db.category.read_personal(id, current_user.categories_created)
    return __db.category.update(id, category, current_user)
