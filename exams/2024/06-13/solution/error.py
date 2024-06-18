from datetime import datetime
from typing import Self

from fastapi import Request, status
from fastapi.responses import JSONResponse


class NotFoundException(Exception):
    def __init__(self: Self, target: str, id: str | int) -> Self:
        self.target = target
        self.id = id


async def not_found_exception_handler(
    request: Request, exc: NotFoundException
):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=dict(
            action="Not Found",
            target=exc.target,
            id=exc.id,
            error=True,
            success=False,
            # timestamp=datetime.now(), # FIXME not JSON serializable
        ),
    )
