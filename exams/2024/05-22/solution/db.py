from typing import List, Self, Type

from fastapi import HTTPException, status
from model import Result, User, engine
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, SQLModel, select


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
                    print(type(obj))
                    obj.created_by_id = user.id
                    session.add(obj)
                    session.commit()
                    session.refresh(obj)
                    return Result(f"{self.model_text} {obj.id} created")
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

    def read(self: Self, id: str) -> ModelType:
        try:
            with Session(engine) as session:
                book_db = session.get(self.model_type, id)
                if not book_db:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"{self.model_text} {id} not found",
                    )
        except Exception as e:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))

    def update(self: Self, model: ModelType, user: User) -> ModelType:
        try:
            with Session(engine) as session:
                model = self.read(id)
                model_data = model.model_dump(exclude_unset=True)
                for key, value in model_data.items():
                    setattr(model, key, value)
                model.updated_by_id = user.id
                session.add(model)
                session.commit()
                session.refresh(model)
                return Result(f"{self.model_text} {id} updated")
        except Exception as e:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))

    def delete(self: Self, id: str) -> Result:
        try:
            with Session(engine) as session:
                model = self.read(id)
                session.delete(model)
                session.commit()
                return Result(f"{self.model_text} {id} deleted")
        except Exception as e:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))

    def read_personal(self: Self, id: str, db) -> ModelType:
        data = list(filter(lambda item: item.id == id, db))
        if len(data) == 0:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                f"{self.model_text} {id} not found",
            )
        return data[0]
