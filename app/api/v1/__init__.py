from fastapi import APIRouter

from . import books
from . import members
from . import library


router = APIRouter(prefix="/v1")
router.include_router(books.router)
router.include_router(members.router)
router.include_router(library.router)
