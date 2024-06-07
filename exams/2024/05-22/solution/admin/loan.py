from typing import Annotated, List

from auth import RoleChecker
from db import DB
from fastapi import Depends
from model import Loan, LoanPublic, LoanUpdate, LoanCreate, Result, User

from . import router

db_loan = DB[Loan](Loan, "Loan")


@router.post("/loan", tags=["Loan"], summary="Insert a new loan")
async def admin_create_loan(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin", "user"]))
    ],
    loan: LoanCreate,
) -> Result:
    return db_loan.create(loan, current_user)


@router.get("/loan", tags=["Loan"], summary="Read all loans")
async def admin_read_loans(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin"]))
    ]
) -> List[LoanPublic]:
    return db_loan.read_all()


@router.get(
    "/loan/{loan_id}", tags=["Loan"], summary="Get the details of a loan"
)
async def admin_read_loan(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin"]))
    ],
    loan_id: int,
) -> LoanPublic:
    return db_loan.read(loan_id)


@router.put("/loan/{loan_id}", tags=["Loan"], summary="Update a loan")
async def admin_update_loan(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin"]))
    ],
    loan_id: int,
    loan: LoanUpdate,
) -> Result:
    return db_loan.update(loan, current_user)


@router.delete("/loan/{loan_id}", tags=["Loan"], summary="Delete a loan")
async def admin_delete_loan(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin"]))
    ],
    loan_id: int,
) -> Result:
    return db_loan.delete(loan_id)
