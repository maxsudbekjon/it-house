import os
import random
from io import BytesIO
from PIL import Image
import requests

from django.core.files import File
from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker
from django.conf import settings

from mainapp.models import (
    Course, Technology, CourseModule, ModuleTheme,
    Statistics, Company, Teacher, TeacherAchievement,
    TeacherSkill, Status, News, CourseAbout, EducationAbout
)


fake = Faker()
PLACEHOLDER_JPG = "https://picsum.photos/800/600"
PLACEHOLDER_PNG = "https://picsum.photos/200/200"


# 🔹 Agar internetdan rasm yuklanmasa, local fake image yaratamiz
def generate_placeholder_image(ext="png", color=(150, 150, 150)):
    img = Image.new("RGB", (200, 200), color=color)
    temp = BytesIO()
    img.save(temp, ext.upper())
    temp.seek(0)
    filename = f"placeholder_{random.randint(1000,9999)}.{ext}"
    return File(temp, name=filename)


def download_image(url, ext="jpg"):
    try:
        response = requests.get(url, timeout=8)
        response.raise_for_status()
        temp = BytesIO(response.content)
        filename = f"seed_{random.randint(1000,9999)}.{ext}"
        return File(temp, name=filename)
    except Exception:
        # 🔹 fallback — local fake image
        return generate_placeholder_image(ext=ext)


