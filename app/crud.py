from __future__ import annotations
from datetime import datetime, date
from typing import Sequence
from sqlalchemy import select, and_
from sqlalchemy.orm import Session
from . import models


def get_or_create_artist(db: Session, name: str) -> models.Artist:
    artist = db.scalar(select(models.Artist).where(models.Artist.name == name))
    if artist:
        return artist
    artist = models.Artist(name=name)
    db.add(artist)
    db.commit()
    db.refresh(artist)
    return artist


def get_or_create_user(db: Session, email: str | None = None) -> models.User:
    if email:
        user = db.scalar(select(models.User).where(models.User.email == email))
        if user:
            return user
    user = models.User(email=email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def bulk_insert_interactions(db: Session, interactions: Sequence[models.Interaction]):
    db.add_all(interactions)
    db.commit()


# Attribution logic (multi-touch with time decay)
DECAY_HALF_LIFE_DAYS = 14.0


def _decay_weight(event_time: datetime, reference_time: datetime) -> float:
    delta_days = (reference_time - event_time).total_seconds() / 86400.0
    if delta_days < 0:
        return 0.0
    return 0.5 ** (delta_days / DECAY_HALF_LIFE_DAYS)


def recompute_attribution_for_user(db: Session, user_id: int, reference_time: datetime | None = None):
    if reference_time is None:
        reference_time = datetime.utcnow()

    rows = db.scalars(select(models.Interaction).where(models.Interaction.user_id == user_id)).all()

    artist_to_score: dict[int, float] = {}
    artist_to_last_touch: dict[int, datetime] = {}

    for it in rows:
        w = _decay_weight(it.occurred_at, reference_time)
        base = 0.0
        if it.interaction_type == "view":
            base = 0.1
        elif it.interaction_type == "click":
            base = 0.5
        elif it.interaction_type == "ticket_purchase":
            base = 5.0
        elif it.interaction_type == "merch_purchase":
            base = 3.0
        elif it.interaction_type == "stream":
            base = 0.2
        elif it.interaction_type.startswith("social_"):
            base = 0.15
        score = base * w
        artist_to_score[it.artist_id] = artist_to_score.get(it.artist_id, 0.0) + score
        if it.artist_id not in artist_to_last_touch or it.occurred_at > artist_to_last_touch[it.artist_id]:
            artist_to_last_touch[it.artist_id] = it.occurred_at

    for artist_id, score in artist_to_score.items():
        attrib = db.scalar(
            select(models.Attribution).where(
                and_(models.Attribution.user_id == user_id, models.Attribution.artist_id == artist_id)
            )
        )
        if attrib is None:
            attrib = models.Attribution(
                user_id=user_id,
                artist_id=artist_id,
                score=score,
                last_touch_at=artist_to_last_touch.get(artist_id),
            )
            db.add(attrib)
        else:
            attrib.score = score
            attrib.last_touch_at = artist_to_last_touch.get(artist_id)
    db.commit()


# Metrics computation (daily rollups)

def compute_daily_metrics_for_date(db: Session, metric_date: date):
    start_dt = datetime.combine(metric_date, datetime.min.time())
    end_dt = datetime.combine(metric_date, datetime.max.time())

    rows = db.scalars(
        select(models.Interaction).where(
            and_(models.Interaction.occurred_at >= start_dt, models.Interaction.occurred_at <= end_dt)
        )
    ).all()

    counters: dict[int, dict[str, int]] = {}
    for it in rows:
        c = counters.setdefault(it.artist_id, {
            "views": 0, "clicks": 0, "ticket_purchases": 0, "merch_purchases": 0, "streams": 0
        })
        if it.interaction_type == "view":
            c["views"] += 1
        elif it.interaction_type == "click":
            c["clicks"] += 1
        elif it.interaction_type == "ticket_purchase":
            c["ticket_purchases"] += 1
        elif it.interaction_type == "merch_purchase":
            c["merch_purchases"] += 1
        elif it.interaction_type == "stream":
            c["streams"] += 1

    for artist_id, vals in counters.items():
        views = vals["views"]
        clicks = vals["clicks"]
        ticket = vals["ticket_purchases"]
        merch = vals["merch_purchases"]
        streams = vals["streams"]

        ctr = (clicks / views) if views > 0 else None
        ticket_conv = (ticket / clicks) if clicks > 0 else None
        merch_conv = (merch / clicks) if clicks > 0 else None
        stream_lift = (streams / clicks) if clicks > 0 else None

        rec = db.scalar(
            select(models.ArtistDailyMetrics).where(
                and_(models.ArtistDailyMetrics.artist_id == artist_id, models.ArtistDailyMetrics.metric_date == metric_date)
            )
        )
        if rec is None:
            rec = models.ArtistDailyMetrics(
                artist_id=artist_id,
                metric_date=metric_date,
                views=views,
                clicks=clicks,
                ticket_purchases=ticket,
                merch_purchases=merch,
                streams=streams,
                ctr=ctr,
                ticket_conversion_rate=ticket_conv,
                merch_conversion_rate=merch_conv,
                stream_lift=stream_lift,
            )
            db.add(rec)
        else:
            rec.views = views
            rec.clicks = clicks
            rec.ticket_purchases = ticket
            rec.merch_purchases = merch
            rec.streams = streams
            rec.ctr = ctr
            rec.ticket_conversion_rate = ticket_conv
            rec.merch_conversion_rate = merch_conv
            rec.stream_lift = stream_lift
    db.commit()
