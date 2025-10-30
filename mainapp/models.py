from django.db import models
from django.core.validators import FileExtensionValidator


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Course(BaseModel):
    banner = models.ImageField(upload_to='course_banners/', validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg'])])
    title_uz = models.CharField(max_length=25)
    title_en = models.CharField(max_length=25)
    title_ru = models.CharField(max_length=25)
    description_uz = models.TextField()
    description_en = models.TextField()
    description_ru = models.TextField()
    duration = models.IntegerField(help_text="Duration in months")
    students = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title_uz
    

class Technology(BaseModel):
    name_uz = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100)
    name_ru = models.CharField(max_length=100)
    icon = models.ImageField(upload_to='technology_icons/', validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg'])])
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='technologies')
    
    def __str__(self):
        return self.name_uz
    

class CourseModule(BaseModel):
    title_uz = models.CharField(max_length=100)
    title_en = models.CharField(max_length=100)
    title_ru = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')

    def __str__(self):
        return self.title_uz


class ModuleTheme(BaseModel):
    title_uz = models.CharField(max_length=100)
    title_en = models.CharField(max_length=100)
    title_ru = models.CharField(max_length=100)
    module = models.ForeignKey(CourseModule, on_delete=models.CASCADE, related_name='themes')

    def __str__(self):
        return self.title_uz
    

class Statistics(BaseModel):
    total_students = models.PositiveIntegerField()
    total_graduates = models.PositiveIntegerField()
    total_employed = models.PositiveIntegerField()
    avg_duration = models.FloatField(help_text="Average course duration in months")
    avg_start_salary = models.FloatField(help_text="Average starting salary after course completion")
    partners = models.PositiveIntegerField()


class Company(BaseModel):
    logo = models.ImageField(upload_to='company_logos/', validators=[FileExtensionValidator(allowed_extensions=['png'])])
    workers = models.PositiveIntegerField()

    def __str__(self):
        return str(self.workers)


class Teacher(BaseModel):
    full_name = models.CharField(max_length=255)
    bio_uz = models.TextField()
    bio_en = models.TextField()
    bio_ru = models.TextField()
    profession = models.CharField(max_length=25)
    exprerience = models.PositiveIntegerField(help_text="Experience in years")
    company = models.CharField(max_length=25)
    total_students = models.PositiveIntegerField()
    total_projects = models.PositiveIntegerField()
    photo = models.ImageField(upload_to='teacher_photos/', validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg'])])
    github_link = models.URLField(blank=True, null=True)
    linkedin_link = models.URLField(blank=True, null=True)
    twitter_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.full_name
    

class TeacherAchievement(BaseModel):
    title_uz = models.CharField(max_length=255)
    title_en = models.CharField(max_length=255)
    title_ru = models.CharField(max_length=255)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='achievements')
    
    def __str__(self):
        return self.title_uz
    

class TeacherSkill(BaseModel):
    name_uz = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100)
    name_ru = models.CharField(max_length=100)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='skills')

    def __str__(self):
        return self.name_uz
    

class News(BaseModel):
    title_uz = models.CharField(max_length=255)
    title_en = models.CharField(max_length=255)
    title_ru = models.CharField(max_length=255)
    description_uz = models.TextField()
    description_en = models.TextField()
    description_ru = models.TextField()
    banner = models.ImageField(upload_to='news_banners/', validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg'])])

    def __str__(self):
        return self.title_uz


class CourseAbout(BaseModel):
    title_uz = models.CharField(max_length=255)
    title_en = models.CharField(max_length=255)
    title_ru = models.CharField(max_length=255)
    description_uz = models.TextField()
    description_en = models.TextField()
    description_ru = models.TextField()

    def __str__(self):
        return self.title_uz


class EducationAbout(BaseModel):
    icon = models.ImageField(upload_to='education_about_icons/', validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg'])])
    title_uz = models.CharField(max_length=255)
    title_en = models.CharField(max_length=255)
    title_ru = models.CharField(max_length=255)
    description_uz = models.TextField()
    description_en = models.TextField()
    description_ru = models.TextField()

    def __str__(self):
        return self.title_uz
