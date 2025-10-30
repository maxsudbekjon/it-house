from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from mainapp.serializers import (CourseSerializer, TechnologySerializer,
                                 CourseModuleSerializer, ModuleThemeSerializer,
                                    StatisticsSerializer, TeacherSerializer,
                                    TeacherAchievementSerializer, TeacherSkillSerializer,
                                    CourseListSerializer)
from mainapp.models import (Course, Technology, CourseModule, ModuleTheme,
                            Statistics, Teacher, TeacherAchievement, TeacherSkill)



class CourseListView(ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseListSerializer
    
class CourseDetailView(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class TechnologyListView(ModelViewSet):
    queryset = Technology.objects.all()
    serializer_class = TechnologySerializer


class CourseModuleListView(ModelViewSet):
    queryset = CourseModule.objects.all()
    serializer_class = CourseModuleSerializer


class ModuleThemeListView(ModelViewSet):
    queryset = ModuleTheme.objects.all()
    serializer_class = ModuleThemeSerializer


class StatisticsListView(ModelViewSet):
    queryset = Statistics.objects.all()
    serializer_class = StatisticsSerializer


class TeacherListView(ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer


class TeacherAchievementListView(ModelViewSet):
    queryset = TeacherAchievement.objects.all()
    serializer_class = TeacherAchievementSerializer


class TeacherSkillListView(ModelViewSet):
    queryset = TeacherSkill.objects.all()
    serializer_class = TeacherSkillSerializer
