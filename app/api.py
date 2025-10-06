from __future__ import annotations
from datetime import date, datetime
from typing import List
from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy import select, desc
from sqlalchemy.orm import Session
from .db import get_db
from . import models, schemas
from .crud import recompute_attribution_for_user, compute_daily_metrics_for_date
from .pipeline import run_daily_pipeline

router = APIRouter()


@router.post("/artists", response_model=schemas.ArtistRead)
def create_artist(artist: schemas.ArtistCreate, db: Session = Depends(get_db)):
    rec = models.Artist(name=artist.name, genre=artist.genre, social_handles=artist.social_handles)
    db.add(rec)
    db.commit()
    db.refresh(rec)
    return rec


@router.post("/users", response_model=schemas.UserRead)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    rec = models.User(email=user.email, external_ids=user.external_ids)
    db.add(rec)
    db.commit()
    db.refresh(rec)
    return rec


@router.post("/interactions", response_model=schemas.InteractionRead)
def create_interaction(payload: schemas.InteractionCreate, db: Session = Depends(get_db)):
    rec = models.Interaction(
        user_id=payload.user_id,
        artist_id=payload.artist_id,
        interaction_type=payload.interaction_type,
        channel=payload.channel,
        metadata_json=payload.metadata,
        occurred_at=payload.occurred_at,
    )
    db.add(rec)
    db.commit()
    db.refresh(rec)
    return rec


@router.post("/recompute_attribution/{user_id}")
def recompute_user_attribution(user_id: int, db: Session = Depends(get_db)):
    recompute_attribution_for_user(db, user_id=user_id, reference_time=datetime.utcnow())
    return {"status": "ok"}


@router.post("/compute_metrics/{metric_date}")
def compute_metrics(metric_date: date, db: Session = Depends(get_db)):
    compute_daily_metrics_for_date(db, metric_date)
    return {"status": "ok"}


@router.get("/top_artists", response_model=List[schemas.ArtistDailyMetricsRead])
def top_artists(limit: int = 10, db: Session = Depends(get_db)):
    today = date.today()
    rows = db.scalars(
        select(models.ArtistDailyMetrics)
        .where(models.ArtistDailyMetrics.metric_date == today)
        .order_by(desc(models.ArtistDailyMetrics.clicks))
        .limit(limit)
    ).all()
    return rows


@router.get("/artist/{artist_id}/metrics", response_model=List[schemas.ArtistDailyMetricsRead])
def artist_metrics(artist_id: int, days: int = 7, db: Session = Depends(get_db)):
    cutoff = date.fromordinal(date.today().toordinal() - days + 1)
    rows = db.scalars(
        select(models.ArtistDailyMetrics)
        .where((models.ArtistDailyMetrics.artist_id == artist_id) & (models.ArtistDailyMetrics.metric_date >= cutoff))
        .order_by(models.ArtistDailyMetrics.metric_date)
    ).all()
    return rows


@router.post("/run_pipeline")
def run_pipeline(concerts_csv: str | None = None, interactions_csv: str | None = None):
    run_daily_pipeline(concerts_csv=concerts_csv, interactions_csv=interactions_csv)
    return {"status": "ok"}


@router.post("/upload/concerts_csv")
async def upload_concerts_csv(file: UploadFile = File(...), db=Depends(get_db)):
    import tempfile, shutil
    from app.ingestion import load_concerts_csv
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name
    count = load_concerts_csv(db, tmp_path)
    return {"inserted": count}


@router.post("/upload/url_csv_scrape")
async def upload_url_csv_scrape(file: UploadFile = File(...), db=Depends(get_db)):
    import tempfile, shutil, subprocess, sys
    from app.ingestion import load_concerts_csv
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp_in:
        shutil.copyfileobj(file.file, tmp_in)
        input_path = tmp_in.name
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp_out:
        output_path = tmp_out.name
    # Run scraper to transform URL list into concerts CSV
    subprocess.run([sys.executable, "scripts/url_csv_scraper.py", input_path, output_path], check=True)
    count = load_concerts_csv(db, output_path)
    return {"inserted": count}
