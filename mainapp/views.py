from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet, ModelViewSet
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from mainapp.serializers import (CourseSerializer, TechnologySerializer,
                                 CourseModuleSerializer, ModuleThemeSerializer,
                                StatisticsSerializer,
                                TeacherSerializer, TeacherAchievementSerializer,
                                TeacherSkillSerializer, CourseListSerializer, NewsSerializer,
                                CompanySerializer, TeacherListSerializer, EducationAboutSerializer,
                                CourseAboutSerializer)
from mainapp.models import (Course, Technology, CourseModule, ModuleTheme, Company, EducationAbout,
                            Statistics, Teacher, TeacherAchievement, TeacherSkill, News, CourseAbout)
from rest_framework.response import Response
from rest_framework import status


class StatisticsAPIView(APIView):
    serializer_class = StatisticsSerializer
    queryset = Statistics.objects.all()
    
    def get(self, request):
        statistics = self.queryset
        serializer = self.serializer_class(statistics, context = {'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context = {'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def patch(self, request):
        stat_id = request.data.get('id')
        statistic = get_object_or_404(Statistics, id=stat_id)
        serializer = self.serializer_class(statistic, data=request.data, context = {'request': request}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request):
        stat_id = request.data.get('id')
        statistic = get_object_or_404(Statistics, id=stat_id)
        statistic.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    


class NewsListView(ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer


class CompanyListView(ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class EducationAboutView(ModelViewSet):
    queryset = EducationAbout.objects.all()
    serializer_class = EducationAboutSerializer


class CourseAboutView(ModelViewSet):
    queryset = CourseAbout.objects.all()
    serializer_class = CourseAboutSerializer


class CourseAPIView(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    

class TechnologyAPIView(APIView):
    serializer_class = TechnologySerializer
    
    def post(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)
        serializer = self.serializer_class(data=request.data, context = {'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save(course=course)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def patch(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)
        technology_id = request.data.get('id')
        technology = get_object_or_404(Technology, id=technology_id, course=course)
        serializer = self.serializer_class(technology, data=request.data, context = {'request': request}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(course=course)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)
        tech_id = request.data.get('id')
        technology = get_object_or_404(Technology, id=tech_id, course=course)
        technology.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class CourseModuleAPIView(APIView):
    serializer_class = CourseModuleSerializer
    queryset = CourseModule.objects.all()
    
    def post(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)
        serializer = self.serializer_class(data=request.data, context = {'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save(course=course)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def patch(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)
        module_id = request.data.get('id')
        module = get_object_or_404(CourseModule, id=module_id, course=course)
        serializer = self.serializer_class(module, data=request.data, context = {'request': request}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(course=course)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)
        module_id = request.data.get('id')
        module = get_object_or_404(CourseModule, id=module_id, course=course)
        module.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class ModuleThemeAPIView(APIView):
    serializer_class = ModuleThemeSerializer
    queryset = ModuleTheme.objects.all()
    
    def post(self, request, module_id):
        module = get_object_or_404(CourseModule, id=module_id)
        serializer = self.serializer_class(data=request.data, context = {'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save(module=module)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def patch(self, request, module_id):
        module = get_object_or_404(CourseModule, id=module_id)
        theme_id = request.data.get('id')
        theme = get_object_or_404(ModuleTheme, id=theme_id, module=module)
        serializer = self.serializer_class(theme, data=request.data, context = {'request': request}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(module=module)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, module_id):
        module = get_object_or_404(CourseModule, id=module_id)
        theme_id = request.data.get('id')
        theme = get_object_or_404(ModuleTheme, id=theme_id, module=module)
        theme.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TeacherAPIView(ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer


class TeacherAchievementAPIView(APIView):
    serializer_class = TeacherAchievementSerializer
    
    def post(self, request, teacher_id):
        teacher = get_object_or_404(Teacher, id=teacher_id)
        serializer = self.serializer_class(data=request.data, context = {'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save(teacher=teacher)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def patch(self, request, teacher_id):
        teacher = get_object_or_404(Teacher, id=teacher_id)
        achievement_id = request.data.get('id')
        achievement = get_object_or_404(TeacherAchievement, id=achievement_id, teacher=teacher)
        serializer = self.serializer_class(achievement, data=request.data, context = {'request': request}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(teacher=teacher)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, teacher_id):
        teacher = get_object_or_404(Teacher, id=teacher_id)
        achievement_id = request.data.get('id')
        achievement = get_object_or_404(TeacherAchievement, id=achievement_id, teacher=teacher)
        achievement.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TeacherSkillAPIView(APIView):
    serializer_class = TeacherSkillSerializer
    
    def post(self, request, teacher_id):
        teacher = get_object_or_404(Teacher, id=teacher_id)
        serializer = self.serializer_class(data=request.data, context = {'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save(teacher=teacher)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def patch(self, request, teacher_id):
        teacher = get_object_or_404(Teacher, id=teacher_id)
        skill_id = request.data.get('id')
        skill = get_object_or_404(TeacherSkill, id=skill_id, teacher=teacher)
        serializer = self.serializer_class(skill, data=request.data, context = {'request': request}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(teacher=teacher)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, teacher_id):
        teacher = get_object_or_404(Teacher, id=teacher_id)
        skill_id = request.data.get('id')
        skill = get_object_or_404(TeacherSkill, id=skill_id, teacher=teacher)
        skill.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)