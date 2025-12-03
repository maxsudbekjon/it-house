from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet, ModelViewSet
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from mainapp.serializers import (CourseSerializer, TechnologySerializer,
                                 CourseModuleSerializer, ModuleThemeSerializer,
                                StatisticsSerializer, StatusSerializer,
                                TeacherSerializer, TeacherAchievementSerializer,
                                TeacherSkillSerializer, CourseListSerializer, NewsSerializer,
                                CompanySerializer, TeacherListSerializer, EducationAboutSerializer,
                                CourseAboutSerializer, ContactMessageSerializer)
from mainapp.models import (Course, Technology, CourseModule, ModuleTheme, Company, EducationAbout, Status,
                            Statistics, Teacher, TeacherAchievement, TeacherSkill, News, CourseAbout, ContactMessage)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from mainapp.utils import sent_to_telegram
from drf_spectacular.utils import extend_schema


class StatisticsAPIView(APIView):
    serializer_class = StatisticsSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context = {'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def get(self, request):
        statistics = Statistics.objects.all()
        serializer = self.serializer_class(statistics, many=True, context = {'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class StatisticsDetailAPIView(APIView):
    serializer_class = StatisticsSerializer
    
    def get(self, request, stat_id):
        statistic = get_object_or_404(Statistics, id=stat_id)
        serializer = self.serializer_class(statistic, context = {'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, stat_id):
        statistic = get_object_or_404(Statistics, id=stat_id)
        serializer = self.serializer_class(statistic, data=request.data, context = {'request': request}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, stat_id):
        statistic = get_object_or_404(Statistics, id=stat_id)
        statistic.delete()
        return Response({"message": "Statistic deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    


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
    permission_classes = []
    
    def post(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)
        serializer = self.serializer_class(data=request.data, context = {'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save(course=course)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def get(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)
        technologies = Technology.objects.filter(course=course)
        serializer = self.serializer_class(technologies, many=True, context = {'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class TechnologyDetailAPIView(APIView):
    serializer_class = TechnologySerializer
    
    def get(self, request, course_id, tech_id):
        course = get_object_or_404(Course, id=course_id)
        technology = get_object_or_404(Technology, id=tech_id, course=course)
        serializer = self.serializer_class(technology, context = {'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, course_id, tech_id):
        course = get_object_or_404(Course, id=course_id)
        technology = get_object_or_404(Technology, id=tech_id, course=course)
        serializer = self.serializer_class(technology, data=request.data, context = {'request': request}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(course=course)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, course_id, tech_id):
        course = get_object_or_404(Course, id=course_id)
        technology = get_object_or_404(Technology, id=tech_id, course=course)
        technology.delete()
        return Response({"message": "Technology deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    

class CourseModuleListAPIView(APIView):
    serializer_class = CourseModuleSerializer
    
    def post(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)
        serializer = self.serializer_class(data=request.data, context = {'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save(course=course)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def get(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)
        moudels = CourseModule.objects.filter(course=course)
        serializer = self.serializer_class(moudels, many=True, context = {'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class CourseModuleAPIView(APIView):
    serializer_class = CourseModuleSerializer
    queryset = CourseModule.objects.all()
    
    def get(self, request, course_id, module_id):
        course = get_object_or_404(Course, id=course_id)
        modules = get_object_or_404(CourseModule, id=module_id, course=course)
        serializer = self.serializer_class(modules, context = {'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, course_id, module_id):
        course = get_object_or_404(Course, id=course_id)
        module = get_object_or_404(CourseModule, id=module_id, course=course)
        serializer = self.serializer_class(module, data=request.data, context = {'request': request}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(course=course)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, course_id, module_id):
        course = get_object_or_404(Course, id=course_id)
        module = get_object_or_404(CourseModule, id=module_id, course=course)
        module.delete()
        return Response({"message": "Module deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    

class ModuleThemeListAPIView(APIView):
    serializer_class = ModuleThemeSerializer
    queryset = ModuleTheme.objects.all()
    
    def post(self, request, module_id):
        module = get_object_or_404(CourseModule, id=module_id)
        serializer = self.serializer_class(data=request.data, context = {'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save(module=module)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def get(self, request, module_id):
        module = get_object_or_404(CourseModule, id=module_id)
        themes = ModuleTheme.objects.filter(module=module)
        serializer = self.serializer_class(themes, many=True, context = {'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class ModuleThemeAPIView(APIView):
    serializer_class = ModuleThemeSerializer
    
    def get(self, request, module_id, theme_id):
        module = get_object_or_404(CourseModule, id=module_id)
        theme = get_object_or_404(ModuleTheme, id=theme_id, module=module)
        serializer = self.serializer_class(theme, context = {'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, module_id, theme_id):
        module = get_object_or_404(CourseModule, id=module_id)
        theme = get_object_or_404(ModuleTheme, id=theme_id, module=module)
        serializer = self.serializer_class(theme, data=request.data, context = {'request': request}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(module=module)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, module_id, theme_id):
        module = get_object_or_404(CourseModule, id=module_id)
        theme = get_object_or_404(ModuleTheme, id=theme_id, module=module)
        theme.delete()
        return Response({"message": "Theme deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


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
    
    def get(self, request, teacher_id):
        teacher = get_object_or_404(Teacher, id=teacher_id)
        achievements = TeacherAchievement.objects.filter(teacher=teacher)
        serializer = self.serializer_class(achievements, many=True, context = {'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class TeacherAchievementDetailAPIView(APIView):
    serializer_class = TeacherAchievementSerializer
    
    def get(self, request, teacher_id, achievement_id):
        teacher = get_object_or_404(Teacher, id=teacher_id)
        achievement = get_object_or_404(TeacherAchievement, id=achievement_id, teacher=teacher)
        serializer = self.serializer_class(achievement, context = {'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, teacher_id, achievement_id):
        teacher = get_object_or_404(Teacher, id=teacher_id)
        achievement = get_object_or_404(TeacherAchievement, id=achievement_id, teacher=teacher)
        serializer = self.serializer_class(achievement, data=request.data, context = {'request': request}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(teacher=teacher)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, teacher_id, achievement_id):
        teacher = get_object_or_404(Teacher, id=teacher_id)
        achievement = get_object_or_404(TeacherAchievement, id=achievement_id, teacher=teacher)
        achievement.delete()
        return Response({"message": "Achievement deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


class TeacherSkillAPIView(APIView):
    serializer_class = TeacherSkillSerializer
    
    def post(self, request, teacher_id):
        teacher = get_object_or_404(Teacher, id=teacher_id)
        serializer = self.serializer_class(data=request.data, context = {'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save(teacher=teacher)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def get(self, request, teacher_id):
        teacher = get_object_or_404(Teacher, id=teacher_id)
        skills = TeacherSkill.objects.filter(teacher=teacher)
        serializer = self.serializer_class(skills, many=True, context = {'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class TeacherSkillDetailAPIView(APIView):
    serializer_class = TeacherSkillSerializer
    
    def get(self, request, teacher_id, skill_id):
        teacher = get_object_or_404(Teacher, id=teacher_id)
        skill = get_object_or_404(TeacherSkill, id=skill_id, teacher=teacher)
        serializer = self.serializer_class(skill, context = {'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, teacher_id, skill_id):
        teacher = get_object_or_404(Teacher, id=teacher_id)
        skill = get_object_or_404(TeacherSkill, id=skill_id, teacher=teacher)
        serializer = self.serializer_class(skill, data=request.data, context = {'request': request}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(teacher=teacher)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, teacher_id, skill_id):
        teacher = get_object_or_404(Teacher, id=teacher_id)
        skill = get_object_or_404(TeacherSkill, id=skill_id, teacher=teacher)
        skill.delete()
        return Response({"message": "Skill deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    
class ContactMessageAPIView(APIView):
    permission_classes = []
    serializer_class = ContactMessageSerializer
    
    @extend_schema(
        request=ContactMessageSerializer,
        responses={201: ContactMessageSerializer},
        description="Create a new contact message and send it to Telegram."
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context = {'request': request})
        serializer.is_valid(raise_exception=True)
        contect = serializer.save()
        
        sent_to_telegram(
            contect.name,
            contect.phone_number,
            contect.course
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class StatusAPIView(ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer