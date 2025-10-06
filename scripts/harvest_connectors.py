from __future__ import annotations
import os, sys
from typing import Iterable, Dict, Any, Optional
from urllib.parse import urlparse
from sqlalchemy.orm import Session

sys.path.append(os.path.dirname(os.path.abspath(os.path.join(__file__, ".."))))

from app.db import SessionLocal, Base, engine
from app.normalize import upsert_interactions_from_events
from app.connectors.ticketing import load_ticketing_file
from app.connectors.merch import load_merch_file
from app.connectors.social import load_social_file
from app.connectors.streaming import load_streams_file
# HTTP versions
from app.connectors.ticketing import load_ticketing_http
from app.connectors.merch import load_merch_http
from app.connectors.social import load_social_http
from app.connectors.streaming import load_streams_http


def _is_url(s: Optional[str]) -> bool:
    if not s: return False
    try:
        u = urlparse(s)
        return u.scheme in ("http", "https")
    except Exception:
        return False


def run(ticketing: Optional[str] = None, merch: Optional[str] = None, social: Optional[str] = None, streaming: Optional[str] = None) -> int:
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()
    total = 0
    try:
        if ticketing:
            events = load_ticketing_http(ticketing) if _is_url(ticketing) else load_ticketing_file(ticketing)
            total += upsert_interactions_from_events(db, events)
        if merch:
            events = load_merch_http(merch) if _is_url(merch) else load_merch_file(merch)
            total += upsert_interactions_from_events(db, events)
        if social:
            events = load_social_http(social) if _is_url(social) else load_social_file(social)
            total += upsert_interactions_from_events(db, events)
        if streaming:
            events = load_streams_http(streaming) if _is_url(streaming) else load_streams_file(streaming)
            total += upsert_interactions_from_events(db, events)
        return total
    finally:
        db.close()


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="Harvest connectors from files or URLs")
    ap.add_argument("--ticketing")
    ap.add_argument("--merch")
    ap.add_argument("--social")
    ap.add_argument("--streaming")
    args = ap.parse_args()
    count = run(args.ticketing, args.merch, args.social, args.streaming)
    print(f"Harvested {count} interactions")
