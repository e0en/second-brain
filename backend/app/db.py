#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
import uuid


DbRow = dict[str, str | int | float | bool | datetime | None]


class Crud:
    """Perform basic CRUD operations on sqlite3, using flat, simple
    dictionaries as input/output data."""
    table: str
    key_column: str

    def create(self, data: DbRow):
        data['updated_at'] = datetime.now()
        query = f'INSERT INTO {self.table}'
        pass

    def read(self, primary_key: str) -> DbRow | None:
        query = f'SELECT * FROM {self.table} WHERE {self.key_column}'
        pass

    def update(self, primary_key: str, data: DbRow):
        data['updated_at'] = datetime.now()
        query = f'UPDATE TABLE {self.table} WHERE {self.key_column}'
        pass

    def delete(self, primary_key: str):
        query = f'DELETE FROM {self.table} WHERE {self.key_column}'
        pass

    def filter(self) -> list[DbRow]:
        raise NotImplementedError

    def check_existence(self, primary_key: str) -> bool:
        query = f'SELECT 1 FROM {self.table} WHERE {self.key_column} LIMIT 1'
        return False


class Entry(Crud):
    def __init__(self):
        self.table: str = "entry"
        self.key_column: str = "id"

    def create(self, data: DbRow):
        data[self.key_column] = self.generate_key()
        super().create(data)

    def generate_key(self):
        return str(uuid.uuid4())


class Tag(Crud):
    def __init__(self):
        self.table: str = "tag"
        self.key_column: str = "name"
