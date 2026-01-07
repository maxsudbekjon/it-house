import os

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .services import fetch_instagram_posts


class InstagramPostListAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        username = os.getenv("INSTAGRAM_USERNAME")
        if not username:
            return Response(
                {"detail": "INSTAGRAM_USERNAME env var is not set."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        posts = fetch_instagram_posts(username, limit=10)
        return Response(posts, status=status.HTTP_200_OK)
