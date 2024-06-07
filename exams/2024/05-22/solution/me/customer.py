from typing import Annotated, List

from auth import RoleChecker
from db import DB
from fastapi import Depends
from model import (
    Customer,
    CustomerCreate,
    CustomerPublic,
    CustomerUpdate,
    Result,
    User,
)

from . import router

db_customer = DB[Customer](Customer, "Customer")

tags = ["Me - Customer"]


@router.post("/customer", tags=tags, summary="Insert a new customer")
async def admin_create_customer(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin", "user"]))
    ],
    customer: CustomerCreate,
) -> Result:
    return db_customer.create(customer, current_user)


@router.get(
    "/customer/created",
    tags=tags,
    summary="Get all the created customers",
)
async def me_read_customers_created(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin", "user"]))
    ],
) -> List[CustomerPublic]:
    return current_user.customers_created


@router.get(
    "/customer/updated",
    tags=tags,
    summary="Get all the updated customers",
)
async def me_read_customers_updated(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin", "user"]))
    ],
) -> List[CustomerPublic]:
    return current_user.customers_updated


@router.get(
    "/customer/{customer_id}",
    tags=tags,
    summary="Get the details of the customer",
)
async def me_read_customer(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin", "user"]))
    ],
    customer_id: str,
) -> CustomerPublic:
    return db_customer.read_personal(
        customer_id, current_user.customers_created
    )


@router.put(
    "/customer/{customer_id}",
    tags=tags,
    summary="Update a customer",
)
async def me_update_customer(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin", "user"]))
    ],
    customer_id: int,
    customer: CustomerUpdate,
) -> Result:
    db_customer.read_personal(customer.id, current_user.customers_created)
    return db_customer.create(customer, current_user)
