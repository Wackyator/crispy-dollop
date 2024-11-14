from datetime import datetime
from typing import Any
from fastapi import APIRouter, HTTPException, status

from app import constants, models
from app.crud.library import CRUDBookLoans
from app.db import DB
from app.clients import FrappeClient

router = APIRouter(prefix="/library", tags=["library"])


@router.post("/loan_book", response_model=models.BookLoansPub)
async def loan_book(db: DB, book_loan: models.BookLoansCreate) -> Any:
    return CRUDBookLoans().create(db, book_loan, True)

@router.put("/return_book")
async def return_book(db: DB, loan_id: int) -> Any:
    return CRUDBookLoans().delete(db, loan_id, True)

@router.post(
    "/clear_dues/{member_id}", response_model=models.TransactionsPub, tags=["members"]
)
async def clear_dues(db: DB, member_id: int) -> Any:
    if member := db.get(models.Member, member_id):
        if member.outstanding_payment > 0:
            member.outstanding_payment = 0
            db.add(member)

            txn = models.Transactions(
                member_id=member_id, txn_date=datetime.now().date()
            )
            db.add(txn)

            db.commit()
            db.refresh(txn)

            return txn

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Member with id: {member_id} does not have any outstanding payment.",
        )

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Member with id: {member_id} does not exist.",
    )


@router.post("/import_books", status_code=201, tags=["books"])
async def import_books(db: DB) -> Any:
    total_imported = 0

    try:
        frappe_books = await FrappeClient.get_book_data()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Unable to import books from frappe at this time.",
        )

    for fb in frappe_books:
        if _ := db.get(models.Book, fb.id):
            continue

        db_book = models.Book.model_validate(fb)
        db.add(db_book)
        total_imported += 1

    db.commit()

    return {"success": True, "total_imported": total_imported}
