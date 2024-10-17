from fastapi import APIRouter

from app.models import Book


router = APIRouter(prefix="/books", tags=["books"])


@router.get("/")
async def get_books() -> list[Book]:
    return []
