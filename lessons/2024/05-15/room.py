from typing import List

from app import app
from fastapi import HTTPException, status
from model import Result, ResultType, Room, engine
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select


@app.post("/room", tags=["Room"])
async def create_room(room: Room) -> Result[Room]:
    try:
        with Session(engine) as session:
            try:
                session.add(room)
                session.commit()
                session.refresh(room)
                return Result(detail=ResultType.CREATED, data=room)
            except IntegrityError as ie:
                raise HTTPException(
                    status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=str(ie)
                )
    except Exception as e:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@app.get("/room", tags=["Room"])
@app.get("/rooms", tags=["Room"])
async def read_rooms() -> List[Room]:
    try:
        with Session(engine) as session:
            return session.exec(select(Room)).all()
    except Exception as e:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@app.get("/room/{id}", tags=["Room"])
async def read_room(id: str) -> Room:
    try:
        with Session(engine) as session:
            room = session.exec(
                select(Room).where(Room.id == id)
            ).one_or_none()
            if room is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=ResultType[Room].NOT_FOUND(id),
                )
            else:
                return room
    except Exception as e:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@app.delete("/room/{id}", tags=["Room"])
async def delete_room(id: str) -> Result[Room]:
    try:
        with Session(engine) as session:
            room = session.exec(
                select(Room).where(Room.id == id)
            ).one_or_none()
            if room is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=ResultType[Room].NOT_FOUND(id),
                )
            else:
                session.delete(room)
                session.commit()
                return Result(detail=ResultType.DELETED, data=room)
    except Exception as e:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
