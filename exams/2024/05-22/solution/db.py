from typing import List

from fastapi import HTTPException, status
from model import Result, User, engine
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, SQLModel, select


class DB[Type: SQLModel, text: str]:
    def create(model: Type, user: User) -> Result:
        try:
            with Session(engine) as session:
                try:
                    model.created_by_id = user.id
                    session.add(model)
                    session.commit()
                    session.refresh(model)
                    return Result(f"{text} {model.id} created")
                except IntegrityError as ie:
                    raise HTTPException(
                        status.HTTP_406_NOT_ACCEPTABLE, str(ie)
                    )
        except Exception as e:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))

    def read_all() -> List[Type]:
        try:
            with Session(engine) as session:
                return session.exec(select(Type)).all()
        except Exception as e:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))

    def read(id: str) -> Type:
        try:
            with Session(engine) as session:
                book_db = session.get(Type, id)
                if not book_db:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"{text} {id} not found",
                    )
        except Exception as e:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))

    def update(model: Type, user: User) -> Type:
        try:
            with Session(engine) as session:
                model = DB.read(id)
                model_data = model.model_dump(exclude_unset=True)
                for key, value in model_data.items():
                    setattr(model, key, value)
                model.updated_by_id = user.id
                session.add(model)
                session.commit()
                session.refresh(model)
                return Result(f"{text} {id} updated")
        except Exception as e:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))

    def delete(id: str) -> Result:
        try:
            with Session(engine) as session:
                model = DB.read[Type](id, text)
                session.delete(model)
                session.commit()
                return Result(f"{text} {id} deleted")
        except Exception as e:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))

    def read_personal(id: str, db) -> Type:
        data = list(filter(lambda item: item.id == id, db))
        if len(data) == 0:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                f"{text} {id} not found",
            )
        return data[0]
