from sqlmodel import SQLModel, Field


class MemberBase(SQLModel):
    name: str = Field(index=True)
    email: str = Field(index=True)
    outstanding_payment: int = Field(default=0)


class Member(MemberBase, table=True):
    id: int | None = Field(default=None, primary_key=True, index=True)
