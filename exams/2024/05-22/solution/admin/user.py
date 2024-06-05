from typing import Annotated, List

from auth import RoleChecker
from fastapi import Depends, HTTPException, status
from model import Result, User, engine
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from . import router


@router.post("/user", tags=["User"], summary="Create a new user")
async def admin_create_user(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin"]))
    ],
    user: User,
    created: bool = True,
) -> Result[User]:
    try:
        with Session(engine) as session:
            try:
                if created:
                    user.created_by_id = current_user.id
                else:
                    user.updated_by_id = current_user.id
                session.add(user)
                session.commit()
                session.refresh(user)
                return Result(
                    f"User {user.id} "
                    f"{'created' if created else 'updated'}",
                    data=user,
                )
            except IntegrityError as ie:
                raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, str(ie))
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))


@router.get("/user", tags=["User"], summary="Get all the users")
async def admin_read_users(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin"]))
    ]
) -> List[User]:
    return admin_read_user(current_user)


@router.get(
    "/user/{user_id}", tags=["User"], summary="Get the details of a user"
)
async def admin_read_user(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin"]))
    ],
    user_id: str = None,
) -> User:
    try:
        with Session(engine) as session:
            if user_id is not None:
                user = session.exec(
                    select(User).where(User.id == user_id)
                ).one_or_none
                if user is None:
                    raise HTTPException(
                        status.HTTP_404_NOT_FOUND, f"User {user_id} not found."
                    )
                return user
            else:
                return session.exec(select(User)).all()
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))


@router.put("/user", tags=["User"], summary="Update a user")
async def admin_update_user(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin", "user"]))
    ],
    user: User,
) -> Result[User]:
    try:
        admin_read_user(current_user, user.id)
        admin_create_user(current_user, user, created=False)
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))


@router.delete("/user/{user_id}", tags=["User"], summary="Delete a user")
async def admin_delete_user(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin"]))
    ],
    user_id: str,
) -> User:
    try:
        with Session(engine) as session:
            user = admin_read_user(current_user, user_id)
            session.delete(user)
            session.commit()
            return Result(f"User {id} deleted", data=user)
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))
