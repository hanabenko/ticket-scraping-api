from fastapi import APIRouter, HTTPException, Body, Query
from typing import List, Optional
import json
import httpx
from bs4 import BeautifulSoup
from .settings import settings

router = APIRouter()

@router.get("/test")
async def test():
    return {"message": "TicketScrapingApp API is working!"}

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
