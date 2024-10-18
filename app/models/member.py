from sqlmodel import SQLModel, Field


class MemberBase(SQLModel):
    name: str = Field(index=True, min_length=1)
    email: str = Field(index=True, unique=True)


class Member(MemberBase, table=True):
    id: int | None = Field(default=None, primary_key=True, index=True)
    outstanding_payment: int = Field(default=0)


class MemberPub(MemberBase):
    id: int
    outstanding_payment: int


class MemberCreate(MemberBase):
    pass


class MemberUpdate(MemberBase):
    pass
