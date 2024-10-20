from datetime import date, datetime
from sqlmodel import Field, SQLModel
from pydantic import field_validator


class BookBase(SQLModel):
    title: str = Field(index=True)
    authors: str = Field(index=True)
    average_rating: float
    isbn: int = Field(index=True, unique=True)
    isbn13: int = Field(index=True, unique=True)
    language_code: str
    num_pages: int
    ratings_count: int
    text_reviews_count: int
    publication_date: date
    publisher: str

    @field_validator("publication_date", mode="before")
    @classmethod
    def parse_publication_date(cls, value: str | date) -> date:
        """Convert string to datetime."""
        if isinstance(value, str):
            return datetime.strptime(value, "%m/%d/%Y").date()
        return value


class Book(BookBase, table=True):
    id: int | None = Field(default=None, primary_key=True, index=True)
    stock: int = Field(default=1, ge=0)


class BookPub(BookBase):
    id: int


class BookCreate(BookBase):
    pass


class BookUpdate(BookBase):
    pass
