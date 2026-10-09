from rest_framework.routers import SimpleRouter

from vacancies.views import VacancyViewSet

router = SimpleRouter()
router.register('', VacancyViewSet, basename='vacancies')

urlpatterns = router.urls
