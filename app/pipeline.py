from __future__ import annotations
from datetime import date, datetime
from sqlalchemy.orm import Session
from .db import SessionLocal, Base, engine
from .ingestion import load_concerts_csv, load_interactions_csv
from .crud import recompute_attribution_for_user, compute_daily_metrics_for_date
from . import models


Base.metadata.create_all(bind=engine)


def run_daily_pipeline(concerts_csv: str | None = None, interactions_csv: str | None = None):
    db: Session = SessionLocal()
    try:
        if concerts_csv:
            load_concerts_csv(db, concerts_csv)
        if interactions_csv:
            load_interactions_csv(db, interactions_csv)

        # recompute attribution for all users touched in interactions file
        if interactions_csv:
            user_ids = [r[0] for r in db.query(models.Interaction.user_id).distinct().all()]
            now = datetime.utcnow()
            for uid in user_ids:
                recompute_attribution_for_user(db, user_id=uid, reference_time=now)

        # compute metrics for today
        compute_daily_metrics_for_date(db, date.today())
    finally:
        db.close()
