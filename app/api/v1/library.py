from datetime import datetime
from typing import Any
from fastapi import APIRouter, HTTPException, status

from app import constants, models
from app.db import DB

router = APIRouter(prefix="/library", tags=["library"])


@router.post("/loan_book", response_model=models.BookLoansPub)
async def loan_book(db: DB, book_loan: models.BookLoansCreate) -> Any:
    if member := db.get(models.Member, book_loan.member_id):
        if member.outstanding_payment >= constants.MAX_OUTSTANDING_ALLOWED:
            raise HTTPException(
                status_code=status.HTTP_402_PAYMENT_REQUIRED,
                detail="You need to clear previous outstanding dues for book loans.",
            )

        # member is under max outstanding payment allowed, proceed flow
        if book := db.get(models.Book, book_loan.book_id):
            if book.stock < 1:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Book with id: {book_loan.book_id} is out of stock.",
                )

            book.stock -= 1
            db.add(book)

            db_book_loan = models.BookLoans.model_validate(book_loan)
            db.add(db_book_loan)

            db.commit()
            db.refresh(db_book_loan)

            return db_book_loan

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id: {book_loan.book_id} does not exist.",
        )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Member with id: {book_loan.member_id} does not exist.",
    )


@router.put("/return_book")
async def return_book(db: DB, loan_id: int) -> Any:
    if book_loan := db.get(models.BookLoans, loan_id):
        member = db.get(models.Member, book_loan.member_id)
        if not member:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Member with id: {book_loan.member_id} does not exist.",
            )

        book = db.get(models.Book, book_loan.book_id)
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Book with id: {book_loan.book_id} does not exist.",
            )

        member.outstanding_payment += constants.LOAN_CHARGE
        db.add(member)

        book.stock += 1
        db.add(book)

        book_loan.return_date = datetime.now().date()
        db.add(book_loan)

        db.commit()
        db.refresh(book_loan)

        return book_loan

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Book loan with id: {loan_id} does not exist.",
    )