from typing import Annotated, List

from auth import RoleChecker
from db import DB
from fastapi import Depends
from model import Book, BookCreate, BookPublic, BookUpdate, Result, User

from . import router

db_book = DB[Book](Book, "Book")


@router.post("/book", tags=["Book"], summary="Insert a new book")
async def admin_create_book(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin", "user"]))
    ],
    book: BookCreate,
) -> Result:
    return db_book.create(book, current_user)


@router.get("/book", tags=["Book"], summary="Get all the books")
async def admin_read_books(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin"]))
    ]
) -> List[BookPublic]:
    return db_book.read_all()


@router.get(
    "/book/{book_id}", tags=["Book"], summary="Get the details of a book"
)
async def admin_read_book(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin"]))
    ],
    book_id: int,
) -> BookPublic:
    return db_book.read(book_id)


@router.put("/book/{book_id}", tags=["Book"], summary="Update a book")
async def admin_update_book(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin"]))
    ],
    book_id: int,
    book: BookUpdate,
) -> Result:
    return db_book.update(book, current_user)


@router.delete("/book/{book_id}", tags=["Book"], summary="Delete a book")
async def admin_delete_book(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin"]))
    ],
    book_id: int,
) -> Result:
    return db_book.delete(book_id)
