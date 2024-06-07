from typing import Annotated, List

from auth import RoleChecker
from db import DB
from fastapi import Depends
from model import Loan, LoanPublic, LoanUpdate, Result, User

from . import router

db_loan = DB[Loan](Loan, "Loan")


@router.get(
    "/loan/created",
    tags=["Loan"],
    summary="Get all the created loans",
)
async def me_read_loans_created(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin", "user"]))
    ],
) -> List[LoanPublic]:
    return current_user.loans_created


@router.get(
    "/loan/updated",
    tags=["Loan"],
    summary="Get all the updated loans",
)
async def me_read_loans_updated(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin", "user"]))
    ],
) -> List[LoanPublic]:
    return current_user.loans_updated


@router.get(
    "/loan/{loan_id}",
    tags=["Loan"],
    summary="Get the details of the loan",
)
async def me_read_loan(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin", "user"]))
    ],
    loan_id: str,
) -> LoanPublic:
    return db_loan.read_personal(loan_id, current_user.loans_created)


@router.put("/loan/{loan_id}", tags=["Loan"], summary="Update a loan")
async def me_update_loan(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin", "user"]))
    ],
    loan_id: int,
    loan: LoanUpdate,
) -> Result:
    db_loan.read_personal(loan.id, current_user.loans_created)
    return db_loan.create(loan, current_user)
