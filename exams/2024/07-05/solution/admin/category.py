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
    tags = ["Admin - Category"]
    category = DB[Category](Category, "Category")
    allowed_roles_ids = ["admin"]

    def prefix(id: bool = False):
        return "/category" + ("/{id}" if id else "")


class __summary(str, Enum):
    CREATE = "Insert a new category"
    READ_ALL = "Get all the categories"
    READ = "Get the details of a category"
    UPDATE = "Update a category"
    DELETE = "Delete a category"


@router.post(__db.prefix(), tags=__db.tags, summary=__summary.CREATE)
async def create(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=__db.allowed_roles_ids))
    ],
    category: CategoryCreate,
) -> Result:
    return __db.category.create(category, current_user)


@router.get(__db.prefix(), tags=__db.tags, summary=__summary.READ_ALL)
async def read_all(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=__db.allowed_roles_ids))
    ]
) -> List[CategoryPublic]:
    return __db.category.read_all()


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
    return __db.category.read(id)


@router.put(__db.prefix(id=True), tags=__db.tags, summary=__summary.UPDATE)
async def update(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=__db.allowed_roles_ids))
    ],
    id: int,
    category: CategoryUpdate,
) -> Result:
    return __db.category.update(id, category, current_user)


@router.delete(__db.prefix(id=True), tags=__db.tags, summary=__summary.DELETE)
async def delete(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=__db.allowed_roles_ids))
    ],
    id: int,
) -> Result:
    return __db.category.delete(id)
