"""Database configuration using SQLite + SQLAlchemy."""

from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


BASE_DIR = Path(__file__).resolve().parent
DATABASE_URL = f"sqlite:///{BASE_DIR / 'employees.db'}"

# check_same_thread is required for SQLite with FastAPI.
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
# SessionLocal is the session factory used to talk to the database.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base is the parent class for all SQLAlchemy models.
Base = declarative_base()


def get_db():
    """Provide a database session for each request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """Create all tables defined by SQLAlchemy models."""
    # Creates the employees table if it does not exist.
    Base.metadata.create_all(bind=engine)
