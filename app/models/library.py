from datetime import date, datetime
from pydantic import field_validator
from sqlmodel import Field, SQLModel


class BookLoansBase(SQLModel):
    book_id: int = Field(index=True)
    member_id: int = Field(index=True)
    loan_date: date | None
    return_date: date | None = Field(default=None)

    @field_validator("loan_date", mode="before")
    @classmethod
    def parse_loan_date(cls, value: str | date | None) -> date:
        """Parse loan date from str if available, set to current date if empty."""
        if not value:
            return datetime.now().date()
        if isinstance(value, str):
            return datetime.strptime(value, "%m/%d/%Y").date()
        return value


class BookLoans(BookLoansBase, table=True):
    id: int | None = Field(default=None, primary_key=True, index=True)


class BookLoansPub(BookLoansBase):
    id: int


class BookLoansCreate(BookLoansBase):
    pass
