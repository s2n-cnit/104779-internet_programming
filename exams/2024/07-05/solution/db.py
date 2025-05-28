from enum import Enum
from typing import List, Self, Type

from error import NotFoundException
from fastapi import HTTPException, status
from model import Result, User, engine
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, SQLModel, select


class Action(str, Enum):
    CREATED = "Created"
    UPDATED = "Updated"
    DELETED = "Deleted"
    STARTED = "Started"
    STOPPED = "Stopped"


class DB[ModelType: SQLModel]:
    def __init__(self: Self, model_type: Type[ModelType], model_text: str):
        self.model_type = model_type
        self.model_text = model_text

    def create(self: Self, model: ModelType, user: User) -> Result:
        try:
            with Session(engine) as session:
                try:
                    obj = self.model_type(
                        **model.model_dump(exclude_unset=True)
                    )
                    obj.created_by_id = user.id
                    session.add(obj)
                    session.commit()
                    session.refresh(obj)
                    return Result(
                        action=Action.CREATED,
                        target=self.model_text,
                        id=obj.id,
                    )
                except IntegrityError as ie:
                    raise HTTPException(
                        status.HTTP_406_NOT_ACCEPTABLE, str(ie)
                    )
        except Exception as e:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))

    def read_all(self: Self) -> List[ModelType]:
        try:
            with Session(engine) as session:
                return session.exec(select(self.model_type)).unique().all()
        except Exception as e:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))

    def read(self: Self, id: str | int) -> ModelType:
        with Session(engine) as session:
            try:
                db = session.get(self.model_type, id)
            except Exception as e:
                raise HTTPException(
                    status.HTTP_500_INTERNAL_SERVER_ERROR, str(e)
                )
            if not db:
                raise NotFoundException(
                    target=self.model_text,
                    id=id,
                )
            return db

    def update(
        self: Self, id: str | int, model: ModelType, user: User
    ) -> ModelType:
        model_db = self.read(id)
        with Session(engine) as session:
            try:
                model_data = model.model_dump(exclude_unset=True)
                for key, value in model_data.items():
                    setattr(model_db, key, value)
                model_db.updated_by_id = user.id
            except Exception as e:
                raise HTTPException(
                    status.HTTP_500_INTERNAL_SERVER_ERROR, str(e)
                )
            if hasattr(model_db, "additional_updates") and callable(
                model_db.additional_updates
            ):
                model_db.additional_updates()
            try:
                session.add(model_db)
                session.commit()
                session.refresh(model_db)
                return Result(
                    action=Action.UPDATED, target=self.model_text, id=id
                )
            except Exception as e:
                raise HTTPException(
                    status.HTTP_500_INTERNAL_SERVER_ERROR, str(e)
                )

    def delete(self: Self, id: str | int) -> Result:
        model = self.read(id)
        try:
            with Session(engine) as session:
                session.delete(model)
                session.commit()
                return Result(
                    action=Action.DELETED, target=self.model_text, id=id
                )
        except Exception as e:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))

    def read_personal(self: Self, id: str | int, db) -> ModelType:
        data = list(filter(lambda item: item.id == id, db))
        if len(data) == 0:
            raise NotFoundException(target=self.model_text, id=id)
        return data[0]
