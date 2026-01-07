from django.urls import path

from .views import InstagramPostListAPIView

urlpatterns = [
    path("instagram-posts/", InstagramPostListAPIView.as_view(), name="instagram-posts"),
]
