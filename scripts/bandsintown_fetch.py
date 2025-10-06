import os
import csv
import sys
from urllib.parse import urlencode
import httpx

BANDSINTOWN_APP_ID = os.getenv("BANDSINTOWN_APP_ID", "your-app-name")
API_BASE = "https://rest.bandsintown.com/v3/artists"


def fetch_artist_events(artist_name: str, per_page: int = 50):
    params = {
        "app_id": BANDSINTOWN_APP_ID,
        "per_page": per_page,
    }
    url = f"{API_BASE}/{artist_name}/events?{urlencode(params)}"
    with httpx.Client(timeout=20.0) as client:
        r = client.get(url)
        r.raise_for_status()
        return r.json()


def to_concert_rows(events, artist_name: str):
    rows = []
    for ev in events:
        venue = ev.get("venue", {})
        rows.append({
            "artist_name": artist_name,
            "venue": venue.get("name", ""),
            "city": venue.get("city", ""),
            "country": venue.get("country", ""),
            "event_date": ev.get("datetime", "").split("T")[0] if ev.get("datetime") else "",
            "source": "Bandsintown",
            "url": ev.get("url", ""),
        })
    return rows


def write_csv(rows, out_path: str):
    fieldnames = ["artist_name","venue","city","country","event_date","source","url"]
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow(r)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python scripts/bandsintown_fetch.py \"Artist Name\" data/concerts_bandsintown.csv", file=sys.stderr)
        sys.exit(2)
    artist = sys.argv[1]
    out_csv = sys.argv[2]
    events = fetch_artist_events(artist)
    rows = to_concert_rows(events, artist)
    write_csv(rows, out_csv)
    print(f"Wrote {len(rows)} rows to {out_csv}")
