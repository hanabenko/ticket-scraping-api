import os
import csv
import sys
import json
from datetime import datetime, timedelta
import httpx

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")


def get_spotify_token():
    if not SPOTIFY_CLIENT_ID or not SPOTIFY_CLIENT_SECRET:
        return None
    
    auth_url = "https://accounts.spotify.com/api/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": SPOTIFY_CLIENT_ID,
        "client_secret": SPOTIFY_CLIENT_SECRET
    }
    
    with httpx.Client(timeout=10.0) as client:
        r = client.post(auth_url, data=data)
        r.raise_for_status()
        return r.json().get("access_token")


def fetch_spotify_data(artist_name: str):
    token = get_spotify_token()
    if not token:
        print("Spotify credentials not set, using mock data", file=sys.stderr)
        return [
            {
                "artist": artist_name,
                "platform": "spotify",
                "track": f"{artist_name} - Hit Song",
                "streams": 1250,
                "occurred_at": (datetime.now() - timedelta(hours=2)).isoformat() + "Z",
                "user": "spotify_user_123"
            }
        ]
    
    headers = {"Authorization": f"Bearer {token}"}
    search_url = f"https://api.spotify.com/v1/search?q={artist_name}&type=artist&limit=1"
    
    with httpx.Client(timeout=10.0) as client:
        r = client.get(search_url, headers=headers)
        r.raise_for_status()
        artists = r.json().get("artists", {}).get("items", [])
        
        if not artists:
            return []
        
        artist_id = artists[0]["id"]
        tracks_url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?market=US"
        r = client.get(tracks_url, headers=headers)
        r.raise_for_status()
        tracks = r.json().get("tracks", [])
        
        result = []
        for i, track in enumerate(tracks[:5]):
            result.append({
                "artist": artist_name,
                "platform": "spotify",
                "track": track["name"],
                "streams": track.get("popularity", 0) * 10,
                "occurred_at": datetime.now().isoformat() + "Z",
                "user": f"spotify_user_{i}"
            })
        return result


def fetch_youtube_data(artist_name: str):
    if not YOUTUBE_API_KEY:
        print("YOUTUBE_API_KEY not set, using mock data", file=sys.stderr)
        return [
            {
                "artist": artist_name,
                "platform": "youtube",
                "video": f"{artist_name} - Official Music Video",
                "views": 50000,
                "occurred_at": (datetime.now() - timedelta(hours=1)).isoformat() + "Z",
                "user": "youtube_user_456"
            }
        ]
    return []


def to_interaction_rows(streaming_data):
    rows = []
    for item in streaming_data:
        rows.append({
            "artist_name": item.get("artist"),
            "email": f"{item.get(user)}@{item.get(platform)}.com",
            "interaction_type": "stream",
            "channel": "streaming",
            "occurred_at": item.get("occurred_at"),
            "metadata": {
                "platform": item.get("platform"),
                "track": item.get("track"),
                "video": item.get("video"),
                "streams": item.get("streams"),
                "views": item.get("views"),
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
        print("Usage: python scripts/streaming_scraper.py \"Artist Name\" data/streaming_data.csv", file=sys.stderr)
        sys.exit(2)
    artist = sys.argv[1]
    out_csv = sys.argv[2]
    
    spotify_data = fetch_spotify_data(artist)
    youtube_data = fetch_youtube_data(artist)
    all_data = spotify_data + youtube_data
    
    rows = to_interaction_rows(all_data)
    write_csv(rows, out_csv)
    print(f"Wrote {len(rows)} streaming interactions to {out_csv}")
