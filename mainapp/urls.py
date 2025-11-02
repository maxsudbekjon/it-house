from django.urls import path
from mainapp.views import (CourseListView, TopStatisticsListView,
                            MediumStatisticsListView, TeacherListView,
                            CourseDetailView, NewsListView, CompanyListView,
                            TeacherDetailView, EducationAboutView, CourseAboutView)

from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'courses', CourseDetailView, basename='course')
router.register(r'top-statistics', TopStatisticsListView, basename='top-statistics')
router.register(r'medium-statistics', MediumStatisticsListView, basename='medium-statistics')
router.register(r'teachers', TeacherListView, basename='teachers')
router.register(r'teachers', TeacherDetailView, basename='teacher-detail')
router.register(r'news', NewsListView, basename='news')
router.register(r'companies', CompanyListView, basename='companies')
router.register(r'education-about', EducationAboutView, basename='education-about')
router.register(r'course-about', CourseAboutView, basename='course-about')  

urlpatterns = [
    path('course-list/', CourseListView.as_view(), name='course-list'),
] + router.urls