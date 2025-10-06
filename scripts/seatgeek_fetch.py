import os
import csv
import sys
from urllib.parse import urlencode
import httpx

SEATGEEK_CLIENT_ID = os.getenv("SEATGEEK_CLIENT_ID")
API_BASE = "https://api.seatgeek.com/2"


def _check_client():
    if not SEATGEEK_CLIENT_ID:
        print("SEATGEEK_CLIENT_ID not set", file=sys.stderr)
        sys.exit(1)


def fetch_events_by_query(artist_query: str, per_page: int = 50):
    _check_client()
    params = {
        "q": artist_query,
        "taxonomies.name": "concert",
        "per_page": per_page,
        "client_id": SEATGEEK_CLIENT_ID,
    }
    url = f"{API_BASE}/events?{urlencode(params)}"
    with httpx.Client(timeout=20.0, follow_redirects=True) as client:
        r = client.get(url)
        r.raise_for_status()
        return r.json().get("events", [])


def search_performers(artist_query: str, per_page: int = 5):
    _check_client()
    params = {
        "q": artist_query,
        "per_page": per_page,
        "client_id": SEATGEEK_CLIENT_ID,
    }
    url = f"{API_BASE}/performers?{urlencode(params)}"
    with httpx.Client(timeout=20.0, follow_redirects=True) as client:
        r = client.get(url)
        r.raise_for_status()
        return r.json().get("performers", [])


def fetch_events_by_performer_id(performer_id: int, per_page: int = 50):
    _check_client()
    params = {
        "performers.id": performer_id,
        "taxonomies.name": "concert",
        "per_page": per_page,
        "client_id": SEATGEEK_CLIENT_ID,
    }
    url = f"{API_BASE}/events?{urlencode(params)}"
    with httpx.Client(timeout=20.0, follow_redirects=True) as client:
        r = client.get(url)
        r.raise_for_status()
        return r.json().get("events", [])


def to_concert_rows(events):
    rows = []
    for ev in events:
        performers = ev.get("performers") or []
        artist_name = None
        if performers:
            artist_name = performers[0].get("name")
        venue = (ev.get("venue") or {})
        rows.append({
            "artist_name": artist_name or "",
            "venue": venue.get("name") or "",
            "city": venue.get("city") or "",
            "state": venue.get("state") or venue.get("state_code") or "",
            "postal_code": venue.get("postal_code") or "",
            "country": venue.get("country") or venue.get("country_code") or "",
            "event_date": (ev.get("datetime_local") or "").split("T")[0] if ev.get("datetime_local") else "",
            "source": "SeatGeek",
            "url": ev.get("url") or "",
        })
    return rows


def write_csv(rows, out_path: str):
    fieldnames = [
        "artist_name","venue","city","state","postal_code","country","event_date","source","url"
    ]
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow(r)


def main():
    if len(sys.argv) < 3:
        print("Usage: SEATGEEK_CLIENT_ID=... python scripts/seatgeek_fetch.py \"Artist Name\" data/concerts_seatgeek.csv", file=sys.stderr)
        sys.exit(2)
    artist = sys.argv[1]
    out_csv = sys.argv[2]

    # First try query
    events = fetch_events_by_query(artist)
    # Fallback to performer search -> events by performer id
    if not events:
        performers = search_performers(artist)
        if performers:
            pid = performers[0].get("id")
            if pid:
                events = fetch_events_by_performer_id(pid)

    rows = to_concert_rows(events)
    write_csv(rows, out_csv)
    print(f"Wrote {len(rows)} rows to {out_csv}")


if __name__ == "__main__":
    main()
