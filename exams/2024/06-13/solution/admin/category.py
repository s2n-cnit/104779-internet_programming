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

db_category = DB[Category](Category, "Category")

tags = ["Admin - Category"]


@router.post("/category", tags=tags, summary="Insert a new category")
async def admin_create_category(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin"]))
    ],
    category: CategoryCreate,
) -> Result:
    return db_category.create(category, current_user)


@router.get("/category", tags=tags, summary="Get all the categories")
async def admin_read_categories(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin"]))
    ]
) -> List[CategoryPublic]:
    return db_category.read_all()


@router.get(
    "/category/{category_id}",
    tags=tags,
    summary="Get the details of a category",
)
async def admin_read_category(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin"]))
    ],
    category_id: int,
) -> CategoryPublic:
    return db_category.read(category_id)


@router.put("/category/{category_id}", tags=tags, summary="Update a category")
async def admin_update_category(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin"]))
    ],
    category_id: int,
    category: CategoryUpdate,
) -> Result:
    return db_category.update(category, current_user)


@router.delete(
    "/category/{category_id}", tags=tags, summary="Delete a category"
)
async def admin_delete_category(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin"]))
    ],
    category_id: int,
) -> Result:
    return db_category.delete(category_id)
