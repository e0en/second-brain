#!/usr/bin/env python
from datetime import datetime
import random
from typing import List  # SQLModel requires this

from sqlmodel import Field, Relationship, SQLModel, create_engine

from secret import DATABASE_URL


_ID_CHARACTERS = "123456789abcdefghjkmnpqrstuvwxyz"


def generate_id() -> str:
    return "".join(random.sample(_ID_CHARACTERS, 3))


def now() -> datetime:
    return datetime.utcnow()


class EntryToTag(SQLModel, table=True):
    entry_id: str = Field(foreign_key="entry.id", primary_key=True)
    tag_name: str = Field(foreign_key="tag.name", primary_key=True)
    created_at: datetime = Field(default=now)


class TagBase(SQLModel):
    name: str = Field(primary_key=True)


class Tag(TagBase, table=True):
    created_at: datetime = Field(default=now)
    updated_at: datetime = Field(default=now)

    entries: List["Entry"] = Relationship(back_populates="tags", link_model=EntryToTag)


class EntryBase(SQLModel):
    content: str


class Entry(EntryBase, table=True):
    id: str = Field(default=generate_id, primary_key=True)
    created_at: datetime = Field(default=now)
    updated_at: datetime = Field(default=now)

    tags: List[Tag] = Relationship(back_populates="entries", link_model=EntryToTag)


class EntryCreate(EntryBase):
    pass


engine = create_engine(
    DATABASE_URL, echo=True, connect_args={"check_same_thread": False}
)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    create_db_and_tables()
