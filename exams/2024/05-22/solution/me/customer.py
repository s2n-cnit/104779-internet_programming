from typing import Annotated, List

from admin.customer import admin_create_customer
from auth import RoleChecker
from fastapi import Depends, HTTPException, status
from model import Customer, Result, User

from . import router


@router.get(
    "/customer",
    tags=["Customer"],
    summary="Get all the created customers",
)
async def me_read_customers(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin", "user"]))
    ],
) -> List[Customer]:
    return me_read_customer(current_user)


@router.get(
    "/customer/{customer_id}",
    tags=["Customer"],
    summary="Get the details of the customer",
)
async def me_read_customer(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin", "user"]))
    ],
    customer_id: str = None,
) -> List[Customer]:
    if customer_id is None:
        return current_user.customers
    else:
        data = list(
            filter(
                lambda customer: customer.id == customer_id,
                current_user.customers,
            )
        )
        if len(data) == 0:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                f"Customer {customer_id} not found",
            )
        return data[0]


@router.put("/customer", tags=["Customer"], summary="Update a customer")
async def me_update_customer(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin", "user"]))
    ],
    customer: Customer,
) -> Result[Customer]:
    try:
        me_read_customer(current_user, customer.id)
        admin_create_customer(current_user, customer, created=False)
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))
