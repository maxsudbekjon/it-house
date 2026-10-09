from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from vacancies.models import Vacancy

URL = '/api/vacancies/'


def make_vacancy(**overrides):
    fields = {
        'title_uz': 'Backend dasturchi', 'title_en': 'Backend developer', 'title_ru': 'Backend разработчик',
        'employment_type': Vacancy.EmploymentType.PART_TIME,
        'description_uz': 'Tavsif', 'description_en': 'Description', 'description_ru': 'Описание',
        'requirements_uz': 'Python\r\n\r\n  Django  \n', 'requirements_en': 'Python', 'requirements_ru': 'Python',
        'location_uz': 'Toshkent', 'location_en': 'Tashkent', 'location_ru': 'Ташкент',
    }
    fields.update(overrides)
    return Vacancy.objects.create(**fields)


def payload(**overrides):
    data = {
        'title_uz': 'Frontend dasturchi', 'title_en': 'Frontend developer', 'title_ru': 'Frontend разработчик',
        'employment_type': 'full_time',
        'description_uz': 'Tavsif', 'description_en': 'Description', 'description_ru': 'Описание',
        'requirements_uz': ['React', 'TypeScript'], 'requirements_en': ['React'], 'requirements_ru': ['React'],
        'location_uz': 'Toshkent', 'location_en': 'Tashkent', 'location_ru': 'Ташкент',
    }
    data.update(overrides)
    return data


class PublicVacancyAPITests(APITestCase):
    def test_list_returns_only_active_vacancies(self):
        active = make_vacancy()
        make_vacancy(is_active=False)

        response = self.client.get(URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual([item['id'] for item in response.data], [active.id])

    def test_list_returns_newest_first(self):
        old, new, newest = make_vacancy(), make_vacancy(), make_vacancy()
        now = timezone.now()
        for vacancy, age in ((old, 2), (new, 1), (newest, 0)):
            Vacancy.objects.filter(pk=vacancy.pk).update(created_at=now - timedelta(days=age))

        response = self.client.get(URL)

        self.assertEqual([item['id'] for item in response.data], [newest.id, new.id, old.id])

    def test_list_item_matches_frontend_contract(self):
        make_vacancy()

        item = self.client.get(URL).data[0]

        self.assertEqual(set(item), {
            'id', 'title_uz', 'title_ru', 'title_en', 'employment_type',
            'description_uz', 'description_ru', 'description_en',
            'requirements_uz', 'requirements_ru', 'requirements_en',
            'location_uz', 'location_ru', 'location_en',
            'is_active', 'created_at',
        })
        self.assertEqual(item['employment_type'], 'part_time')
        self.assertEqual(item['requirements_uz'], ['Python', 'Django'])
        self.assertIs(item['is_active'], True)

    def test_retrieve_inactive_vacancy_returns_404(self):
        vacancy = make_vacancy(is_active=False)

        response = self.client.get(f'{URL}{vacancy.id}/')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_anonymous_cannot_modify_vacancies(self):
        vacancy = make_vacancy()
        detail = f'{URL}{vacancy.id}/'

        responses = [
            self.client.post(URL, payload(), format='json'),
            self.client.put(detail, payload(), format='json'),
            self.client.patch(detail, {'is_active': False}, format='json'),
            self.client.delete(detail),
        ]

        self.assertEqual({r.status_code for r in responses}, {status.HTTP_401_UNAUTHORIZED})
        vacancy.refresh_from_db()
        self.assertTrue(vacancy.is_active)

    def test_regular_user_cannot_create_vacancy(self):
        user = get_user_model().objects.create_user(username='user', password='pass')
        self.client.force_authenticate(user)

        response = self.client.post(URL, payload(), format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(Vacancy.objects.exists())


class AdminVacancyAPITests(APITestCase):
    def setUp(self):
        admin = get_user_model().objects.create_superuser(username='admin', password='pass')
        self.client.force_authenticate(admin)

    def test_superuser_creates_vacancy(self):
        response = self.client.post(URL, payload(), format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        vacancy = Vacancy.objects.get(pk=response.data['id'])
        self.assertEqual(vacancy.requirements_uz, 'React\nTypeScript')
        self.assertTrue(vacancy.is_active)

    def test_invalid_employment_type_is_rejected(self):
        response = self.client.post(URL, payload(employment_type='yarim stavka'), format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('employment_type', response.data)

    def test_empty_requirements_are_rejected(self):
        response = self.client.post(URL, payload(requirements_ru=[]), format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('requirements_ru', response.data)

    def test_superuser_sees_and_reactivates_inactive_vacancy(self):
        vacancy = make_vacancy(is_active=False)

        self.assertEqual([item['id'] for item in self.client.get(URL).data], [vacancy.id])
        response = self.client.patch(f'{URL}{vacancy.id}/', {'is_active': True}, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        vacancy.refresh_from_db()
        self.assertTrue(vacancy.is_active)

    def test_deactivated_vacancy_disappears_from_public_list(self):
        vacancy = make_vacancy()

        self.client.patch(f'{URL}{vacancy.id}/', {'is_active': False}, format='json')
        self.client.force_authenticate(None)

        self.assertEqual(self.client.get(URL).data, [])

    def test_superuser_deletes_vacancy(self):
        vacancy = make_vacancy()

        response = self.client.delete(f'{URL}{vacancy.id}/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Vacancy.objects.exists())


class VacancyAdminTests(APITestCase):
    def setUp(self):
        admin = get_user_model().objects.create_superuser(username='admin', password='pass')
        self.client.force_login(admin)

    def test_changelist_and_add_pages_render(self):
        make_vacancy()

        for url in ('/admin-page-locked/vacancies/vacancy/', '/admin-page-locked/vacancies/vacancy/add/'):
            self.assertEqual(self.client.get(url).status_code, status.HTTP_200_OK, url)

    def test_deactivate_action(self):
        vacancy = make_vacancy()

        self.client.post('/admin-page-locked/vacancies/vacancy/', {
            'action': 'deactivate', '_selected_action': [vacancy.pk],
        })

        vacancy.refresh_from_db()
        self.assertFalse(vacancy.is_active)
