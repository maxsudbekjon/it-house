from django.urls import path
from mainapp.views import (
    StatisticsAPIView,
    NewsListView,
    CompanyListView,
    EducationAboutView,
    CourseAboutView,
    CourseAPIView,
    TechnologyAPIView,
    CourseModuleListAPIView,
    CourseModuleAPIView,
    ModuleThemeListAPIView,
    ModuleThemeAPIView,
    TeacherAPIView,
    TeacherAchievementAPIView,
    TeacherSkillAPIView,
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('news', NewsListView, basename='news')
router.register('company', CompanyListView, basename='company')
router.register('education-about', EducationAboutView, basename='education-about')
router.register('course-about', CourseAboutView, basename='course-about')
router.register('courses', CourseAPIView, basename='courses')
router.register('teachers', TeacherAPIView, basename='teachers')

urlpatterns = [
    path('statistics/', StatisticsAPIView.as_view(), name='statistics'),
    path('technologies/<int:course_id>/', TechnologyAPIView.as_view(), name='technologies'),
    path('courses/<int:course_id>/modules/', CourseModuleListAPIView.as_view(), name='course-modules-list'),
    path('courses/<int:course_id>/modules/<int:module_id>/', CourseModuleAPIView.as_view(), name='course-modules'),
    path('modules/<int:module_id>/themes/', ModuleThemeListAPIView.as_view(), name='module-themes-list'),
    path('modules/<int:module_id>/themes/<int:theme_id>/', ModuleThemeAPIView.as_view(), name='module-themes'),
    path('teacher-achievements/<int:teacher_id>/', TeacherAchievementAPIView.as_view(), name='teacher-achievements'),
    path('teacher-skills/<int:teacher_id>/', TeacherSkillAPIView.as_view(), name='teacher-skills'),
] + router.urls