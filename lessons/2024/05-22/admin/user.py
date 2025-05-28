from typing import Annotated, List

from auth import RoleChecker
from fastapi import Depends, HTTPException, status
from model import Result, User, engine
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from . import router


@router.post("/user", tags=["User"], summary="Create a new user")
async def create_user(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin"]))
    ],
    user: User,
) -> Result[User]:
    try:
        with Session(engine) as session:
            try:
                session.add(user)
                session.commit()
                session.refresh(user)
                return Result(f"User {user.id} created", data=user)
            except IntegrityError as ie:
                raise HTTPException(
                    status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=str(ie)
                )
    except Exception as e:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/user", tags=["User"], summary="Get all the users")
async def read_users(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin"]))
    ]
) -> List[User]:
    try:
        with Session(engine) as session:
            return session.exec(select(User)).all()
    except Exception as e:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get(
    "/user/{user_id}", tags=["User"], summary="Get the details of a user"
)
async def admin_read_user(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin"]))
    ],
    user_id: str,
) -> User:
    try:
        with Session(engine) as session:
            user = session.exec(
                select(User).where(User.id == user_id)
            ).one_or_none
            if user is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"User {user_id} not found in yacr.",
                )
            return user
    except Exception as e:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.delete("/user/{user_id}", tags=["User"], summary="Delete a user")
async def admin_delete_user(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin"]))
    ],
    user_id: str,
) -> User:
    try:
        with Session(engine) as session:
            user = session.exec(
                select(User).where(User.id == user_id)
            ).one_or_none
            if user is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"User {user_id} not found in yacr.",
                )
            session.delete(user)
            session.commit()
            return Result(detail="User {id} was removed from yacr", data=user)
    except Exception as e:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
