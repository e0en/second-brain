from datetime import datetime, timezone
import uuid

from sqlalchemy import (
    Column,
    UnicodeText,
    DateTime,
    ForeignKey,
    String,
)

from app.database import Base


def _generate_entry_id() -> str:
    x = uuid.uuid4()
    return str(x)


def _now() -> datetime:
    return datetime.now(tz=timezone.utc)


class Entry(Base):
    __tablename__ = "entries"

    id = Column(String, primary_key=True, default=_generate_entry_id)
    content = Column(UnicodeText, nullable=False)
    created_at = Column(DateTime, nullable=False, default=_now)
    updated_at = Column(DateTime, nullable=False, onupdate=_now)


class Tag(Base):
    __tablename__ = "tags"
    name = Column(UnicodeText, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=_now)
    updated_at = Column(DateTime, nullable=False, onupdate=_now)


class EntryToTag(Base):
    __table_name__ = "entry_to_tags"
    entry_id = Column(ForeignKey("entries.id"), primary_key=True)
    tag_name = Column(ForeignKey("tags.name"), primary_key=True)
    created_at = Column(DateTime, nullable=False, default=_now)
