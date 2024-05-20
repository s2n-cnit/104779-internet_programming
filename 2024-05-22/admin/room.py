from typing import Annotated, List

from auth import get_current_active_user
from fastapi import HTTPException, Security, status
from model import Result, Room, User, engine
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from . import router


@router.post("/room", tags=["Room"], summary="Create a new chat room")
async def admin_create_room(
    current_user: Annotated[
        User, Security(get_current_active_user, scopes=["admin"])
    ],
    room: Room,
) -> Result[Room]:
    try:
        with Session(engine) as session:
            try:
                session.add(room)
                session.commit()
                session.refresh(room)
                return Result(f"Room {room.id} created", data=room)
            except IntegrityError as ie:
                raise HTTPException(
                    status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=str(ie)
                )
    except Exception as e:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/room", tags=["Room"], summary="Get all the rooms")
async def admin_read_rooms(
    current_user: Annotated[
        User, Security(get_current_active_user, scopes=["admin"])
    ]
) -> List[Room]:
    try:
        with Session(engine) as session:
            return session.exec(select(Room)).all()
    except Exception as e:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get(
    "/room/{room_id}", tags=["Room"], summary="Get the details of a room"
)
async def admin_read_room(
    current_user: Annotated[
        User, Security(get_current_active_user, scopes=["admin"])
    ],
    room_id: str,
) -> Room:
    try:
        with Session(engine) as session:
            room = session.exec(
                select(Room).where(Room.id == room_id)
            ).one_or_none()
            if room is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Room {room_id} not found",
                )
            else:
                return room
    except Exception as e:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.delete("/room/{room_id}", tags=["Room"], summary="Delete a room")
async def admin_delete_room(
    current_user: Annotated[
        User, Security(get_current_active_user, scopes=["admin"])
    ],
    room_id: str,
) -> Result[Room]:
    try:
        with Session(engine) as session:
            room = session.exec(
                select(Room).where(Room.id == room_id)
            ).one_or_none()
            if room is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Room {room_id} not found",
                )
            else:
                session.delete(room)
                session.commit()
                return Result(f"Room {room_id} deleted", data=room)
    except Exception as e:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
