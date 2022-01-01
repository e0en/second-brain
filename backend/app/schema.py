#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Entry(BaseModel):
    content: str
    tags: str
    updated_at: Optional[datetime]


class Tag(BaseModel):
    name: str
    updated_at: Optional[datetime]

