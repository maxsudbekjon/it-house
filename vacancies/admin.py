from django.contrib import admin
from django.utils import timezone

from vacancies.models import Vacancy


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ('title_uz', 'employment_type', 'location_uz', 'is_active', 'created_at')
    list_editable = ('is_active',)
    list_filter = ('is_active', 'employment_type')
    search_fields = ('title_uz', 'title_en', 'title_ru')
    actions = ('activate', 'deactivate')
    fieldsets = (
        (None, {'fields': ('employment_type', 'is_active')}),
        ("O'zbekcha", {'fields': ('title_uz', 'description_uz', 'requirements_uz', 'location_uz')}),
        ('Русский', {'fields': ('title_ru', 'description_ru', 'requirements_ru', 'location_ru')}),
        ('English', {'fields': ('title_en', 'description_en', 'requirements_en', 'location_en')}),
    )

    @admin.action(description='Activate selected vacancies')
    def activate(self, request, queryset):
        updated = queryset.update(is_active=True, updated_at=timezone.now())
        self.message_user(request, f'Activated vacancies: {updated}.')

    @admin.action(description='Deactivate selected vacancies')
    def deactivate(self, request, queryset):
        updated = queryset.update(is_active=False, updated_at=timezone.now())
        self.message_user(request, f'Deactivated vacancies: {updated}.')
