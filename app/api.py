from fastapi import APIRouter, HTTPException, Body, Query, Depends
from typing import List, Optional
import json
import httpx
from bs4 import BeautifulSoup
from .settings import settings
from .db import get_db
from .crud import (
    create_interaction, 
    get_top_artists_by_attribution, 
    get_artist_metrics,
    compute_daily_metrics_for_date
)
from sqlalchemy.orm import Session
from datetime import datetime
from urllib.parse import urljoin, urlparse

router = APIRouter()

@router.get("/test")
async def test():
    return {"message": "TicketScrapingApp API is working!"}

# Scraping endpoints
@router.get("/scrape/seatgeek")
async def scrape_seatgeek(
    query: str = Query(..., description="Artist, team, or event search query"),
    per_page: int = Query(20, ge=1, le=100),
    page: int = Query(1, ge=1),
    client_id: Optional[str] = Query(None, description="SeatGeek client_id if required")
):
    params = {"q": query, "per_page": per_page, "page": page}
    cid = client_id or settings.seatgeek_client_id
    if cid:
        params["client_id"] = cid
    url = "https://api.seatgeek.com/2/events"
    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.get(url, params=params)
    if r.status_code != 200:
        raise HTTPException(status_code=r.status_code, detail=r.text)
    data = r.json()
    results = []
    for ev in data.get("events", []):
        performers = [p.get("name") for p in ev.get("performers", []) if p.get("name")]
        venue = ev.get("venue") or {}
        results.append({
            "id": ev.get("id"),
            "title": ev.get("title"),
            "datetime_local": ev.get("datetime_local"),
            "url": ev.get("url"),
            "performers": performers,
            "venue": {
                "name": venue.get("name"),
                "city": venue.get("city"),
                "state": venue.get("state"),
                "country": venue.get("country"),
            }
        })
    return {"count": len(results), "events": results}

@router.get("/scrape/url")
async def scrape_url(url: str = Query(..., description="Event page URL to scrape")):
    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.get(url, headers={"User-Agent": "Mozilla/5.0"})
    if r.status_code != 200:
        raise HTTPException(status_code=r.status_code, detail=f"Fetch failed: {r.text[:200]}")
    soup = BeautifulSoup(r.text, "lxml")
    events = []
    for tag in soup.find_all("script", type="application/ld+json"):
        try:
            payload = json.loads(tag.string or tag.text or "{}")
        except Exception:
            continue
        items = payload if isinstance(payload, list) else [payload]
        for item in items:
            if isinstance(item, dict) and item.get("@type") in ("Event", ["Event"]):
                events.append({
                    "name": item.get("name"),
                    "startDate": item.get("startDate"),
                    "location": (item.get("location") or {}).get("name") if isinstance(item.get("location"), dict) else item.get("location"),
                    "offers": item.get("offers"),
                    "raw": item,
                })
    return {"count": len(events), "events": events}

@router.post("/scrape/urls")
async def scrape_urls(urls: List[str] = Body(..., embed=True)):
    out = []
    async with httpx.AsyncClient(timeout=20) as client:
        for url in urls:
            try:
                r = await client.get(url, headers={"User-Agent": "Mozilla/5.0"})
                if r.status_code != 200:
                    out.append({"url": url, "error": f"status {r.status_code}"})
                    continue
                soup = BeautifulSoup(r.text, "lxml")
                found = 0
                for tag in soup.find_all("script", type="application/ld+json"):
                    try:
                        payload = json.loads(tag.string or tag.text or "{}")
                    except Exception:
                        continue
                    items = payload if isinstance(payload, list) else [payload]
                    for item in items:
                        if isinstance(item, dict) and item.get("@type") in ("Event", ["Event"]):
                            found += 1
                out.append({"url": url, "events_found": found})
            except Exception as e:
                out.append({"url": url, "error": str(e)})
    return {"results": out}

