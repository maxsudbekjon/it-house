from django.contrib import admin
from mainapp.models import (Teacher, Course, CourseAbout, CourseModule,
                            Company, TeacherAchievement, TeacherSkill, Technology,
                            ModuleTheme, Statistics, News, EducationAbout, Status
)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title_uz', 'title_en', 'title_ru', 'duration', 'price')
    search_fields = ('title_uz', 'title_en', 'title_ru')
    list_filter = ('duration', 'price')
@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ('name_uz', 'name_en', 'name_ru')
    search_fields = ('name_uz', 'name_en', 'name_ru')
@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('name_uz', 'name_en', 'name_ru')
    search_fields = ('name_uz', 'name_en', 'name_ru')
@admin.register(CourseModule)
class CourseModuleAdmin(admin.ModelAdmin):
    list_display = ('title_uz', 'course')
    search_fields = ('title_uz', 'title_en', 'title_ru', 'course__title_uz')
    list_filter = ('course',)
@admin.register(CourseAbout)
class CourseAboutAdmin(admin.ModelAdmin):
    list_display = ('title_uz', 'title_en', 'title_ru')
    search_fields = ('title_uz', 'title_en', 'title_ru')
@admin.register(ModuleTheme)
class ModuleThemeAdmin(admin.ModelAdmin):
    list_display = ('title_uz', 'module')
    search_fields = ('title_uz', 'title_en', 'title_ru', 'module__title_uz')
    list_filter = ('module',)
@admin.register(Statistics)
class StatisticsAdmin(admin.ModelAdmin):
    list_display = ('total_students', 'total_graduates', 'total_employed', 'avg_duration', 'avg_start_salary', 'partners')
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('logo', 'workers')
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'profession', 'experience', 'photo')
    search_fields = ('full_name', 'profession')
@admin.register(TeacherAchievement)
class TeacherAchievementAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'title_uz')
@admin.register(TeacherSkill)
class TeacherSkillAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'name_uz')
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title_uz', 'description_uz')
@admin.register(EducationAbout)
class EducationAboutAdmin(admin.ModelAdmin):
    list_display = ('title_uz', 'title_en', 'title_ru')