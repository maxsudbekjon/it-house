from django.urls import path
from mainapp.views import (
    TopStatisticsListView,
    MediumStatisticsListView,
    NewsListView,
    CompanyListView,
    EducationAboutView,
    CourseAboutView,
    CourseAPIView,
    TechnologyAPIView,
    CourseModuleAPIView,
    ModuleThemeAPIView,
    TeacherAPIView,
    TeacherAchievementAPIView,
    TeacherSkillAPIView,
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('top-statistics', TopStatisticsListView, basename='top-statistics')
router.register('medium-statistics', MediumStatisticsListView, basename='medium-statistics')
router.register('news', NewsListView, basename='news')
router.register('company', CompanyListView, basename='company')
router.register('education-about', EducationAboutView, basename='education-about')
router.register('course-about', CourseAboutView, basename='course-about')
router.register('courses', CourseAPIView, basename='courses')
router.register('teachers', TeacherAPIView, basename='teachers')

urlpatterns = [
    path('technologies/<int:course_id>/', TechnologyAPIView.as_view(), name='technologies'),
    path('course-modules/<int:course_id>/', CourseModuleAPIView.as_view(), name='course-modules'),
    path('module-themes/<int:module_id>/', ModuleThemeAPIView.as_view(), name='module-themes'),
    path('teacher-achievements/<int:teacher_id>/', TeacherAchievementAPIView.as_view(), name='teacher-achievements'),
    path('teacher-skills/<int:teacher_id>/', TeacherSkillAPIView.as_view(), name='teacher-skills'),
] + router.urls