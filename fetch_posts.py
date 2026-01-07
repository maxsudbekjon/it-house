import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from instagram_posts.services import fetch_instagram_posts


def main():
    username = os.getenv("INSTAGRAM_USERNAME")
    if not username:
        print("INSTAGRAM_USERNAME env var is not set")
        return
    posts = fetch_instagram_posts(username, limit=10)
    print(f"✅ Instagramdan {len(posts)} ta post olindi")


if __name__ == "__main__":
    main()
