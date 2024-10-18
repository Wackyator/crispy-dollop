from fastapi import APIRouter

from . import books
from . import members


router = APIRouter(prefix="/v1")
router.include_router(books.router)
router.include_router(members.router)
