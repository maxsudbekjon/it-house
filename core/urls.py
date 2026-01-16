
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('admin-page-locked/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api-schema-locked', SpectacularAPIView.as_view(), name='schema'),
    path('api-swagger-locked', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/', include('mainapp.urls')),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/podcasts/', include('podcasts.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
