import os
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from .services import fetch_instagram_posts


class InstagramPostListAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        username = os.getenv("INSTAGRAM_USERNAME", "ithouse_edu")

        try:
            posts = fetch_instagram_posts(username, limit=10)
        except Exception as e:
            return Response(
                {
                    "detail": "Instagramdan post olishda xatolik",
                    "error": str(e),
                },
                status=status.HTTP_502_BAD_GATEWAY,
            )

        return Response(posts, status=status.HTTP_200_OK)