class Command(BaseCommand):
    help = "Seed DB with fake data for frontend testing (with language suffixes)."

    def add_arguments(self, parser):
        parser.add_argument('--courses', type=int, default=5)
        parser.add_argument('--teachers', type=int, default=5)
        parser.add_argument('--use_local_assets', action='store_true')

    @transaction.atomic
    def handle(self, *args, **options):
        courses_count = options['courses']
        teachers_count = options['teachers']
        use_local = options['use_local_assets']
        fixtures_dir = os.path.join(settings.MEDIA_ROOT, 'fixtures')

        self.stdout.write(self.style.WARNING("⚙️ Seeding fake data..."))

        # --- Statistics ---
        if not Statistics.objects.exists():
            Statistics.objects.create(
                total_students=15000,
                total_graduates=9000,
                total_employed=7000,
                avg_duration=6.2,
                avg_start_salary=1100.5,
                partners=15
            )

        # --- Status ---
        for name in ["Draft", "Published", "Archived"]:
            Status.objects.get_or_create(
                name_uz=f"{name} (UZ)",
                name_en=f"{name} (EN)",
                name_ru=f"{name} (RU)",
            )

        # --- Courses ---
        for _ in range(courses_count):
            title = fake.sentence(nb_words=3).rstrip('.')

            banner = (
                download_image(PLACEHOLDER_JPG, ext="jpg")
                if not use_local
                else self.get_local_image(fixtures_dir)
            )

            course = Course.objects.create(
                banner=banner,
                title_uz=f"{title} (UZ)",
                title_en=f"{title} (EN)",
                title_ru=f"{title} (RU)",
                description_uz=f"{fake.paragraph()} (UZ)",
                description_en=f"{fake.paragraph()} (EN)",
                description_ru=f"{fake.paragraph()} (RU)",
                price=round(random.uniform(100, 999), 2),
                duration=random.randint(1, 12),
                students=random.randint(50, 500),
            )
            self.stdout.write(f"🧩 Created course: {course.title_en}")

            # --- Technologies ---
            for _ in range(random.randint(2, 5)):
                icon = download_image(PLACEHOLDER_PNG, ext="png")
                Technology.objects.create(
                    name_uz=f"{fake.word().title()} (UZ)",
                    name_en=f"{fake.word().title()} (EN)",
                    name_ru=f"{fake.word().title()} (RU)",
                    icon=icon,
                    course=course
                )

            # --- Modules + Themes ---
            for m in range(random.randint(2, 4)):
                module = CourseModule.objects.create(
                    title_uz=f"Module {m+1}: {fake.word().title()} (UZ)",
                    title_en=f"Module {m+1}: {fake.word().title()} (EN)",
                    title_ru=f"Module {m+1}: {fake.word().title()} (RU)",
                    course=course
                )
                for t in range(random.randint(2, 5)):
                    ModuleTheme.objects.create(
                        title_uz=f"{fake.sentence(nb_words=3)} (UZ)",
                        title_en=f"{fake.sentence(nb_words=3)} (EN)",
                        title_ru=f"{fake.sentence(nb_words=3)} (RU)",
                        module=module
                    )

        # --- Teachers ---
        for _ in range(teachers_count):
            photo = download_image(PLACEHOLDER_JPG, ext="jpg")
            teacher = Teacher.objects.create(
                full_name=fake.name(),
                bio_uz=f"{fake.text()} (UZ)",
                bio_en=f"{fake.text()} (EN)",
                bio_ru=f"{fake.text()} (RU)",
                profession=fake.job()[:25],
                experience=random.randint(1, 20),
                company=fake.company()[:25],
                total_students=random.randint(100, 2000),
                total_projects=random.randint(1, 40),
                photo=photo,
                github_link=f"https://github.com/{fake.user_name()}",
                linkedin_link=f"https://linkedin.com/in/{fake.user_name()}",
                twitter_link=f"https://twitter.com/{fake.user_name()}",
            )
            for _ in range(random.randint(1, 3)):
                TeacherAchievement.objects.create(
                    title_uz=f"{fake.sentence(nb_words=5)} (UZ)",
                    title_en=f"{fake.sentence(nb_words=5)} (EN)",
                    title_ru=f"{fake.sentence(nb_words=5)} (RU)",
                    teacher=teacher
                )
            for _ in range(random.randint(2, 5)):
                TeacherSkill.objects.create(
                    name_uz=f"{fake.word().title()} (UZ)",
                    name_en=f"{fake.word().title()} (EN)",
                    name_ru=f"{fake.word().title()} (RU)",
                    teacher=teacher
                )

        # --- Companies ---
        for _ in range(3):
            logo = download_image(PLACEHOLDER_PNG, ext="png")
            Company.objects.create(
                logo=logo,
                workers=random.randint(10, 500)
            )

        # --- CourseAbout & EducationAbout ---
        for _ in range(2):
            CourseAbout.objects.create(
                title_uz=f"{fake.sentence(nb_words=4)} (UZ)",
                title_en=f"{fake.sentence(nb_words=4)} (EN)",
                title_ru=f"{fake.sentence(nb_words=4)} (RU)",
                description_uz=f"{fake.text()} (UZ)",
                description_en=f"{fake.text()} (EN)",
                description_ru=f"{fake.text()} (RU)"
            )

            EducationAbout.objects.create(
                icon=download_image(PLACEHOLDER_PNG, ext="png"),
                title_uz=f"{fake.sentence(nb_words=3)} (UZ)",
                title_en=f"{fake.sentence(nb_words=3)} (EN)",
                title_ru=f"{fake.sentence(nb_words=3)} (RU)",
                description_uz=f"{fake.text()} (UZ)",
                description_en=f"{fake.text()} (EN)",
                description_ru=f"{fake.text()} (RU)"
            )

        # --- News ---
        status = Status.objects.first()
        for _ in range(5):
            News.objects.create(
                title_uz=f"{fake.sentence(nb_words=6)} (UZ)",
                title_en=f"{fake.sentence(nb_words=6)} (EN)",
                title_ru=f"{fake.sentence(nb_words=6)} (RU)",
                description_uz=f"{fake.paragraph()} (UZ)",
                description_en=f"{fake.paragraph()} (EN)",
                description_ru=f"{fake.paragraph()} (RU)",
                banner=download_image(PLACEHOLDER_JPG, ext="jpg"),
                status=status
            )

        self.stdout.write(self.style.SUCCESS("✅ Fake data seeded successfully."))

    # --- Helper: local image loader ---
    def get_local_image(self, fixtures_dir):
        try:
            files = [f for f in os.listdir(fixtures_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            if not files:
                return generate_placeholder_image()
            path = os.path.join(fixtures_dir, random.choice(files))
            return File(open(path, 'rb'), name=os.path.basename(path))
        except Exception:
            return generate_placeholder_image()
