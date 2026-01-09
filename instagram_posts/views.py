import os
from django.core.cache import cache
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from .services import fetch_instagram_posts


class InstagramPostListAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        username = request.query_params.get(
            "username",
            os.getenv("INSTAGRAM_USERNAME", "ithouse_edu"),
        )
        try:
            limit = int(request.query_params.get("limit", 10))
        except (TypeError, ValueError):
            limit = 10

        cache_ttl = int(os.getenv("INSTAGRAM_CACHE_TTL_SECONDS", "259200"))
        min_interval = int(os.getenv("INSTAGRAM_FETCH_INTERVAL_SECONDS", "259200"))
        cache_key = f"instagram_posts:{username}:{limit}"
        last_fetch_key = f"instagram_posts_last_fetch:{username}"

        cached_posts = cache.get(cache_key)
        if cached_posts is not None:
            return Response(cached_posts, status=status.HTTP_200_OK)

        last_fetch_at = cache.get(last_fetch_key)
        if last_fetch_at is not None:
            seconds_since = (timezone.now() - last_fetch_at).total_seconds()
            if seconds_since < min_interval:
                return Response(
                    {
                        "detail": "So'rovlar cheklangan. Keyinroq urinib ko'ring.",
                    },
                    status=status.HTTP_429_TOO_MANY_REQUESTS,
                )

        try:
            posts = fetch_instagram_posts(username, limit=limit)
        except Exception as e:
            return Response(
                {
                    "detail": "Instagramdan post olishda xatolik",
                    "error": str(e),
                },
                status=status.HTTP_502_BAD_GATEWAY,
            )

        cache.set(cache_key, posts, timeout=cache_ttl)
        cache.set(last_fetch_key, timezone.now(), timeout=cache_ttl)
        return Response(posts, status=status.HTTP_200_OK)
