from __future__ import annotations
from datetime import datetime
from typing import Dict, Any, Iterable, List
import pandas as pd
from sqlalchemy.orm import Session
from . import models
from .crud import get_or_create_artist, get_or_create_user


ISO_FMT = "%Y-%m-%dT%H:%M:%S%z"


def upsert_interactions_from_events(db: Session, events: Iterable[Dict[str, Any]]) -> int:
    inserted = 0
    for e in events:
        artist = get_or_create_artist(db, e["artist_name"]) if e.get("artist_name") else None
        user = get_or_create_user(db, e.get("email"))
        occurred_at = pd.to_datetime(e["occurred_at"]).to_pydatetime()
        rec = models.Interaction(
            user_id=user.id,
            artist_id=artist.id if artist else None,
            interaction_type=e["interaction_type"],
            channel=e.get("channel"),
            metadata_json=e.get("metadata"),
            occurred_at=occurred_at,
        )
        db.add(rec)
        inserted += 1
    db.commit()
    return inserted
