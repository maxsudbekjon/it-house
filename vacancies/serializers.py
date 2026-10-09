from rest_framework import serializers

from vacancies.models import Vacancy


class LinesField(serializers.ListField):
    """Newline-separated text in the database, a list of strings in the API."""
    child = serializers.CharField()

    def to_representation(self, value):
        return [line.strip() for line in value.splitlines() if line.strip()]

    def to_internal_value(self, data):
        return '\n'.join(super().to_internal_value(data))


class VacancySerializer(serializers.ModelSerializer):
    requirements_uz = LinesField(allow_empty=False)
    requirements_en = LinesField(allow_empty=False)
    requirements_ru = LinesField(allow_empty=False)

    class Meta:
        model = Vacancy
        fields = [
            'id',
            'title_uz', 'title_ru', 'title_en',
            'employment_type',
            'description_uz', 'description_ru', 'description_en',
            'requirements_uz', 'requirements_ru', 'requirements_en',
            'location_uz', 'location_ru', 'location_en',
            'is_active',
            'created_at',
        ]
