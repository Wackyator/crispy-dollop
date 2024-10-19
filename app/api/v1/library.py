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
        if _ := db.get(
            models.Book, book_loan.book_id
        ):  # purely a sanity check to see if book exists
            # assuming the member has fetched book to loan, so it's available in the library?
            # kinda dodgy, maybe book table should probably have total_stock and available_stock fields
            # or maybe a book_stock table with isbn and one-to-many to book table?
            # but oh well, here we go
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

        # this value is not being utilised anywhere and is purely for sanity check
        book = db.get(models.Book, book_loan.book_id)
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Book with id: {book_loan.book_id} does not exist.",
            )

        member.outstanding_payment += constants.LOAN_CHARGE
        db.add(member)

        book_loan.return_date = datetime.now().date()
        db.add(book_loan)

        db.commit()
        db.refresh(book_loan)

        return book_loan

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Book loan with id: {loan_id} does not exist.",
    )
