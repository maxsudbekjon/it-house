from rest_framework import serializers
from mainapp.models import (Course, Technology, CourseModule, ModuleTheme, Company, EducationAbout, Status,
                            Statistics, Teacher, TeacherAchievement, TeacherSkill, News, CourseAbout, ContactMessage)


class TechnologySerializer(serializers.ModelSerializer):
    class Meta:
        model = Technology
        fields = '__all__'


# class CourseModuleSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CourseModule
#         fields = '__all__'




class ModuleThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModuleTheme
        fields = '__all__'
        extra_kwargs = {
            'module': {'read_only': True},
        }


class CourseModuleSerializer(serializers.ModelSerializer):
    themes = ModuleThemeSerializer(many=True, read_only=True)

    class Meta:
        model = CourseModule
        fields = '__all__'
        extra_kwargs = {
            'course': {'read_only': True},
        }



class CourseSerializer(serializers.ModelSerializer):
    modules = CourseModuleSerializer(many=True, read_only=True)
    technologies = TechnologySerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = '__all__'


class CourseListSerializer(serializers.ModelSerializer):
    technologies = TechnologySerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = '__all__'


class StatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statistics
        fields = '__all__'

    
class TeacherAchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherAchievement
        fields = '__all__'


class TeacherSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherSkill
        fields = '__all__'


class TeacherSerializer(serializers.ModelSerializer):
    achievements = TeacherAchievementSerializer(many=True, read_only=True)
    skills = TeacherSkillSerializer(many=True, read_only=True)


    class Meta:
        model = Teacher
        fields = '__all__'


class TeacherListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'full_name', 'profession', 'photo', 'experience', 'company', 'linkedin_link', 'github_link']


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'
        depth = 1


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class EducationAboutSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationAbout
        fields = '__all__'


class CourseAboutSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseAbout
        fields = '__all__'
        

class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = '__all__'
        extra_kwargs = {
            'created_at': {'read_only': True},
        }
