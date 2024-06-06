from typing import Annotated, List

from auth import RoleChecker
from db import DB
from fastapi import Depends
from model import Customer, CustomerPublic, Result, User

from . import router

db_customer = DB[Customer, "Customer"]


@router.get(
    "/customer",
    tags=["Customer"],
    summary="Get all the created customers",
)
async def me_read_customers(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin", "user"]))
    ],
) -> List[CustomerPublic]:
    return current_user.customers


@router.get(
    "/customer/{customer_id}",
    tags=["Customer"],
    summary="Get the details of the customer",
)
async def me_read_customer(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin", "user"]))
    ],
    customer_id: str,
) -> List[CustomerPublic]:
    return db_customer.read_personal(customer_id, current_user.customers)


@router.put("/customer", tags=["Customer"], summary="Update a customer")
async def me_update_customer(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin", "user"]))
    ],
    customer: Customer,
) -> Result:
    db_customer.read_personal(customer.id, current_user.customers)
    return db_customer.create(customer, current_user)
