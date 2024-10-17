from fastapi import APIRouter

from . import books


router = APIRouter(prefix="/v1")
router.include_router(books.router)
