"""Database engine, session factory, and base model."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import os

DATABASE_URL = os.getenv("DATABASE_URL")

# Create a SQLAlchemy engine for the configured database URL.
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Session factory for request-scoped database sessions.
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Declarative base for ORM models.
class Base(DeclarativeBase):
    pass


def get_db():
    # Dependency helper for opening/closing DB sessions.
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
