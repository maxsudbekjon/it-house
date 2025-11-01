from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from mainapp.serializers import (CourseSerializer, TechnologySerializer,
                                 CourseModuleSerializer, ModuleThemeSerializer,
                                TopStatisticsSerializer, MediumStatisticsSerializer,
                                TeacherSerializer, TeacherAchievementSerializer,
                                TeacherSkillSerializer, CourseListSerializer, NewsSerializer,
                                CompanySerializer, TeacherListSerializer, EducationAboutSerializer,
                                CourseAboutSerializer)
from mainapp.models import (Course, Technology, CourseModule, ModuleTheme, Company, EducationAbout,
                            Statistics, Teacher, TeacherAchievement, TeacherSkill, News, CourseAbout)



class CourseListView(ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseListSerializer

class CourseDetailView(RetrieveModelMixin, GenericViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class TechnologyListView(ReadOnlyModelViewSet):
    queryset = Technology.objects.all()
    serializer_class = TechnologySerializer


class CourseModuleListView(ReadOnlyModelViewSet):
    queryset = CourseModule.objects.all()
    serializer_class = CourseModuleSerializer


class ModuleThemeListView(ReadOnlyModelViewSet):
    queryset = ModuleTheme.objects.all()
    serializer_class = ModuleThemeSerializer


class TopStatisticsListView(ListModelMixin, GenericViewSet):
    queryset = Statistics.objects.all()
    serializer_class = TopStatisticsSerializer


class MediumStatisticsListView(ListModelMixin, GenericViewSet):
    queryset = Statistics.objects.all()
    serializer_class = MediumStatisticsSerializer


class TeacherListView(ListModelMixin, GenericViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherListSerializer


class TeacherDetailView(RetrieveModelMixin, GenericViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer


class TeacherAchievementListView(ReadOnlyModelViewSet):
    queryset = TeacherAchievement.objects.all()
    serializer_class = TeacherAchievementSerializer


class TeacherSkillListView(ReadOnlyModelViewSet):
    queryset = TeacherSkill.objects.all()
    serializer_class = TeacherSkillSerializer


class NewsListView(ReadOnlyModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer


class CompanyListView(ListModelMixin, GenericViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class EducationAboutView(ListModelMixin, GenericViewSet):
    queryset = EducationAbout.objects.all()
    serializer_class = EducationAboutSerializer


class CourseAboutView(ListModelMixin, GenericViewSet):
    queryset = CourseAbout.objects.all()
    serializer_class = CourseAboutSerializer
