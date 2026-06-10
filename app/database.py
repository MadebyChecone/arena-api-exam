from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine

DATABASE_URL = "sqlite:///arena.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


# Alias to have less noise on FastAPI endpoints.
# Use it as an endpoint parameter to access the database session.
#
# Instead of:
# def list_players(session: Session = Depends(get_session)):
#     ...
#
# Write:
# def list_players(session: SessionDep):
#     ...
SessionDep = Annotated[Session, Depends(get_session)]
