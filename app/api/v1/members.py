import logging
from typing import Annotated, Any
from fastapi import APIRouter, HTTPException, Query, status
from sqlmodel import select

from app.db import DB
from app import models

router = APIRouter(prefix="/members", tags=["members"])


@router.get("/", response_model=list[models.MemberPub])
async def get_members(
    db: DB,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> Any:
    members = db.exec(select(models.Member).offset(offset).limit(limit)).all()
    return members


@router.get("/{member_id}", response_model=models.MemberPub)
async def get_member(db: DB, member_id: int) -> Any:
    member = db.get(models.Member, member_id)

    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    return member


@router.post("/", response_model=models.MemberPub)
async def create_member(db: DB, member: models.MemberCreate) -> Any:
    if db.exec(select(models.Member).where(models.Member.email == member.email)):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Account with this email already exists",
        )

    db_member = models.Member.model_validate(member)
    db.add(db_member)
    db.commit()
    db.refresh(db_member)

    return db_member


@router.put("/{member_id}", response_model=models.MemberPub)
async def update_member(db: DB, member_id: int, member: models.MemberUpdate) -> Any:
    db_member = db.get(models.Member, member_id)

    if not db_member:
        raise HTTPException(status_code=404, detail="Member not found")

    # could be done better
    member_data = member.model_dump(exclude_unset=True)
    db_member.sqlmodel_update(member_data)

    db.add(db_member)
    db.commit()
    db.refresh(db_member)

    return db_member


@router.delete("/{member_id}", response_model=models.MemberPub)
async def delete_book(db: DB, member_id: int) -> Any:
    member = db.get(models.Member, member_id)

    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    db.delete(member)
    db.commit()

    return member