@router.get("/scrape/discover")
async def scrape_discover(
    url: str = Query(..., description="Seed page URL; we will crawl same-domain links to find Event JSON-LD"),
    max_pages: int = Query(10, ge=1, le=50)
):
    async with httpx.AsyncClient(timeout=20) as client:
        # fetch seed
        r = await client.get(url, headers={"User-Agent": "Mozilla/5.0"})
        if r.status_code != 200:
            raise HTTPException(status_code=r.status_code, detail=f"Seed fetch failed: {r.text[:200]}")
        soup = BeautifulSoup(r.text, "lxml")
        # collect same-origin links
        origin = urlparse(url).netloc
        hrefs = []
        for a in soup.find_all("a", href=True):
            href = a.get("href")
            abs_url = urljoin(url, href)
            if urlparse(abs_url).netloc == origin:
                hrefs.append(abs_url)
        # de-dup and cap
        seen = set()
        crawl = []
        for h in hrefs:
            if h not in seen:
                seen.add(h)
                crawl.append(h)
            if len(crawl) >= max_pages:
                break
        # visit and extract events
        found = []
        for link in crawl:
            try:
                rr = await client.get(link, headers={"User-Agent": "Mozilla/5.0"})
                if rr.status_code != 200:
                    continue
                psoup = BeautifulSoup(rr.text, "lxml")
                for tag in psoup.find_all("script", type="application/ld+json"):
                    try:
                        payload = json.loads(tag.string or tag.text or "{}")
                    except Exception:
                        continue
                    items = payload if isinstance(payload, list) else [payload]
                    for item in items:
                        if isinstance(item, dict) and item.get("@type") in ("Event", ["Event"]):
                            found.append({
                                "source": link,
                                "name": item.get("name"),
                                "startDate": item.get("startDate"),
                                "location": (item.get("location") or {}).get("name") if isinstance(item.get("location"), dict) else item.get("location"),
                                "raw": item,
                            })
            except Exception:
                continue
    return {"seed": url, "scanned": len(crawl), "events": found}

# Data pipeline endpoints
@router.post("/interactions")
async def create_user_interaction(
    user_id: str = Body(..., embed=True),
    artist_name: str = Body(..., embed=True),
    interaction_type: str = Body(..., embed=True),
    channel: str = Body(..., embed=True),
    value: Optional[float] = Body(None, embed=True),
    concert_id: Optional[int] = Body(None, embed=True),
    metadata: Optional[dict] = Body(None, embed=True),
    db: Session = Depends(get_db)
):
    """Create a new user interaction"""
    interaction = create_interaction(
        db=db,
        user_id=user_id,
        artist_name=artist_name,
        interaction_type=interaction_type,
        channel=channel,
        value=value,
        concert_id=concert_id,
        metadata=metadata
    )
    return {
        "id": interaction.id,
        "user_id": user_id,
        "artist_name": artist_name,
        "interaction_type": interaction_type,
        "channel": channel,
        "timestamp": interaction.timestamp.isoformat()
    }

@router.get("/insights/top-artists")
async def get_top_artists(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Get top artists by attribution score"""
    artists = get_top_artists_by_attribution(db, limit)
    return {"top_artists": artists}

@router.get("/insights/artist/{artist_name}")
async def get_artist_insights(
    artist_name: str,
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db)
):
    """Get comprehensive metrics for a specific artist"""
    metrics = get_artist_metrics(db, artist_name, days)
    if not metrics:
        raise HTTPException(status_code=404, detail=f"Artist '{artist_name}' not found")
    return metrics

@router.post("/metrics/compute")
async def compute_metrics(
    date: Optional[str] = Body(None, embed=True),
    db: Session = Depends(get_db)
):
    """Compute daily metrics for all artists"""
    target_date = datetime.fromisoformat(date) if date else datetime.utcnow()
    compute_daily_metrics_for_date(db, target_date)
    return {"message": f"Metrics computed for {target_date.date()}", "date": target_date.isoformat()}
