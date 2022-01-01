#!/usr/bin/env python
# -*- coding: utf-8 -*-
from fastapi import FastAPI, HTTPException, status

from schema import Entry, Tag
import db


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello, world!"}


@app.get("/entry/{entry_id}")
async def read_entry(entry_id: str):
    """Get an entry."""
    entry = db.Entry().read(entry_id)
    if entry is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        return entry


@app.post("/entry/", status_code=201)
async def create_entry(entry: Entry):
    """Create a new entry."""
    db.Entry().create(entry.dict())
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@app.put("/entry/{entry_id}")
async def update_entry(entry_id: str, entry: Entry):
    """Modify content, tag of an entry."""
    if not db.Entry().check_existence(entry_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    db.Entry().update(entry_id, entry.dict())
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@app.delete("/entry/{entry_id}")
async def delete_entry(entry_id: str):
    """Delete an entry."""
    if not db.Entry().check_existence(entry_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    db.Entry().delete(entry_id)
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@app.get("/tag/{name}")
async def read_tag(name: str):
    """Get a tag."""
    tag = db.Tag().read(name)
    if tag is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        return tag


@app.post("/tag/", status_code=201)
async def create_tag(name: str):
    """Create a new tag. Return an error if a tag with the same name exists."""
    db.Tag().create(Tag(name=name).dict())
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@app.put("/tag/{name}")
async def update_tag(name: str):
    """Rename a tag. Return an error if the name is not available."""
    if not db.Tag().check_existence(name):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    tag = Tag(name=name)
    db.Tag().update(name, tag.dict())
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@app.delete("/tag/{name}")
async def delete_tag(name: str):
    """Delete a tag, and remove it from every entry."""
    if not db.Tag().check_existence(name):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    db.Tag().delete(name)
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
