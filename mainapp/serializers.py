from rest_framework import serializers
from mainapp.models import (Course, Technology, CourseModule, ModuleTheme,
                            Statistics, Teacher, TeacherAchievement, TeacherSkill)


class TechnologySerializer(serializers.ModelSerializer):
    class Meta:
        model = Technology
        fields = '__all__'


class CourseModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseModule
        fields = '__all__'


class ModuleThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModuleTheme
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    course_modules = CourseModuleSerializer(many=True, read_only=True)
    module_themes = ModuleThemeSerializer(many=True, read_only=True)
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
    teacher_achievements = TeacherAchievementSerializer(many=True, read_only=True)
    teacher_skills = TeacherSkillSerializer(many=True, read_only=True)

    class Meta:
        model = Teacher
        fields = '__all__'
