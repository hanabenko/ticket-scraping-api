from __future__ import annotations
import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.join(__file__, ".."))))
from sqlalchemy.orm import Session
from app.db import SessionLocal, Base, engine
from app.normalize import upsert_interactions_from_events
from app.connectors.ticketing import load_ticketing_file
from app.connectors.merch import load_merch_file
from app.connectors.social import load_social_file
from app.connectors.streaming import load_streams_file

if __name__ == "__main__":
    # ensure tables
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()
    try:
        total = 0
        total += upsert_interactions_from_events(db, load_ticketing_file("data/ticketing.json"))
        total += upsert_interactions_from_events(db, load_merch_file("data/merch.json"))
        total += upsert_interactions_from_events(db, load_social_file("data/social.json"))
        total += upsert_interactions_from_events(db, load_streams_file("data/streams.json"))
        print(f"Harvested events -> interactions: {total}")
    finally:
        db.close()
