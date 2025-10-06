from __future__ import annotations
from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel


class ArtistCreate(BaseModel):
    name: str
    genre: Optional[str] = None
    social_handles: Optional[dict] = None


class ArtistRead(BaseModel):
    id: int
    name: str
    genre: Optional[str] = None
    social_handles: Optional[dict] = None
    created_at: datetime

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    email: Optional[str] = None
    external_ids: Optional[dict] = None


class UserRead(BaseModel):
    id: int
    email: Optional[str] = None
    external_ids: Optional[dict] = None
    created_at: datetime

    class Config:
        from_attributes = True


class ConcertCreate(BaseModel):
    artist_id: int
    venue: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    event_date: Optional[date] = None
    source: Optional[str] = None
    url: Optional[str] = None


class ConcertRead(ConcertCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class InteractionCreate(BaseModel):
    user_id: int
    artist_id: int
    interaction_type: str
    channel: Optional[str] = None
    metadata: Optional[dict] = None
    occurred_at: datetime


class InteractionRead(InteractionCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class AttributionRead(BaseModel):
    user_id: int
    artist_id: int
    score: float
    last_touch_at: Optional[datetime] = None
    updated_at: datetime

    class Config:
        from_attributes = True


class ArtistDailyMetricsRead(BaseModel):
    artist_id: int
    metric_date: date
    views: int
    clicks: int
    ticket_purchases: int
    merch_purchases: int
    streams: int
    ctr: Optional[float] = None
    ticket_conversion_rate: Optional[float] = None
    merch_conversion_rate: Optional[float] = None
    stream_lift: Optional[float] = None

    class Config:
        from_attributes = True
