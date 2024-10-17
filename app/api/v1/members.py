from fastapi import APIRouter

from app.models import Member

router = APIRouter(prefix="/members", tags=["members"])


@router.get("/")
async def get_members() -> list[Member]:
    return []
