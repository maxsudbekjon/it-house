from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from mainapp.views import IsSuperUser
from vacancies.models import Vacancy
from vacancies.serializers import VacancySerializer


class VacancyViewSet(ModelViewSet):
    serializer_class = VacancySerializer

    def get_queryset(self):
        queryset = Vacancy.objects.all()
        # Superusers manage hidden vacancies too; everyone else sees only active ones.
        if not IsSuperUser().has_permission(self.request, self):
            queryset = queryset.filter(is_active=True)
        return queryset

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsSuperUser]
        return super().get_permissions()
