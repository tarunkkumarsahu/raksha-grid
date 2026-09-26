"""Database configuration for RAKSHA Grid.

Development defaults to a local SQLite database. Production can provide a
PostgreSQL/PostGIS-compatible DATABASE_URL without changing application code.
"""
from __future__ import annotations

import os
from collections.abc import Iterator

from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker


DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./raksha_grid_dev.db")


class Base(DeclarativeBase):
    pass


def make_engine(database_url: str = DATABASE_URL) -> Engine:
    is_sqlite = database_url.startswith("sqlite")
    connect_args = {"check_same_thread": False} if is_sqlite else {}
    created_engine = create_engine(
        database_url,
        connect_args=connect_args,
        pool_pre_ping=True,
    )

    if is_sqlite:
        @event.listens_for(created_engine, "connect")
        def _enable_sqlite_foreign_keys(dbapi_connection, _connection_record) -> None:
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()

    return created_engine


engine = make_engine()
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def init_db(target_engine: Engine = engine) -> None:
    # Import models here so SQLAlchemy metadata is populated without creating
    # circular imports at module import time.
    from app import models  # noqa: F401

    Base.metadata.create_all(bind=target_engine)


def get_db() -> Iterator[Session]:
    with SessionLocal() as session:
        yield session
