from typing import Generator, Annotated
from sqlmodel import create_engine, Session
from fastapi import Depends

DB_URL = "sqlite:///database.db"

engine = create_engine(DB_URL, echo=True)


def get_session() -> Generator[Session]:
    with Session(engine) as session:
        yield session


DB = Annotated[Session, Depends(get_session)]
