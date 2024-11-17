from datetime import datetime
from fastapi import HTTPException, status
from sqlmodel import SQLModel
from app import constants, models
from app.crud.base import CRUDBase
from app.db import DB
from app.models.library import BookLoans, BookLoansCreate


class CRUDBookLoans(CRUDBase):
    def get_inner(self) -> type[SQLModel]:
        return BookLoans

    def create(self, db: DB, create_obj: BookLoansCreate, commit: bool = True, *args, **kwargs) -> BookLoans:
        if member := db.get(models.Member, create_obj.member_id):
            if member.outstanding_payment >= constants.MAX_OUTSTANDING_ALLOWED:
                raise HTTPException(
                    status_code=status.HTTP_402_PAYMENT_REQUIRED,
                    detail="You need to clear previous outstanding dues for book loans.",
                )

            # member is under max outstanding payment allowed, proceed flow
            if book := db.get(models.Book, create_obj.book_id):
                if book.stock < 1:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Book with id: {create_obj.book_id} is out of stock.",
                    )

                book.stock -= 1
                db.add(book)

                member.outstanding_payment += constants.LOAN_CHARGE
                db.add(member)

        return super().create(db, create_obj, commit)
        
    def delete(self, db: DB, id: int, commit: bool = True) -> SQLModel:
        if book_loan := db.get(models.BookLoans, id):
            if book_loan.return_date is None:
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

                book.stock += 1
                db.add(book)

                book_loan.return_date = datetime.now().date()
                db.add(book_loan)

                if commit:
                    db.commit()
                else:
                    db.flush() 

                db.refresh(book_loan)
                return book_loan
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This book has already been returned.",
            )

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book loan with id: {id} does not exist.",
        )