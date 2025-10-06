from __future__ import annotations
from typing import Any, Iterable, Dict
from .base import read_json_file

# Map social actions to interaction types
SOCIAL_TYPE_MAP = {
    "like": "social_like",
    "comment": "social_comment",
    "share": "social_share",
}

def load_social_file(path: str) -> Iterable[Dict[str, Any]]:
    data = read_json_file(path)
    for row in data:
        itype = SOCIAL_TYPE_MAP.get(row.get("action"), "social_like")
        yield {
            "artist_name": row.get("artist"),
            "email": row.get("email"),
            "interaction_type": itype,
            "channel": row.get("channel", "social"),
            "occurred_at": row.get("occurred_at"),
            "metadata": {k: v for k, v in row.items() if k not in {"artist","email","occurred_at","channel","action"}},
        }


from .base import fetch_json_http_sync


def load_social_http(url: str):
    data = fetch_json_http_sync(url)
    if isinstance(data, dict):
        payload = data.get(data) or data.get(items) or data.get(events) or data.get(rows) or []
    else:
        payload = data
    for row in payload:
        yield {
            artist_name: row.get(artist) or row.get(artist_name),
            email: row.get(email),
            interaction_type: (row.get(type) or row.get(interaction_type) or (stream if social==streaming else click)),
            channel: row.get(channel) or social,
            occurred_at: row.get(occurred_at) or row.get(timestamp),
            metadata: {k: v for k, v in row.items() if k not in {artist,artist_name,email,type,interaction_type,occurred_at,timestamp,channel}},
        }
