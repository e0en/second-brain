#!/usr/bin/env python
# -*- coding: utf-8 -*-
from fastapi import FastAPI, HTTPException, status, Depends
from sqlmodel import select, Session

import models


app = FastAPI()


def get_db():
    db = Session(models.engine)
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
def on_startup():
    models.create_db_and_tables()


@app.get("/")
async def root():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@app.get("/entry/{entry_id}", response_model=models.Entry)
def read_entry(entry_id: str, db: Session = Depends(get_db)):
    """Get an entry."""
    entry = db.exec(select(models.Entry).where(models.Entry.id == entry_id)).one()
    if entry is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        return entry


@app.get("/entries/")
def read_entries(offset: int, limit: int, db: Session = Depends(get_db)):
    """Get a range of entries."""
    entries = db.exec(
        select(models.Entry)
        .order_by(models.Entry.updated_at)
        .offset(offset)
        .limit(limit)
    ).all()
    return entries


@app.post("/entry/", status_code=201)
def create_entry(entry: models.EntryCreate, db: Session = Depends(get_db)):
    """Create a new entry."""
    db_entry = models.Entry(content=entry.content)
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry


@app.put("/entry/{entry_id}")
def update_entry(entry_id: str, entry: models.Entry, db: Session = Depends(get_db)):
    """Modify content, tag of an entry."""
    db_entry = db.exec(select(models.Entry).where(models.Entry.id == entry_id)).one()
    if db_entry is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    db_entry.content = entry.content
    db_entry.updated_at = models.now()
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry


@app.delete("/entry/{entry_id}")
def delete_entry(entry_id: int, db: Session = Depends(get_db)):
    """Delete an entry."""
    entry = db.exec(select(models.Entry).where(models.Entry.id == entry_id)).one()
    if entry is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    db.delete(entry)
    db.commit()


@app.get("/tag/{name}", response_model=models.Tag)
def read_tag(name: str, db: Session = Depends(get_db)):
    """Get a tag."""
    tag = db.exec(select(models.Tag).where(models.Tag.name == name)).one()
    if tag is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        return tag


@app.get("/tags", response_model=models.Tag)
def read_tags(offset: int, limit: int, db: Session = Depends(get_db)):
    """Get a range of tags."""
    tags = db.exec(
        select(models.Tag).order_by(models.Tag.updated_at).offset(offset).limit(limit)
    ).all()
    return tags


@app.post("/tag/", status_code=201)
def create_tag(name: str, db: Session = Depends(get_db)):
    """Create a new tag. Return an error if a tag with the same name exists."""
    tag = models.Tag(name=name)
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag


@app.put("/tag/{name}")
def update_tag(name: str, new_name: str, db: Session = Depends(get_db)):
    """Rename a tag. Return an error if the name is not available."""
    tag = db.exec(select(models.Tag).where(models.Tag.name == name)).one()
    if tag is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    tag.name = new_name
    tag.updated_at = models.now()
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag


@app.delete("/tag/{name}")
def delete_tag(name: str, db: Session = Depends(get_db)):
    """Delete a tag, and remove it from every entry."""
    tag = db.exec(select(models.Tag).where(models.Tag.name == name)).one()
    if tag is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    db.delete(tag)
    db.commit()


@app.post("/entry_tag/", status_code=201, response_model=models.Tag)
def add_tag_to_entry(entry_id: str, tag_name: str, db: Session = Depends(get_db)):
    """Add a tag to an entry."""
    entry = db.exec(select(models.Entry).where(models.Entry.id == entry_id)).one()
    if entry is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    tag = db.exec(select(models.Tag).where(models.Tag.name == tag_name)).one()
    if tag is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    entry.tags.append(tag)
    db.commit()
    return tag


@app.get("/entry_tag/")
def get_tags_in_entry(entry_id: str, db: Session = Depends(get_db)):
    """Retrieve all tag attached to an entry."""
    entry = db.exec(select(models.Entry).where(models.Entry.id == entry_id)).one()
    if entry is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    return entry.tags


@app.delete("/entry_tag/", response_model=models.Tag)
def remove_tag_from_entry(entry_id: str, tag_name: str, db: Session = Depends(get_db)):
    """Remove a tag to an entry."""
    entry = db.exec(select(models.Entry).where(models.Entry.id == entry_id)).one()
    if entry is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    tag = db.exec(select(models.Tag).where(models.Tag.name == tag_name)).one()
    if tag is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    entry.tags.remove(tag)
    db.commit()
    return tag


@app.get("/tag_entry/")
def get_entries_with_tag(tag_name: str, db: Session = Depends(get_db)):
    """Retrieve all entries with the given tag."""
    tag = db.exec(select(models.Tag).where(models.Tag.name == tag_name)).one()
    if tag is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    return [r.id for r in tag.entries]
