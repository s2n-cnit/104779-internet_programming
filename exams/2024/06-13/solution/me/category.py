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

tags = ["Me - Category"]


@router.post("/category", tags=tags, summary="Insert a new category")
async def admin_create_category(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin", "user"]))
    ],
    category: CategoryCreate,
) -> Result:
    return db_category.create(category, current_user)


@router.get(
    "/category/created",
    tags=tags,
    summary="Get all the created categories",
)
async def me_read_categories_created(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin", "user"]))
    ],
) -> List[CategoryPublic]:
    return current_user.categories_created


@router.get(
    "/category/updated",
    tags=tags,
    summary="Get all the updated categories",
)
async def me_read_categories_updated(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin", "user"]))
    ],
) -> List[CategoryPublic]:
    return current_user.categories_updated


@router.get(
    "/category/{category_id}",
    tags=tags,
    summary="Get the details of the category",
)
async def me_read_category(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin", "user"]))
    ],
    category_id: int,
) -> CategoryPublic:
    return db_category.read_personal(
        category_id, current_user.categories_created
    )


@router.put(
    "/category/{category_id}",
    tags=tags,
    summary="Update a category",
)
async def me_update_category(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin", "user"]))
    ],
    category_id: int,
    category: CategoryUpdate,
) -> Result:
    db_category.read_personal(category_id, current_user.categories_created)
    return db_category.update(category_id, category, current_user)
