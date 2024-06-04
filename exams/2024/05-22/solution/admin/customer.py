from typing import Annotated, List

from auth import RoleChecker
from fastapi import Depends, HTTPException, status
from model import Customer, Result, User, engine
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from . import router


@router.post("/customer", tags=["Customer"], summary="Insert a new customer")
async def admin_create_customer(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin", "user"]))
    ],
    customer: Customer,
    created: bool = True,
) -> Result[Customer]:
    try:
        with Session(engine) as session:
            try:
                session.add(customer)
                session.commit()
                session.refresh(customer)
                return Result(
                    f"Customer {customer.id} "
                    f"{'created' if created else 'updated'}",
                    data=customer,
                )
            except IntegrityError as ie:
                raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, str(ie))
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))


@router.get("/customer", tags=["Customer"], summary="Get all the customers")
async def admin_read_customers(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin"]))
    ]
) -> List[Customer]:
    return admin_read_customers(current_user)


@router.get(
    "/customer/{customer_id}",
    tags=["Customer"],
    summary="Get the details of a customer",
)
async def admin_read_customer(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin"]))
    ],
    customer_id: str = None,
) -> Customer:
    try:
        with Session(engine) as session:
            if customer_id is not None:
                customer = session.exec(
                    select(Customer).where(Customer.id == customer_id)
                ).one_or_none
                if customer is None:
                    raise HTTPException(
                        status.HTTP_404_NOT_FOUND,
                        f"Customer {customer_id} not found",
                    )
                return customer
            else:
                return session.exec(select(Customer)).all()
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))


@router.put("/customer", tags=["Customer"], summary="Update a customer")
async def admin_update_customer(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin"]))
    ],
    customer: Customer,
) -> Result[Customer]:
    try:
        admin_read_customer(current_user, customer.id)
        admin_create_customer(current_user, customer, created=False)
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))


@router.delete(
    "/customer/{customer_id}", tags=["Customer"], summary="Delete a customer"
)
async def admin_delete_customer(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin"]))
    ],
    customer_id: str,
) -> Customer:
    try:
        with Session(engine) as session:
            customer = admin_read_customer(current_user, customer_id)
            session.delete(customer)
            session.commit()
            return Result("Customer {id} deleted", data=customer)
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))
