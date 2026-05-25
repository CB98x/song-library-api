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
    title: str = Field(..., min_length=1, max_length=200)
    artist: str = Field(..., min_length=1, max_length=200)
    album: Optional[str] = Field(None, max_length=200)
    year: Optional[int] = Field(None, ge=1900, le=2100)
    tags: list[str] = Field(..., min_length=1, max_length=10)

class SongCreate(SongBase):
    pass

class SongUpdate(SongBase):
    pass

class SongRead(SongBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class MetricsResponse(BaseModel):
    requests_total: int
    requests_by_endpoint: dict[str, int]
    songs_in_db: int
    errors_total: int

    