from rest_framework import status
from rest_framework.test import APITestCase

from mainapp.models import Teacher


class TeacherPermissionTests(APITestCase):
    def setUp(self):
        self.teacher = Teacher.objects.create(
            full_name='John Doe', profession='Backend', experience=5, photo='teacher_photos/john.jpg',
        )

    def test_anonymous_cannot_replace_teacher(self):
        response = self.client.put(f'/api/teachers/{self.teacher.id}/', {
            'full_name': 'Hacked', 'profession': 'x', 'experience': 1,
        })

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.teacher.refresh_from_db()
        self.assertEqual(self.teacher.full_name, 'John Doe')
