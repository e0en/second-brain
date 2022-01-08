#!/usr/bin/env python
# -*- coding: utf-8 -*-
from fastapi import FastAPI, HTTPException, status, Depends
from sqlalchemy import and_
from sqlalchemy.orm.session import Session

from schema import Entry, Tag, EntryCreate
import models
import database


models.Base.metadata.create_all(bind=database.engine)


app = FastAPI()


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@app.get("/entry/{entry_id}", response_model=Entry)
def read_entry(entry_id: str, db: Session = Depends(get_db)):
    """Get an entry."""
    entry = db.query(models.Entry).filter(models.Entry.id == entry_id).first()
    if entry is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        return entry


@app.post("/entry/", status_code=201)
def create_entry(entry: EntryCreate, db: Session = Depends(get_db)):
    """Create a new entry."""
    db_entry = models.Entry(content=entry.content)
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry


@app.put("/entry/{entry_id}")
def update_entry(entry_id: str, entry: Entry, db: Session = Depends(get_db)):
    """Modify content, tag of an entry."""
    if not has_entry(db, entry_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    db_entry = models.Entry(id=entry_id, content=entry.content)
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry


@app.delete("/entry/{entry_id}")
def delete_entry(entry_id: str, db: Session = Depends(get_db)):
    """Delete an entry."""
    db.query(models.Entry).filter(models.Entry.id == entry_id).delete()
    db.query(models.EntryToTag).filter(models.EntryToTag.entry_id == entry_id).delete()
    db.commit()


@app.get("/tag/{name}", response_model=Tag)
def read_tag(name: str, db: Session = Depends(get_db)):
    """Get a tag."""
    tag = db.query(models.Tag).filter(models.Tag.name == name).first()
    if tag is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        return tag


@app.post("/tag/", status_code=201)
def create_tag(name: str, db: Session = Depends(get_db)):
    """Create a new tag. Return an error if a tag with the same name exists."""
    db_tag = models.Tag(name=name)
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag


@app.put("/tag/{name}")
def update_tag(name: str, new_name: str, db: Session = Depends(get_db)):
    """Rename a tag. Return an error if the name is not available."""
    db_tag = db.query(models.Tag).filter(models.Tag.name == name).first()
    if db_tag is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    db_tag.name = new_name
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag


@app.delete("/tag/{name}")
def delete_tag(name: str, db: Session = Depends(get_db)):
    """Delete a tag, and remove it from every entry."""
    db_tag = db.query(models.Tag).filter(models.Tag.name == name).first()
    if db_tag is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    db.delete(db_tag)
    db.query(models.EntryToTag).filter(models.EntryToTag.tag_name == name).delete()
    db.commit()


@app.post("/entry_tag/", status_code=201)
def add_tag_to_entry(entry_id: str, tag_name: str, db: Session = Depends(get_db)):
    """Add a tag to an entry."""
    if not has_entry(db, entry_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    if not has_tag(db, tag_name):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    db_entry_to_tag = models.EntryToTag(entry_id=entry_id, tag_name=tag_name)
    db.add(db_entry_to_tag)
    db.commit()
    db.refresh(db_entry_to_tag)
    return db_entry_to_tag


@app.get("/entry_tag/")
def get_tags_in_entry(entry_id: str, db: Session = Depends(get_db)):
    """Retrieve all tag attached to an entry."""
    if not has_entry(db, entry_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    rows = (
        db.query(models.EntryToTag).filter(models.EntryToTag.entry_id == entry_id).all()
    )
    return [r.tag_name for r in rows]


@app.delete("/entry_tag/")
def remove_tag_from_entry(entry_id: str, tag_name: str, db: Session = Depends(get_db)):
    """Remove a tag to an entry."""
    db_entry_to_tag = (
        db.query(models.EntryToTag)
        .filter(
            and_(
                models.EntryToTag.entry_id == entry_id,
                models.EntryToTag.tag_name == tag_name,
            )
        )
        .first()
    )
    if db_entry_to_tag is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    db.delete(db_entry_to_tag)
    db.commit()


@app.get("/tag_entry/")
def get_entries_with_tag(tag_name: str, db: Session = Depends(get_db)):
    """Retrieve all entries with the given tag."""
    if not has_tag(db, tag_name):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    rows = (
        db.query(models.EntryToTag).filter(models.EntryToTag.tag_name == tag_name).all()
    )
    return [r.entry_id for r in rows]


def has_entry(db: Session, entry_id: str) -> bool:
    n_result = db.query(models.Entry).filter(models.Entry.id == entry_id).count()
    return n_result > 0


def has_tag(db: Session, name: str) -> bool:
    n_result = db.query(models.Tag).filter(models.Tag.name == name).count()
    return n_result > 0


async def entry_has_tag(db: Session, entry_id: str, tag_name: str) -> bool:
    n_result = (
        db.query(models.EntryToTag)
        .filter(
            and_(
                models.EntryToTag.entry_id == entry_id,
                models.EntryToTag.tag_name == tag_name,
            )
        )
        .count()
    )
    return n_result > 0
