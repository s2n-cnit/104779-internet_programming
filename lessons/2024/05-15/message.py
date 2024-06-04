from typing import List

from app import app
from fastapi import HTTPException, status
from model import Message, Result, ResultType, engine
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select


@app.post("/message", tags=["Message"])
async def create_message(message: Message) -> Result[Message]:
    try:
        with Session(engine) as session:
            try:
                session.add(message)
                session.commit()
                session.refresh(message)
                return Result(detail=ResultType.CREATED, data=message)
            except IntegrityError as ie:
                raise HTTPException(
                    status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=str(ie)
                )
    except Exception as e:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@app.get("/message", tags=["Message"])
@app.get("/messages", tags=["Message"])
async def read_messages() -> List[Message]:
    try:
        with Session(engine) as session:
            return session.exec(select(Message)).all()
    except Exception as e:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@app.get("/message/{id}", tags=["Message"])
async def read_message(id: str) -> Message:
    try:
        with Session(engine) as session:
            message = session.exec(
                select(Message).where(Message.id == id)
            ).one_or_none()
            if message is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Message with id={id} not found",
                )
            else:
                return message
    except Exception as e:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@app.delete("/message/{id}", tags=["Message"])
async def delete_message(id: str) -> Result[Message]:
    try:
        with Session(engine) as session:
            message = session.exec(
                select(Message).where(Message.id == id)
            ).one_or_none()
            if message is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=ResultType[Message].NOT_FOUND(id),
                )
            else:
                session.delete(message)
                session.commit()
                return Result(detail=ResultType.DELETED, data=message)
    except Exception as e:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
