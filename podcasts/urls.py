from django.urls import path
from .views import LatestPodcastsView

urlpatterns = [
    path('latest/', LatestPodcastsView.as_view()),
]

