from unittest import mock

import requests
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db import IntegrityError, transaction
from rest_framework import status
from rest_framework.test import APITestCase

from mainapp.models import ContactMessage, Course, Statistics, Teacher

CONTACT_URL = '/api/contact/'


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


class ContactMessageAPITests(APITestCase):
    def setUp(self):
        # ContactMessageThrottle allows one request per hour and keeps its history in the cache
        cache.clear()
        patcher = mock.patch('mainapp.utils.requests.post')
        self.telegram_post = patcher.start()
        self.addCleanup(patcher.stop)

    def payload(self, **overrides):
        data = {'name': 'Ali', 'phone_number': '+998901234567', 'course': 'Backend'}
        data.update(overrides)
        return data

    def test_message_is_saved_and_sent_to_telegram(self):
        response = self.client.post(CONTACT_URL, self.payload(message='Kechki guruh bormi?'), format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Kechki guruh bormi?')
        self.assertEqual(ContactMessage.objects.get().message, 'Kechki guruh bormi?')
        self.assertIn('\nMessage: Kechki guruh bormi?', self.telegram_post.call_args.kwargs['data']['text'])

    def test_message_is_optional(self):
        for value in ({}, {'message': None}, {'message': ''}):
            with self.subTest(value=value):
                cache.clear()
                response = self.client.post(CONTACT_URL, self.payload(**value), format='json')

                self.assertEqual(response.status_code, status.HTTP_201_CREATED)
                self.assertNotIn('\nMessage:', self.telegram_post.call_args.kwargs['data']['text'])

    def test_message_up_to_limit_is_accepted(self):
        response = self.client.post(CONTACT_URL, self.payload(message='a' * 1000), format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_message_over_limit_is_rejected(self):
        response = self.client.post(CONTACT_URL, self.payload(message='a' * 1001), format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('message', response.data)
        self.assertFalse(ContactMessage.objects.exists())
        self.telegram_post.assert_not_called()

    def test_telegram_is_called_with_timeout(self):
        self.client.post(CONTACT_URL, self.payload(), format='json')

        self.assertTrue(self.telegram_post.call_args.kwargs.get('timeout'))

    def test_telegram_network_error_does_not_break_request_or_leak_token(self):
        token = 'secret-bot-token'
        self.telegram_post.side_effect = requests.ConnectionError(f'Max retries exceeded with url: /bot{token}/sendMessage')

        with mock.patch('mainapp.utils.BOT_TOKEN', token), self.assertLogs('mainapp.utils', 'ERROR') as logs:
            response = self.client.post(CONTACT_URL, self.payload(), format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(ContactMessage.objects.exists())
        self.assertNotIn(token, '\n'.join(logs.output))

    def test_telegram_error_response_is_logged(self):
        self.telegram_post.return_value.ok = False
        self.telegram_post.return_value.status_code = 400
        self.telegram_post.return_value.text = '{"ok":false,"description":"Bad Request: chat not found"}'

        with self.assertLogs('mainapp.utils', 'ERROR') as logs:
            response = self.client.post(CONTACT_URL, self.payload(), format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('chat not found', logs.output[0])


def make_course(title='Backend'):
    return Course.objects.create(
        banner='course_banners/x.jpg', title_uz=title, title_en=title, title_ru=title,
        description_uz='.', description_en='.', description_ru='.', duration=6,
    )


class StatisticsAPITests(APITestCase):
    def setUp(self):
        self.statistics = Statistics.objects.create(
            total_students=3000, total_graduates=2200, total_employed=1000,
            avg_duration=7, avg_start_salary=300, partners=3, employment_rate=40,
        )
        self.url = f'/api/statistics/{self.statistics.id}/'
        make_course('Backend')
        make_course('Frontend')

    def as_superuser(self):
        admin = get_user_model().objects.create_superuser(username='admin', password='pass')
        self.client.force_authenticate(admin)

    def test_list_returns_employment_rate_and_total_directions(self):
        response = self.client.get('/api/statistics/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['employment_rate'], 40)
        self.assertEqual(response.data[0]['total_directions'], 2)

    def test_total_directions_follows_course_count(self):
        make_course('Design')
        self.assertEqual(self.client.get(self.url).data['total_directions'], 3)

        Course.objects.filter(title_uz='Design').delete()
        self.assertEqual(self.client.get(self.url).data['total_directions'], 2)

    def test_employment_rate_defaults_to_zero(self):
        statistics = Statistics.objects.create(
            total_students=1, total_graduates=1, total_employed=1, avg_duration=1, avg_start_salary=1, partners=1,
        )

        self.assertEqual(statistics.employment_rate, 0)

    def test_superuser_can_update_employment_rate(self):
        self.as_superuser()

        for value in (0, 100):
            with self.subTest(value=value):
                response = self.client.patch(self.url, {'employment_rate': value}, format='json')

                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.statistics.refresh_from_db()
                self.assertEqual(self.statistics.employment_rate, value)

    def test_employment_rate_must_be_integer_from_0_to_100(self):
        self.as_superuser()

        for value in (-1, 101, 97.5, 'abc'):
            with self.subTest(value=value):
                response = self.client.patch(self.url, {'employment_rate': value}, format='json')

                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                self.assertIn('employment_rate', response.data)
        self.statistics.refresh_from_db()
        self.assertEqual(self.statistics.employment_rate, 40)

    def test_total_directions_is_read_only(self):
        self.as_superuser()

        response = self.client.patch(self.url, {'total_directions': 50}, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_directions'], 2)

    def test_anonymous_cannot_update_employment_rate(self):
        response = self.client.patch(self.url, {'employment_rate': 99}, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_database_rejects_employment_rate_over_100(self):
        with self.assertRaises(IntegrityError), transaction.atomic():
            Statistics.objects.filter(id=self.statistics.id).update(employment_rate=101)

    def test_admin_shows_and_validates_employment_rate(self):
        admin = get_user_model().objects.create_superuser(username='admin', password='pass')
        self.client.force_login(admin)
        change_url = f'/admin-page-locked/mainapp/statistics/{self.statistics.id}/change/'

        self.assertContains(self.client.get('/admin-page-locked/mainapp/statistics/'), 'employment_rate')
        response = self.client.post(change_url, {
            'total_students': 3000, 'total_graduates': 2200, 'total_employed': 1000,
            'avg_duration': 7, 'avg_start_salary': 300, 'partners': 3, 'employment_rate': 101,
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'Ensure this value is less than or equal to 100.')
        self.statistics.refresh_from_db()
        self.assertEqual(self.statistics.employment_rate, 40)
