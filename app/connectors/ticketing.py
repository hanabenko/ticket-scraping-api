from __future__ import annotations
from typing import Any, Iterable, Dict
from .base import read_json_file

# Expected schema example (list of events):
# {"artist": "The Echoes", "email": "alice@example.com", "type": "click|ticket_purchase", "occurred_at": "2025-10-01T10:05:00Z", "channel": "ticketing"}

def load_ticketing_file(path: str) -> Iterable[Dict[str, Any]]:
    data = read_json_file(path)
    for row in data:
        yield {
            "artist_name": row.get("artist"),
            "email": row.get("email"),
            "interaction_type": row.get("type"),
            "channel": row.get("channel", "ticketing"),
            "occurred_at": row.get("occurred_at"),
            "metadata": {k: v for k, v in row.items() if k not in {"artist","email","type","occurred_at","channel"}},
        }


from .base import fetch_json_http_sync


def load_ticketing_http(url: str):
    data = fetch_json_http_sync(url)
    if isinstance(data, dict):
        payload = data.get(data) or data.get(items) or data.get(events) or data.get(rows) or []
    else:
        payload = data
    for row in payload:
        yield {
            artist_name: row.get(artist) or row.get(artist_name),
            email: row.get(email),
            interaction_type: (row.get(type) or row.get(interaction_type) or (stream if ticketing==streaming else click)),
            channel: row.get(channel) or ticketing,
            occurred_at: row.get(occurred_at) or row.get(timestamp),
            metadata: {k: v for k, v in row.items() if k not in {artist,artist_name,email,type,interaction_type,occurred_at,timestamp,channel}},
        }
