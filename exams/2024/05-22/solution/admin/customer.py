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


@router.post("/customer", tags=["Customer"], summary="Insert a new customer")
async def admin_create_customer(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin", "user"]))
    ],
    customer: CustomerCreate,
) -> Result:
    return db_customer.create(customer, current_user)


@router.get("/customer", tags=["Customer"], summary="Get all the customers")
async def admin_read_customers(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin"]))
    ]
) -> List[CustomerPublic]:
    return db_customer.read_all()


@router.get(
    "/customer/{customer_id}",
    tags=["Customer"],
    summary="Get the details of a customer",
)
async def admin_read_customer(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin"]))
    ],
    customer_id: int,
) -> CustomerPublic:
    return db_customer.read(customer_id)


@router.put(
    "/customer/{customer_id}", tags=["Customer"], summary="Update a customer"
)
async def admin_update_customer(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin"]))
    ],
    customer_id: int,
    customer: CustomerUpdate,
) -> Result:
    return db_customer.update(customer, current_user)


@router.delete(
    "/customer/{customer_id}", tags=["Customer"], summary="Delete a customer"
)
async def admin_delete_customer(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin"]))
    ],
    customer_id: int,
) -> Result:
    return db_customer.delete(customer_id)
