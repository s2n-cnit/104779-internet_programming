from typing import List

from app import app
from fastapi import HTTPException, status
from model import Message, engine
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select


@app.post("/message")
async def create_message(message: Message) -> Message:
    try:
        with Session(engine) as session:
            try:
                session.add(message)
                session.commit()
                session.refresh(message)
                return message
            except IntegrityError as ie:
                raise HTTPException(
                    status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=str(ie)
                )
    except Exception as e:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@app.get("/messages/")
async def read_messages() -> List[Message]:
    try:
        with Session(engine) as session:
            return session.exec(select(Message)).all()
    except Exception as e:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@app.get("/messages/{id}")
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


@app.delete("/messages/{id}")
async def delete_message(id: str) -> Message:
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
                session.delete(message)
                session.commit()
    except Exception as e:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
