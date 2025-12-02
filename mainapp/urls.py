from django.urls import path
from mainapp.views import (
    StatisticsAPIView,
    StatisticsDetailAPIView,
    NewsListView,
    CompanyListView,
    EducationAboutView,
    CourseAboutView,
    CourseAPIView,
    TechnologyAPIView,
    TechnologyDetailAPIView,
    CourseModuleListAPIView,
    CourseModuleAPIView,
    ModuleThemeListAPIView,
    ModuleThemeAPIView,
    TeacherAPIView,
    TeacherAchievementAPIView,
    TeacherAchievementDetailAPIView,
    TeacherSkillAPIView,
    TeacherSkillDetailAPIView,
    StatusAPIView,
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('news', NewsListView, basename='news')
router.register('company', CompanyListView, basename='company')
router.register('education-about', EducationAboutView, basename='education-about')
router.register('course-about', CourseAboutView, basename='course-about')
router.register('courses', CourseAPIView, basename='courses')
router.register('teachers', TeacherAPIView, basename='teachers')
router.register('status', StatusAPIView, basename='status')

urlpatterns = [
    path('statistics/', StatisticsAPIView.as_view(), name='statistics'),
    path('statistics/<int:stat_id>/', StatisticsDetailAPIView.as_view(), name='statistics-detail'),
    path('technologies/<int:course_id>/', TechnologyAPIView.as_view(), name='technologies'),
    path('technologies/<int:course_id>/<int:tech_id>/', TechnologyDetailAPIView.as_view(), name='technology-detail'),
    path('courses/<int:course_id>/modules/', CourseModuleListAPIView.as_view(), name='course-modules-list'),
    path('courses/<int:course_id>/modules/<int:module_id>/', CourseModuleAPIView.as_view(), name='course-modules'),
    path('modules/<int:module_id>/themes/', ModuleThemeListAPIView.as_view(), name='module-themes-list'),
    path('modules/<int:module_id>/themes/<int:theme_id>/', ModuleThemeAPIView.as_view(), name='module-themes'),
    path('teacher/<int:teacher_id>/achievements/', TeacherAchievementAPIView.as_view(), name='teacher-achievements'),
    path('teacher/<int:teacher_id>/achievements/<int:achievement_id>/', TeacherAchievementDetailAPIView.as_view(), name='teacher-achievement-detail'),
    path('teacher/<int:teacher_id>/skills/', TeacherSkillAPIView.as_view(), name='teacher-skills'),
    path('teacher/<int:teacher_id>/skills/<int:skill_id>/', TeacherSkillDetailAPIView.as_view(), name='teacher-skill-detail'),
    
] + router.urls