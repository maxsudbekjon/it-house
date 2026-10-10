from unittest import mock

import requests
from django.core.cache import cache
from rest_framework import status
from rest_framework.test import APITestCase

from mainapp.models import ContactMessage, Teacher

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
