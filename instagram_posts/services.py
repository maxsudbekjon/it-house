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


def _build_headers(username):
    return {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/123.0.0.0 Safari/537.36"
        ),
        "Accept": "application/json",
        "Referer": f"https://www.instagram.com/{username}/",
    }


def _extract_edges_from_payload(data):
    if "data" in data:
        return (
            data.get("data", {})
            .get("user", {})
            .get("edge_owner_to_timeline_media", {})
            .get("edges", [])
        )
    return (
        data.get("graphql", {})
        .get("user", {})
        .get("edge_owner_to_timeline_media", {})
        .get("edges", [])
    )


def _request_profile_json(username, timeout=15):
    headers = _build_headers(username)
    profile_url = f"https://www.instagram.com/{username}/"

    endpoints = [
        f"https://www.instagram.com/api/v1/users/web_profile_info/?username={username}",
        f"{profile_url}?__a=1&__d=dis",
    ]

    for url in endpoints:
        response = requests.get(url, headers=headers, timeout=timeout)
        if response.status_code >= 400:
            continue
        try:
            payload = response.json()
        except ValueError:
            continue
        edges = _extract_edges_from_payload(payload)
        if edges:
            return edges
    return []


import instaloader
from datetime import datetime
from django.utils import timezone


def fetch_instagram_posts(username: str, limit: int = 10):
    loader = instaloader.Instaloader(
        download_pictures=False,
        download_videos=False,
        download_video_thumbnails=False,
        save_metadata=False,
        compress_json=False,
    )

    profile = instaloader.Profile.from_username(
        loader.context, username
    )

    posts = []

    for post in profile.get_posts():
        posts.append(
            {
                "instagram_id": post.mediaid,
                "caption": post.caption or "",
                "media_url": post.url,
                "permalink": f"https://www.instagram.com/p/{post.shortcode}/",
                "media_type": "VIDEO" if post.is_video else "IMAGE",
                "posted_at": post.date_utc.astimezone(timezone.utc),
                "likes": post.likes,
                "comments": post.comments,
            }
        )

        if len(posts) >= limit:
            break

    return posts
