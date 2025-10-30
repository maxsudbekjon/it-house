from django.contrib import admin
from .models import Course, Technology, CourseModule, ModuleTheme, Statistics, Company, Teacher, TeacherAchievement, TeacherSkill


# Register your models here.
admin.site.register(Course)
admin.site.register(Technology)
admin.site.register(CourseModule)
admin.site.register(ModuleTheme)
admin.site.register(Statistics)
admin.site.register(Company)
admin.site.register(Teacher)
admin.site.register(TeacherAchievement)
admin.site.register(TeacherSkill)