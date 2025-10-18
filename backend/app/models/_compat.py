from flask import current_app
from sqlalchemy import types
from sqlalchemy.dialects import postgresql
from sqlalchemy.types import TypeDecorator, JSON, String
from sqlalchemy.dialects.postgresql import ARRAY

'''
def ArrayOrJSON(base_type):
    """Return ARRAY for PostgreSQL, JSON for SQLite."""
    try:
        uri = current_app.config.get("SQLALCHEMY_DATABASE_URI", "")
    except RuntimeError:
        # Current app not ready (e.g., during CLI init)
        uri = ""

    if "sqlite" in uri:
        return types.JSON
    else:
        return postgresql.ARRAY(base_type)
'''

class ArrayOrJSON(TypeDecorator):
    """
    Emulates ARRAY for SQLite by using JSON.
    Uses native ARRAY for PostgreSQL.
    """
    impl = JSON
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == 'sqlite':
            return dialect.type_descriptor(JSON())
        else:
            return dialect.type_descriptor(ARRAY(String()))

    def process_bind_param(self, value, dialect):
        if value is None:
            return []
        return value

    def process_result_value(self, value, dialect):
        return value or []


def JSONOrJSONB():
    """Return JSONB for PostgreSQL, JSON for SQLite."""
    try:
        uri = current_app.config.get("SQLALCHEMY_DATABASE_URI", "")
    except RuntimeError:
        uri = ""

    if "sqlite" in uri:
        return types.JSON
    else:
        return postgresql.JSONB
