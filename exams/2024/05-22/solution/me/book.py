from typing import Annotated, List

from auth import RoleChecker
from db import DB
from fastapi import Depends
from model import Book, BookCreate, BookPublic, BookUpdate, Result, User

from . import router

db_book = DB[Book](Book, "Book")

tags = ["Me - Book"]


@router.post("/book", tags=tags, summary="Insert a new book")
async def me_create_book(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin", "user"]))
    ],
    book: BookCreate,
) -> Result:
    return db_book.create(book, current_user)


@router.get(
    "/book/created",
    tags=tags,
    summary="Get all the created books",
)
async def me_read_books_created(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin", "user"]))
    ],
) -> List[BookPublic]:
    return current_user.books_created


@router.get(
    "/book/updated",
    tags=tags,
    summary="Get all the updated books",
)
async def me_read_books_updated(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin", "user"]))
    ],
) -> List[BookPublic]:
    return current_user.books_updated


@router.get(
    "/book/{book_id}",
    tags=tags,
    summary="Get the details of the book",
)
async def me_read_book(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin", "user"]))
    ],
    book_id: str,
) -> BookPublic:
    return db_book.read_personal(book_id, current_user.books_created)


@router.put("/book/{book_id}", tags=tags, summary="Update a book")
async def me_update_book(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin", "user"]))
    ],
    book_id: int,
    book: BookUpdate,
) -> Result:
    db_book.read_personal(book.id, current_user.books_created)
    return db_book.create(book, current_user)
