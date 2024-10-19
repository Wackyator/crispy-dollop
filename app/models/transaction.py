from datetime import date
from sqlmodel import Field, SQLModel


class TransactionsBase(SQLModel):
    member_id: int
    txn_date: date


class Transactions(TransactionsBase, table=True):
    id: int | None = Field(default=None, primary_key=True, index=True)


class TransactionsPub(TransactionsBase):
    id: int
