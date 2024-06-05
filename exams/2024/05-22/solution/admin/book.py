from datetime import datetime
from typing import Annotated, List

from auth import RoleChecker
from fastapi import Depends, HTTPException, status
from model import (
    Book,
    BookCreate,
    BookPublic,
    BookUpdate,
    Result,
    User,
    engine,
)
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from . import router


@router.post("/book", tags=["Book"], summary="Insert a new book")
async def admin_create_book(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin", "user"]))
    ],
    book: BookCreate,
    created: bool = True,
) -> Result[BookPublic]:
    try:
        with Session(engine) as session:
            try:
                if created:
                    book.created_by_id = current_user.id
                else:
                    book.updated_by_id = current_user.id
                session.add(book)
                session.commit()
                session.refresh(book)
                return Result(
                    f"Book {book.id} "
                    f"{'created' if created else 'updated'}",
                    data=book,
                )
            except IntegrityError as ie:
                raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, str(ie))
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))


@router.get("/book", tags=["Book"], summary="Get all the books")
async def admin_read_books(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin"]))
    ]
) -> List[Book]:
    return admin_read_book(current_user)


@router.get(
    "/book/{book_id}", tags=["Book"], summary="Get the details of a book"
)
async def admin_read_book(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin"]))
    ],
    book_id: str = None,
) -> Book:
    try:
        with Session(engine) as session:
            if book_id is not None:
                book = session.exec(
                    select(Book).where(Book.id == book_id)
                ).one_or_none()
                if book is None:
                    raise HTTPException(
                        status.HTTP_404_NOT_FOUND, f"Book {book_id} not found"
                    )
                return book
            else:
                return session.exec(select(Book)).all()
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))


@router.put("/book", tags=["Book"], summary="Update a book")
async def admin_update_book(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin"]))
    ],
    book: Book,
) -> Result[Book]:
    try:
        admin_read_book(current_user, book.id)
        admin_create_book(current_user, book, created=False)
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))


@router.delete("/book/{book_id}", tags=["Book"], summary="Delete a book")
async def admin_delete_book(
    current_user: Annotated[
        User, Depends(RoleChecker(allowed_role_ids=["admin"]))
    ],
    book_id: str,
) -> Result[Book]:
    try:
        with Session(engine) as session:
            book = admin_read_book(current_user, book_id)
            session.delete(book)
            session.commit()
            return Result(f"Book {book_id} deleted", data=book)
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))
