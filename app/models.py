from __future__ import annotations
from datetime import datetime, date
from typing import Optional
from sqlalchemy import String, Integer, Float, DateTime, Date, ForeignKey, JSON, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .db import Base


class Artist(Base):
    __tablename__ = "artists"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    genre: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    social_handles: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    concerts: Mapped[list["Concert"]] = relationship("Concert", back_populates="artist")
    interactions: Mapped[list["Interaction"]] = relationship("Interaction", back_populates="artist")
    attributions: Mapped[list["Attribution"]] = relationship("Attribution", back_populates="artist")


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[Optional[str]] = mapped_column(String(255), index=True, nullable=True)
    external_ids: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    interactions: Mapped[list["Interaction"]] = relationship("Interaction", back_populates="user")
    attributions: Mapped[list["Attribution"]] = relationship("Attribution", back_populates="user")


class Concert(Base):
    __tablename__ = "concerts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    artist_id: Mapped[int] = mapped_column(ForeignKey("artists.id"), index=True, nullable=False)
    venue: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    city: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    country: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    event_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    source: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    url: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    artist: Mapped["Artist"] = relationship("Artist", back_populates="concerts")


class Interaction(Base):
    __tablename__ = "interactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True, nullable=False)
    artist_id: Mapped[int] = mapped_column(ForeignKey("artists.id"), index=True, nullable=False)
    interaction_type: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    channel: Mapped[Optional[str]] = mapped_column(String(64), index=True, nullable=True)
    metadata_json: Mapped[Optional[dict]] = mapped_column("metadata", JSON, nullable=True)
    occurred_at: Mapped[datetime] = mapped_column(DateTime, index=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="interactions")
    artist: Mapped["Artist"] = relationship("Artist", back_populates="interactions")

    __table_args__ = (
        Index("ix_interactions_user_artist_time", "user_id", "artist_id", "occurred_at"),
    )


class Attribution(Base):
    __tablename__ = "attributions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True, nullable=False)
    artist_id: Mapped[int] = mapped_column(ForeignKey("artists.id"), index=True, nullable=False)
    score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    last_touch_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="attributions")
    artist: Mapped["Artist"] = relationship("Artist", back_populates="attributions")

    __table_args__ = (
        Index("uq_attr_user_artist", "user_id", "artist_id", unique=True),
    )


class ArtistDailyMetrics(Base):
    __tablename__ = "artist_daily_metrics"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    artist_id: Mapped[int] = mapped_column(ForeignKey("artists.id"), index=True, nullable=False)
    metric_date: Mapped[date] = mapped_column(Date, index=True, nullable=False)

    views: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    clicks: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    ticket_purchases: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    merch_purchases: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    streams: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    ctr: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    ticket_conversion_rate: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    merch_conversion_rate: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    stream_lift: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    __table_args__ = (
        Index("uq_artist_daily", "artist_id", "metric_date", unique=True),
    )
