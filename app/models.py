"""
app/models.py — SQLAlchemy ORM models.

These classes are how we read and write the database in Python terms.
A `Song` object IS a row in the `songs` table.
"""

from datetime import datetime
from sqlalchemy import Integer, String, JSON, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


# Every SQLAlchemy model inherits from a Base class. We define it once here.
class Base(DeclarativeBase):
    pass

class Song(Base):
    __tablename__ = "songs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    artist: Mapped[str] = mapped_column(String(200), nullable=False)
    album: Mapped[str] = mapped_column(String(200), nullable=True)
    year: Mapped[int] = mapped_column(Integer, nullable = True)

    tags: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<Song id={self.id} title={self.title!r} artist={self.artist!r}"
    