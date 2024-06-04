from typing import Annotated, List

from auth import RoleChecker
from fastapi import Depends, HTTPException, status
from model import Loan, Result, User, engine
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from . import router


@router.post("/loan", tags=["Loan"], summary="Insert a new loan")
async def admin_create_loan(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin", "user"]))
    ],
    loan: Loan,
    created: bool = True,
) -> Result[Loan]:
    try:
        with Session(engine) as session:
            try:
                session.add(loan)
                session.commit()
                session.refresh(loan)
                return Result(
                    f"Loan {loan.id} "
                    f" {'created' if created else 'updated'}",
                    data=loan,
                )
            except IntegrityError as ie:
                raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, str(ie))
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))


@router.get("/loan", tags=["Loan"], summary="Read all loans")
async def admin_read_loans(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin"]))
    ]
) -> List[Loan]:
    return admin_read_loan(current_user)


@router.get(
    "/loan/{loan_id}", tags=["Loan"], summary="Get the details of a loan"
)
async def admin_read_loan(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin"]))
    ],
    loan_id: str = None,
) -> Loan:
    try:
        with Session(engine) as session:
            if loan_id is not None:
                loan = session.exec(
                    select(Loan).where(Loan.id == loan_id)
                ).one_or_none()
                if loan is None:
                    raise HTTPException(
                        status.HTTP_404_NOT_FOUND, f"Loan {loan_id} not found"
                    )
                return loan
            else:
                return session.exec(select(Loan)).all()
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))


@router.put("/loan", tags=["Loan"], summary="Update a loan")
async def admin_update_loan(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin"]))
    ],
    loan: Loan,
) -> Result[Loan]:
    try:
        admin_read_loan(current_user, loan.id)
        admin_create_loan(current_user, loan, created=False)
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))


@router.delete("/loan/{id}", tags=["Loan"], summary="Delete a loan")
async def admin_delete_loan(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin"]))
    ],
    loan_id: str,
) -> Result[Loan]:
    try:
        with Session(engine) as session:
            loan = admin_read_loan(current_user, loan_id)
            session.delete(loan)
            session.commit()
            return Result(f"Loan {loan.id} deleted", data=loan)
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))
