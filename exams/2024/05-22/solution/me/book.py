from typing import Annotated, List

from admin.book import admin_create_book
from auth import RoleChecker
from fastapi import Depends, HTTPException, status
from model import Book, Result, User

from . import router


@router.get(
    "/book",
    tags=["Book"],
    summary="Get all the created books",
)
async def me_read_books(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin", "user"]))
    ],
) -> List[Book]:
    return me_read_book(current_user)


@router.get(
    "/book/{book_id}",
    tags=["Book"],
    summary="Get the details of the book",
)
async def me_read_book(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin", "user"]))
    ],
    book_id: str = None,
) -> List[Book]:
    if book_id is None:
        return current_user.books
    else:
        data = list(
            filter(lambda book: book.id == book_id, current_user.books)
        )
        if len(data) == 0:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                f"Book {book_id} not found",
            )
        return data[0]


@router.put("/book", tags=["Book"], summary="Update a book")
async def me_update_book(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin", "user"]))
    ],
    book: Book,
) -> Result[Book]:
    try:
        me_read_book(current_user, book.id)
        admin_create_book(current_user, book, created=False)
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))
