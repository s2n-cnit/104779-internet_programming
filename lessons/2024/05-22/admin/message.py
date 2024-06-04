from typing import Annotated, List

from auth import RoleChecker
from fastapi import Depends, HTTPException, status
from model import Message, Result, User, engine
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from . import router


@router.post("/message", tags=["Message"], summary="Create a new message")
async def admin_create_message(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin"]))
    ],
    message: Message,
) -> Result[Message]:
    try:
        with Session(engine) as session:
            try:
                session.add(message)
                session.commit()
                session.refresh(message)
                return Result(
                    detail=f"Message {message.id} of "
                    "user {user_id} created in room {room_id}",
                    data=message,
                )
            except IntegrityError as ie:
                raise HTTPException(
                    status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=str(ie)
                )
    except Exception as e:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/message", tags=["Message"], summary="Read all messages")
async def admin_read_messages__admin(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin"]))
    ]
) -> List[Message]:
    try:
        with Session(engine) as session:
            return session.exec(select(Message)).all()
    except Exception as e:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.delete("/message/{id}", tags=["Message"], summary="Read a message")
async def admin_delete_message(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin"]))
    ],
    id: str,
) -> Result[Message]:
    try:
        with Session(engine) as session:
            message = session.exec(
                select(Message).where(Message.id == id)
            ).one_or_none()
            if message is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Message {message.id} not found",
                )
            else:
                session.delete(message)
                session.commit()
                return Result(
                    detail=f"Message {message.id} of user {message.user_id} "
                    "deleted from room {message.room_id}",
                    data=message,
                )
    except Exception as e:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
