from datetime import datetime
from sqlmodel import Field, SQLModel
from pydantic import field_validator


class BookBase(SQLModel):
    title: str = Field(index=True)
    authors: str = Field(index=True)
    average_rating: float
    isbn: int = Field(index=True, unique=True)
    isbn13: int = Field(index=True, unique=True)
    language_code: str
    num_pages: int = Field(alias="  num_pages")
    ratings_count: int
    text_reviews_count: int
    publication_date: datetime
    publisher: str

    @field_validator("publication_date", mode="before")
    @classmethod
    def parse_publication_date(cls, value: str | datetime) -> datetime:
        """Convert string to datetime."""
        if isinstance(value, str):
            return datetime.strptime(value, "%m/%d/%Y")
        return value


class Book(BookBase, table=True):
    id: int | None = Field(default=None, primary_key=True, index=True, alias="bookID")
