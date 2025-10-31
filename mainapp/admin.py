from django.contrib import admin
from mainapp.models import (Teacher, Course, CourseAbout, CourseModule,
                            Company, TeacherAchievement, TeacherSkill, Technology,
                            ModuleTheme, Statistics, News, EducationAbout
)

# Register your models here.
admin.site.register(Course)
admin.site.register(Technology)
admin.site.register(CourseModule)
admin.site.register(CourseAbout)
admin.site.register(ModuleTheme)
admin.site.register(Statistics)
admin.site.register(Company)
admin.site.register(Teacher)
admin.site.register(TeacherAchievement)
admin.site.register(TeacherSkill)
admin.site.register(News)
admin.site.register(EducationAbout)
