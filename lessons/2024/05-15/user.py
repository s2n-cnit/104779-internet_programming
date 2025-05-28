from typing import List

from app import app
from fastapi import HTTPException, status
from model import Result, ResultType, User, engine
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select


@app.post("/user", tags=["User"])
async def create_user(user: User) -> Result[User]:
    try:
        with Session(engine) as session:
            try:
                session.add(user)
                session.commit()
                session.refresh(user)
                return Result(detail=ResultType.CREATED, data=user)
            except IntegrityError as ie:
                raise HTTPException(
                    status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=str(ie)
                )
    except Exception as e:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@app.get("/user", tags=["User"])
@app.get("/users", tags=["User"])
async def read_users() -> List[User]:
    try:
        with Session(engine) as session:
            return session.exec(select(User)).all()
    except Exception as e:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@app.get("/user/{id}", tags=["User"])
async def read_user(id: str) -> User:
    try:
        with Session(engine) as session:
            user = session.exec(
                select(User).where(User.id == id)
            ).one_or_none()
            if user is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=ResultType[User].NOT_FOUND(id),
                )
            else:
                return user
    except Exception as e:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@app.delete("/user/{id}", tags=["User"])
async def delete_user(id: str) -> Result[User]:
    try:
        with Session(engine) as session:
            user = session.exec(
                select(User).where(User.id == id)
            ).one_or_none()
            if user is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=ResultType[User].NOT_FOUND(id),
                )
            else:
                session.delete(user)
                session.commit()
                return Result(detail=ResultType.DELETED, data=user)
    except Exception as e:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
