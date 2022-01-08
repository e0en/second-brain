#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import BaseModel


class EntryBase(BaseModel):
    content: str


class EntryCreate(EntryBase):
    pass


class Entry(EntryBase):
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class TagBase(BaseModel):
    name: str


class TagCreate(TagBase):
    pass


class Tag(TagBase):
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
