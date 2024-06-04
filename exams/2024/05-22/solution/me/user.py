from typing import Annotated, List

from auth import RoleChecker
from fastapi import Depends, HTTPException, status
from model import Result, User, engine
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from . import router


@router.get("/", tags=["User"], summary="Get my details")
async def me_get(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin", "user"]))
    ],
) -> User:
    return current_user


@router.delete("/", tags=["User"], summary="Remove my account")
async def me_delete(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin", "user"]))
    ],
) -> User:
    try:
        with Session(engine) as session:
            session.delete(current_user)
            session.commit()
            return Result(detail="You was removed", data=current_user)
    except Exception as e:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
