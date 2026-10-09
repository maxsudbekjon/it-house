from django.db import models

from mainapp.models import BaseModel


class Vacancy(BaseModel):
    class EmploymentType(models.TextChoices):
        FULL_TIME = 'full_time', 'Full-time'
        PART_TIME = 'part_time', 'Part-time'
        INTERNSHIP = 'internship', 'Internship'
        CONTRACT = 'contract', 'Contract'

    title_uz = models.CharField(max_length=255)
    title_en = models.CharField(max_length=255)
    title_ru = models.CharField(max_length=255)
    employment_type = models.CharField(max_length=20, choices=EmploymentType.choices)
    description_uz = models.TextField()
    description_en = models.TextField()
    description_ru = models.TextField()
    requirements_uz = models.TextField(help_text="One requirement per line")
    requirements_en = models.TextField(help_text="One requirement per line")
    requirements_ru = models.TextField(help_text="One requirement per line")
    location_uz = models.CharField(max_length=255)
    location_en = models.CharField(max_length=255)
    location_ru = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True, help_text="Only active vacancies are shown on the website")

    class Meta:
        ordering = ['-created_at', '-id']
        verbose_name_plural = 'vacancies'
        indexes = [
            models.Index(fields=['is_active', '-created_at'], name='vacancy_active_created_idx'),
        ]

    def __str__(self):
        return self.title_uz
