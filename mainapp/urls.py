from django.urls import path
from mainapp.views import (CourseListView, TechnologyListView,
                            CourseModuleListView, ModuleThemeListView,
                            TopStatisticsListView, MediumStatisticsListView,
                            TeacherListView, TeacherAchievementListView,
                            TeacherSkillListView, CourseDetailView)

from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'courses', CourseDetailView, basename='course')
router.register(r'technologies', TechnologyListView, basename='technology')
router.register(r'course-modules', CourseModuleListView, basename='course-module')
router.register(r'module-themes', ModuleThemeListView, basename='module-theme')
router.register(r'top-statistics', TopStatisticsListView, basename='top-statistics')
router.register(r'medium-statistics', MediumStatisticsListView, basename='medium-statistics')
router.register(r'teachers', TeacherListView, basename='teachers')
router.register(r'teacher-achievements', TeacherAchievementListView, basename='teacher-achievements')
router.register(r'teacher-skills', TeacherSkillListView, basename='teacher-skills')

urlpatterns = [
    path('course-list/', CourseListView.as_view(), name='course-list'),
] + router.urls