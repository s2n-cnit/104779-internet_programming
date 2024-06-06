from typing import Annotated, List

from auth import RoleChecker
from db import DB
from fastapi import Depends
from model import Loan, LoanPublic, Result, User

from . import router

db_loan = DB[Loan, "Loan"]


@router.get(
    "/loan",
    tags=["Loan"],
    summary="Get all the created loans",
)
async def me_read_loans(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin", "user"]))
    ],
) -> List[LoanPublic]:
    return current_user.loans


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
) -> List[LoanPublic]:
    return db_loan.read_personal(loan_id, current_user.loans)


@router.put("/loan", tags=["Loan"], summary="Update a loan")
async def me_update_loan(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin", "user"]))
    ],
    loan: Loan,
) -> Result:
    db_loan.read_personal(loan.id, current_user.loans)
    return db_loan.create(loan, current_user)
