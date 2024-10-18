from typing import Annotated, Any
from fastapi import APIRouter, HTTPException, Query
from sqlmodel import select

from app import models
from app.db import DB


router = APIRouter(prefix="/books", tags=["books"])


@router.get("/", response_model=list[models.BookPub])
async def get_books(
    db: DB,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> Any:
    books = db.exec(select(models.Book).offset(offset).limit(limit)).all()
    return books


@router.get("/{book_id}", response_model=models.BookPub)
async def get_book(db: DB, book_id: int) -> Any:
    book = db.get(models.Book, book_id)

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    return book


@router.post("/", response_model=models.BookPub)
async def create_book(db: DB, book: models.BookCreate) -> Any:
    db_book = models.Book.model_validate(book)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book


@router.put("/{book_id}", response_model=models.BookPub)
async def update_book(db: DB, book_id: int, book: models.BookUpdate) -> Any:
    db_book = db.get(models.Book, book_id)

    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")

    # could be done better
    book_data = book.model_dump(exclude_unset=True)
    db_book.sqlmodel_update(book_data)

    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book


@router.delete("/{book_id}", response_model=models.BookPub)
async def delete_book(db: DB, book_id: int) -> Any:
    book = db.get(models.Book, book_id)

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    db.delete(book)
    db.commit()

    return book
