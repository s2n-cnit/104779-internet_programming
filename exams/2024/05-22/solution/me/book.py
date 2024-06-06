from typing import Annotated, List

from auth import RoleChecker
from db import DB
from fastapi import Depends
from model import Book, BookPublic, Result, User

from . import router

db_book = DB[Book, "Book"]


@router.get(
    "/book",
    tags=["Book"],
    summary="Get all the created books",
)
async def me_read_books(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin", "user"]))
    ],
) -> List[BookPublic]:
    return current_user.books


@router.get(
    "/book/{book_id}",
    tags=["Book"],
    summary="Get the details of the book",
)
async def me_read_book(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin", "user"]))
    ],
    book_id: str,
) -> List[BookPublic]:
    return db_book.read_personal(book_id, current_user.books)


@router.put("/book", tags=["Book"], summary="Update a book")
async def me_update_book(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin", "user"]))
    ],
    book: Book,
) -> Result:
    db_book.read_personal(book.id, current_user.books)
    return db_book.create(book, current_user)
