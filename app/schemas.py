"""
app/schemas.py — Pydantic models for request and response bodies.

These describe the SHAPE OF DATA going in and out of the API.
They're separate from database models so we can validate, transform, and
control exactly what's exposed.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class SongBase(BaseModel):
    """Fields shared by create and update — the user-editable fields."""
    title:  str = Field(..., min_length=1, max_length=200)
    artist: str = Field(..., min_length=1, max_length=200)
    album:  Optional[str] = Field(None, max_length=200)
    year:   Optional[int] = Field(None, ge=1900, le=2100)

    # tags is a list of strings. We enforce length and per-tag character limits.
    # FastAPI will automatically return a 422 if these aren't met. Free validation!
    tags:   list[str] = Field(..., min_length=1, max_length=10)


class SongCreate(SongBase):
    """Schema for POST /songs — incoming data when creating a song."""
    pass


class SongUpdate(SongBase):
    """Schema for PUT /songs/{id} — incoming data when updating."""
    pass


class SongRead(SongBase):
    """Schema for responses — what we send back to the client."""
    id: int
    created_at: datetime

    # PYDANTIC v2 BASIC: this tells Pydantic to read from ORM objects
    # (i.e., SQLAlchemy models) by attribute, not just from dicts.
    model_config = ConfigDict(from_attributes=True)


class MetricsResponse(BaseModel):
    """Schema for GET /metrics."""
    requests_total: int
    requests_by_endpoint: dict[str, int]
    songs_in_db: int
    errors_total: int