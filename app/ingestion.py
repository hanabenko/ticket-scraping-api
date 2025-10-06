from __future__ import annotations
from datetime import datetime
import pandas as pd
from sqlalchemy.orm import Session
from . import models
from .crud import get_or_create_artist, get_or_create_user


def load_concerts_csv(db: Session, path: str) -> int:
    df = pd.read_csv(path)
    inserted = 0
    for _, row in df.iterrows():
        artist = get_or_create_artist(db, row["artist_name"])
        concert = models.Concert(
            artist_id=artist.id,
            venue=row.get("venue"),
            city=row.get("city"),
            country=row.get("country"),
            event_date=pd.to_datetime(row.get("event_date")).date() if row.get("event_date") else None,
            source=row.get("source"),
            url=row.get("url"),
        )
        db.add(concert)
        inserted += 1
    db.commit()
    return inserted


def load_interactions_csv(db: Session, path: str) -> int:
    df = pd.read_csv(path)
    inserted = 0
    for _, row in df.iterrows():
        artist = get_or_create_artist(db, row["artist_name"])
        user = get_or_create_user(db, row.get("email") if "email" in df.columns else None)
        it = models.Interaction(
            user_id=user.id,
            artist_id=artist.id,
            interaction_type=row["interaction_type"],
            channel=row.get("channel"),
            metadata_json=None,
            occurred_at=pd.to_datetime(row["occurred_at"]).to_pydatetime(),
        )
        db.add(it)
        inserted += 1
    db.commit()
    return inserted
