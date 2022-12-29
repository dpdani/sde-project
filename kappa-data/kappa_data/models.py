import json
from datetime import datetime
from typing import Self

from sqlmodel import Field, SQLModel, Session, create_engine, select

from .config import config


engine = None


def get_db():
    global engine
    if engine is None:
        engine = create_engine(config.db.url)
    with Session(engine) as session:
        yield session


class User(SQLModel, table=True):
    user_id: int | None = Field(primary_key=True)
    login: str = Field(unique=True)
    password: str
    token: str | None

    @classmethod
    def get(cls, db: Session, login: str):
        result, *_ = db.exec(
            select(cls)
            .where(cls.login == login)
        )
        return result

    @classmethod
    def signup(cls, db: Session, login: str, password: str):
        db.add(cls(login=login, password=password))


class Function(SQLModel, table=True):
    fn_id: int | None = Field(primary_key=True)
    name: str
    owner: int = Field(foreign_key="user.user_id")
    code_id: str

    @classmethod
    def get(cls, db: Session, owner: int, name: str) -> Self:
        result, *_ = db.exec(
            select(cls)
            .where(cls.owner == owner)
            .where(cls.name == name)
        )
        return result

    @classmethod
    def get_by_id(cls, db: Session, fn_id: int) -> Self:
        result, *_ = db.get(cls, fn_id)
        return result


class KappaLog(SQLModel, table=True):
    log_id: int | None = Field(primary_key=True)
    time: datetime | None
    user: int | None
    fn: str | None
    content: str

    @classmethod
    def add(cls, db: Session, user: int | None, fn: str | None, content: dict):
        return db.add(cls(
            user=user,
            fn=fn,
            content=json.dumps(content),
        ))

    @classmethod
    def get_all(cls, db: Session, user: int, fn: str):
        return db.exec(
            select(cls)
            .where(cls.user == user)
            .where(cls.fn == fn)
        )
