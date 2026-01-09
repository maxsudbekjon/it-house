import instaloader

def get_last_posts(username, limit=10):
    L = instaloader.Instaloader(
        download_pictures=False,
        download_videos=False,
        download_video_thumbnails=False,
        save_metadata=False,
        compress_json=False
    )

    profile = instaloader.Profile.from_username(L.context, username)

    posts_data = []

    for i, post in enumerate(profile.get_posts()):
        if i >= limit:
            break

        posts_data.append({
            "id": post.mediaid,
            "shortcode": post.shortcode,
            "post_url": f"https://www.instagram.com/p/{post.shortcode}/",
            "image_url": post.url,
            "caption": post.caption,
            "timestamp": post.date_utc.isoformat()
        })

    return posts_data


if __name__ == "__main__":
    username = "instagram"  # <-- BU YERGA USERNAME QO'YASIZ
    posts = get_last_posts(username)

    for p in posts:
        print(p)
