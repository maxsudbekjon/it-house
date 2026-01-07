from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from googleapiclient.discovery import build
from django.conf import settings

@extend_schema(tags=['Get Podcasts'])
class LatestPodcastsView(APIView):
    def get(self, request):
        try:
            youtube = build('youtube', 'v3',
                            developerKey=settings.YOUTUBE_API_KEY)

            playlist_response = youtube.playlistItems().list(
                part='snippet',
                playlistId=settings.YOUTUBE_PLAYLIST_ID,
                maxResults=4
            ).execute()

            videos = []
            for item in playlist_response['items']:
                video_id = item['snippet']['resourceId']['videoId']
                videos.append({
                    'title': item['snippet']['title'],
                    'url': f'https://www.youtube.com/watch?v={video_id}',
                    'published': item['snippet']['publishedAt']
                })

            return Response({'videos': videos})

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )




