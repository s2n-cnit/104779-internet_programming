from datetime import datetime
from enum import Enum
from typing import Self

from fastapi import Request, status
from fastapi.responses import JSONResponse


class Action(str, Enum):
    NOT_FOUND = "Not Found"
    CONFLICT = "Conflict"


class BaseException(Exception):
    def __init__(self: Self, target: str, id: str | int) -> Self:
        self.target = target
        self.id = id

    def response(self: Self) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=dict(
                action=self.action,
                target=self.target,
                id=self.id,
                error=True,
                success=False,
                # timestamp=datetime.now(), # FIXME not JSON serializable
            ),
        )


async def exception_handler(
    request: Request, exc: BaseException
) -> JSONResponse:
    return exc.response()


class NotFoundException(BaseException):
    action = Action.NOT_FOUND


class ConflictException(BaseException):
    action = Action.CONFLICT
