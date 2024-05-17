from datetime import datetime
from typing import Type

from app import app
from fastapi import HTTPException, status
from model import Result, ResultType, Room, User, UserRoom, engine
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, SQLModel, select


def joined(room_id: str, user_id: str):
    return f"User {user_id} joined room {room_id}"


def left(room_id: str, user_id: str):
    return f"User {user_id} left room {room_id}"


def not_joined(room_id: str, user_id: str):
    return "User {user_id} not joined room {room_ids}"


@app.post("/user/{user_id}/join/room/{room_id}", tags=["User - Room"])
@app.post("/room/{room_id}/join/user/{user_id}", tags=["User - Room"])
async def join_user(room_id: str, user_id: str) -> Result[UserRoom]:
    try:
        with Session(engine) as session:
            try:
                check_entity(session, User, id)
                check_entity(session, Room, id)
                ur = UserRoom(
                    user_id=user_id, room_id=room_id, join_at=datetime.now()
                )
                session.add(ur)
                session.commit()
                session.refresh(ur)
                return Result(detail=joined(room_id, user_id), data=ur)
            except IntegrityError as ie:
                raise HTTPException(
                    status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=str(ie)
                )
    except Exception as e:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@app.delete("/user/{user_id}/leave/room/{room_id}", tags=["User - Room"])
@app.delete("/room/{room_id}/leave/user/{user_id}", tags=["User - Room"])
async def leave_user(room_id: str, user_id: str) -> Result[UserRoom]:
    try:
        with Session(engine) as session:
            check_entity(session, User, id)
            check_entity(session, Room, id)
            ur = session.exec(
                select(UserRoom).where(
                    UserRoom.room_id == room_id and UserRoom.user_id == user_id
                )
            ).one_or_none()
            if ur is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=not_joined(room_id, user_id),
                )
            else:
                session.delete(ur)
                session.commit()
                return Result(detail=ResultType.DELETED, data=ur)
    except Exception as e:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


def check_entity(
    session: Session, Entity: Type[SQLModel], entity_id: str
) -> None:
    if (
        session.exec(select(Entity).where(Entity.id == id)).one_or_none()
        is None
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ResultType[Entity].NOT_FOUND(id),
        )
