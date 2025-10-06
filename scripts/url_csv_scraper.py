import sys
import csv
import json
import httpx
from bs4 import BeautifulSoup
from urllib.parse import urlparse

# Input CSV columns: url[, artist_hint]
# Output CSV columns (concerts.csv schema): artist_name,venue,city,country,event_date,source,url

FIELDS = ["artist_name","venue","city","country","event_date","source","url"]


def fetch_page(url: str) -> str:
    headers = {"User-Agent": "Mozilla/5.0 (compatible; TicketScrapingApp/1.0)"}
    with httpx.Client(timeout=20.0, headers=headers, follow_redirects=True) as client:
        r = client.get(url)
        r.raise_for_status()
        return r.text


def parse_event_from_html(html: str, page_url: str, artist_hint: str | None = None) -> dict | None:
    soup = BeautifulSoup(html, "lxml")
    # Look for JSON-LD scripts
    for tag in soup.find_all("script", type=lambda t: t and "ld+json" in t):
        try:
            data = json.loads(tag.string or "{}")
        except json.JSONDecodeError:
            continue
        # Normalize into list
        candidates = data if isinstance(data, list) else [data]
        for obj in candidates:
            t = obj.get("@type")
            if t == "Event" or (isinstance(t, list) and "Event" in t):
                name = obj.get("name")
                start_date = (obj.get("startDate") or obj.get("start_date") or "").split("T")[0]
                location = obj.get("location") or {}
                if isinstance(location, dict):
                    venue = location.get("name") or ""
                    addr = location.get("address") or {}
                    if isinstance(addr, dict):
                        city = addr.get("addressLocality") or ""
                        country = addr.get("addressCountry") or ""
                    else:
                        city = ""
                        country = ""
                else:
                    venue = ""
                    city = ""
                    country = ""
                # Artist/performer
                performer = obj.get("performer") or obj.get("performers") or []
                artist_name = artist_hint or ""
                if not artist_name:
                    if isinstance(performer, list) and performer:
                        if isinstance(performer[0], dict):
                            artist_name = performer[0].get("name") or ""
                        else:
                            artist_name = str(performer[0])
                    elif isinstance(performer, dict):
                        artist_name = performer.get("name") or ""
                source = urlparse(page_url).netloc
                return {
                    "artist_name": artist_name or name or "",
                    "venue": venue or "",
                    "city": city or "",
                    "country": country or "",
                    "event_date": start_date or "",
                    "source": source or "",
                    "url": page_url,
                }
    return None


def run(input_csv: str, output_csv: str):
    rows_out = []
    with open(input_csv, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for rec in reader:
            url = rec.get("url")
            if not url:
                continue
            artist_hint = rec.get("artist_hint")
            try:
                html = fetch_page(url)
                event = parse_event_from_html(html, url, artist_hint)
                if event:
                    rows_out.append(event)
            except Exception:
                continue
    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for r in rows_out:
            w.writerow(r)
    print(f"Wrote {len(rows_out)} rows to {output_csv}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python scripts/url_csv_scraper.py input_urls.csv data/concerts_scraped.csv", file=sys.stderr)
        sys.exit(2)
    run(sys.argv[1], sys.argv[2])
