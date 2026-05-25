"""
app/database.py — database engine and session setup.
"""

import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.models import Base

logger = logging.getLogger(__name__)

# Path to the SQLite database file. It'll be created at the project root.
# In a real app this would be in an env var, not hardcoded.
DATABASE_URL = "sqlite:///./songs.db"

# The engine is the lowest-level interface to the database.
# check_same_thread=False is a SQLite-specific quirk for FastAPI.
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# A SessionLocal is a factory that produces database sessions.
# A "session" is one unit of work — a conversation with the DB.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db() -> None:
    """Create all tables defined on Base. Safe to call multiple times."""
    logger.info("Initializing database schema")
    Base.metadata.create_all(bind=engine)


def get_db():
    """
    FastAPI dependency that gives a route handler a DB session.
    
    The 'yield' makes this a generator — FastAPI calls it before the request,
    yields the session, then runs the finally block after the response is sent.
    This guarantees the session is always closed, even if the handler crashes.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()