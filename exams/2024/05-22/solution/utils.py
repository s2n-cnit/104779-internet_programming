from typing import Type

from fastapi import HTTPException, status
from model import ResultType
from sqlmodel import Session, SQLModel, select


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
