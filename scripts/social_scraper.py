import os
import csv
import sys
import json
from datetime import datetime, timedelta
import httpx

TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
INSTAGRAM_ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN")


def fetch_twitter_mentions(artist_name: str, days_back: int = 7):
    if not TWITTER_BEARER_TOKEN:
        print("TWITTER_BEARER_TOKEN not set, using mock data", file=sys.stderr)
        return [
            {
                "artist": artist_name,
                "platform": "twitter",
                "action": "mention",
                "content": f"Just saw {artist_name} live! Amazing show!",
                "user": "fan123",
                "occurred_at": (datetime.now() - timedelta(days=1)).isoformat() + "Z",
                "engagement": {"likes": 5, "retweets": 2, "replies": 1}
            }
        ]
    return []


def fetch_instagram_posts(artist_name: str, days_back: int = 7):
    if not INSTAGRAM_ACCESS_TOKEN:
        print("INSTAGRAM_ACCESS_TOKEN not set, using mock data", file=sys.stderr)
        return [
            {
                "artist": artist_name,
                "platform": "instagram",
                "action": "post",
                "content": f"Fan photo with {artist_name}",
                "user": "fan456",
                "occurred_at": (datetime.now() - timedelta(days=2)).isoformat() + "Z",
                "engagement": {"likes": 15, "comments": 3}
            }
        ]
    return []


def to_interaction_rows(social_data):
    rows = []
    for item in social_data:
        action_map = {
            "mention": "social_comment",
            "post": "social_like",
            "like": "social_like",
            "share": "social_share"
        }
        interaction_type = action_map.get(item.get("action"), "social_like")
        
        rows.append({
            "artist_name": item.get("artist"),
            "email": f"{item.get(user)}@{item.get(platform)}.com",
            "interaction_type": interaction_type,
            "channel": "social",
            "occurred_at": item.get("occurred_at"),
            "metadata": {
                "platform": item.get("platform"),
                "content": item.get("content"),
                "engagement": item.get("engagement", {}),
                "user": item.get("user")
            }
        })
    return rows


def write_csv(rows, out_path: str):
    fieldnames = ["artist_name","email","interaction_type","channel","occurred_at","metadata"]
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            r["metadata"] = json.dumps(r["metadata"])
            w.writerow(r)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python scripts/social_scraper.py \"Artist Name\" data/social_data.csv", file=sys.stderr)
        sys.exit(2)
    artist = sys.argv[1]
    out_csv = sys.argv[2]
    
    twitter_data = fetch_twitter_mentions(artist)
    instagram_data = fetch_instagram_posts(artist)
    all_data = twitter_data + instagram_data
    
    rows = to_interaction_rows(all_data)
    write_csv(rows, out_csv)
    print(f"Wrote {len(rows)} social interactions to {out_csv}")
