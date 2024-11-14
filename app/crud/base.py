
import logging
from typing import Type

from fastapi import HTTPException
from sqlmodel import SQLModel, select

from app.db import DB


class CRUDBase:
    def get_inner(self) -> Type[SQLModel]:
        raise Exception(f"'get_inner' is not implemented on {self.get_name()}")

    def get_name(self) -> str:
        return f"{type(self).__name__}()"

    def get(self, db: DB, id: int) -> type[SQLModel]:
        if obj := db.get(self.get_inner(), id):
            return obj
        raise HTTPException(status_code=404, detail=f"{self.get_name()} not found")

    def list(self, db: DB, offset: int = 0, limit: int = 100) -> type[SQLModel]:
        return db.exec(select(self.get_inner()).offset(offset).limit(limit)).all()

    def create(self, db: DB, create_obj: type[SQLModel], commit: bool = True, *args, **kwargs) -> type[SQLModel]:
        if obj := self.get_inner().model_validate(create_obj):
            db.add(obj)

            if commit:
                db.commit()
            else:
                db.flush()

            db.refresh(obj)
            
            logging.error(obj)
            return obj
        raise HTTPException(status_code=404, detail=f"{self.get_name()} not found")

    def update(self, db: DB, id: int, update_obj: type[SQLModel], commit: bool = True, *args, **kwargs) -> type[SQLModel]:
        if old := db.get(self.get_inner(), id):
            old.sqlmodel_update(update_obj.model_dump(exclude_unset=True))
            db.add(old)
            
            if commit:
                db.commit()
            else:
                db.flush()
            
            db.refresh(old)
            return old
        raise HTTPException(status_code=404, detail=f"{self.get_name()} not found")

    def delete(self, db: DB, id: int, commit: bool = True) -> type[SQLModel]:
        if obj := db.get(self.get_inner(), id):
            db.delete(obj)

            if commit:
                db.commit()
            else:
                db.flush()
            
            return obj
        raise HTTPException(status_code=404, detail=f"{self.get_name()} not found")
