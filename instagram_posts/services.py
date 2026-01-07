from datetime import datetime

import requests
from django.utils import timezone


def _extract_caption(node):
    edges = node.get("edge_media_to_caption", {}).get("edges", [])
    if not edges:
        return ""
    return edges[0].get("node", {}).get("text", "")


def _parse_timestamp(node):
    ts = node.get("taken_at_timestamp")
    if not ts:
        return timezone.now()
    return datetime.fromtimestamp(ts, tz=timezone.utc)


def fetch_instagram_posts(username, limit=10):
    url = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={username}"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/123.0.0.0 Safari/537.36"
        ),
        "Accept": "application/json",
    }
    response = requests.get(url, headers=headers, timeout=15)
    response.raise_for_status()
    data = response.json()
    edges = (
        data.get("data", {})
        .get("user", {})
        .get("edge_owner_to_timeline_media", {})
        .get("edges", [])
    )

    posts = []
    for edge in edges[:limit]:
        node = edge.get("node", {})
        shortcode = node.get("shortcode")
        posts.append(
            {
                "instagram_id": node.get("id", ""),
                "caption": _extract_caption(node),
                "media_url": node.get("display_url", ""),
                "permalink": f"https://www.instagram.com/p/{shortcode}/" if shortcode else "",
                "media_type": node.get("__typename", ""),
                "posted_at": _parse_timestamp(node),
            }
        )

    return [post for post in posts if post.get("instagram_id") and post.get("media_url")]
