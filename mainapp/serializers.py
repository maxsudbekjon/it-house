from rest_framework import serializers
from mainapp.models import (Course, Technology, CourseModule, ModuleTheme,
                            Statistics, Teacher, TeacherAchievement, TeacherSkill, News)


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


class CourseModuleSerializer(serializers.ModelSerializer):
    module_themes = ModuleThemeSerializer(many=True, read_only=True)

    class Meta:
        model = CourseModule
        fields = '__all__'   # ⬅️ no change here



class CourseSerializer(serializers.ModelSerializer):
    course_modules = CourseModuleSerializer(many=True, read_only=True)
    technologies = TechnologySerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = '__all__'





# class CourseSerializer(serializers.ModelSerializer):
#     course_modules = CourseModuleSerializer(many=True, read_only=True)
#     module_themes = ModuleThemeSerializer(many=True, read_only=True)
#     technologies = TechnologySerializer(many=True, read_only=True)
    
#     class Meta:
#         model = Course
#         fields = '__all__'


class CourseListSerializer(serializers.ModelSerializer):
    technologies = TechnologySerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = '__all__'


class TopStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statistics
        fields = ['total_students', 'total_graduates', 'total_employed', 'avg_duration']


class MediumStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statistics
        fields = ['total_employed', 'avg_start_salary', 'total_graduates', 'partners']

    
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


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'
