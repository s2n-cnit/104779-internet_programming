from typing import Annotated, List

from admin.loan import admin_create_loan
from auth import RoleChecker
from fastapi import Depends, HTTPException, status
from model import Loan, Result, User

from . import router


@router.get(
    "/loan",
    tags=["Loan"],
    summary="Get all the created loans",
)
async def me_read_loans(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin", "user"]))
    ],
) -> List[Loan]:
    return me_read_loan(current_user)


@router.get(
    "/loan/{loan_id}",
    tags=["Loan"],
    summary="Get the details of the loan",
)
async def me_read_loan(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin", "user"]))
    ],
    loan_id: str = None,
) -> List[Loan]:
    if loan_id is None:
        return current_user.loans
    else:
        data = list(
            filter(
                lambda loan: loan.id == loan_id,
                current_user.loans,
            )
        )
        if len(data) == 0:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                f"Loan {loan_id} not found",
            )
        return data[0]


@router.put("/loan", tags=["Loan"], summary="Update a loan")
async def me_update_loan(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin", "user"]))
    ],
    loan: Loan,
) -> Result[Loan]:
    try:
        me_read_loan(current_user, loan.id)
        admin_create_loan(current_user, loan, created=False)
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))
