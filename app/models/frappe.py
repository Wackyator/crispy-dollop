from pydantic import Field, BaseModel


# using pydantic model here instead of SQLModel
# alias on SQLModel seems to be broken???
class APIResponse(BaseModel):
    id: int = Field(alias="bookID")
    title: str
    authors: str
    average_rating: float
    isbn: int
    isbn13: int
    language_code: str
    num_pages: int = Field(alias="  num_pages")
    ratings_count: int
    text_reviews_count: int
    publication_date: str
    publisher: str
