from datetime import datetime, timezone as dt_timezone
import os

import instaloader
import requests
from django.utils import timezone as dj_timezone


def _extract_caption(node):
    edges = node.get("edge_media_to_caption", {}).get("edges", [])
    if not edges:
        return ""
    return edges[0].get("node", {}).get("text", "")


def _parse_timestamp(node):
    ts = node.get("taken_at_timestamp")
    if not ts:
        return dj_timezone.now()
    return datetime.fromtimestamp(ts, tz=dt_timezone.utc)


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


def _init_loader():
    loader = instaloader.Instaloader(
        download_pictures=False,
        download_videos=False,
        download_video_thumbnails=False,
        save_metadata=False,
        compress_json=False,
    )

    if os.getenv("INSTAGRAM_DISABLE_LOGIN", "0") == "1":
        return loader

    login_username = os.getenv("INSTAGRAM_LOGIN_USERNAME")
    login_password = os.getenv("INSTAGRAM_LOGIN_PASSWORD")
    session_file = os.getenv("INSTAGRAM_SESSION_FILE")

    if login_username and session_file:
        try:
            loader.load_session_from_file(login_username, session_file)
            return loader
        except Exception:
            pass

    if login_username and login_password:
        loader.login(login_username, login_password)
        if session_file:
            try:
                loader.save_session_to_file(session_file)
            except Exception:
                pass

    return loader




def fetch_instagram_posts(username: str, limit: int = 10):
    if os.getenv("INSTAGRAM_DISABLE_LOGIN", "0") == "1":
        loader = instaloader.Instaloader(
            download_pictures=False,
            download_videos=False,
            download_video_thumbnails=False,
            save_metadata=False,
            compress_json=False,
        )
    else:
        loader = _init_loader()

    profile = instaloader.Profile.from_username(loader.context, username)
    posts = []

    for index, post in enumerate(profile.get_posts()):
        if index >= limit:
            break

        posts.append(
            {
                "instagram_id": post.mediaid,
                "caption": post.caption or "",
                "media_url": post.url,
                "permalink": f"https://www.instagram.com/p/{post.shortcode}/",
                "media_type": "VIDEO" if post.is_video else "IMAGE",
                "posted_at": post.date_utc.astimezone(dt_timezone.utc),
                "likes": post.likes,
                "comments": post.comments,
            }
        )

    return posts
