# Вакансии (`vacancies`)

Приложение `vacancies` отдаёт список открытых вакансий IT House для сайта и даёт администратору управлять ими.

## Эндпоинты

| Метод | URL | Доступ | Описание |
|---|---|---|---|
| `GET` | `/api/vacancies/` | все | Список вакансий, сначала новые |
| `GET` | `/api/vacancies/{id}/` | все | Одна вакансия |
| `POST` | `/api/vacancies/` | superuser | Создать |
| `PUT` / `PATCH` | `/api/vacancies/{id}/` | superuser | Изменить, в т.ч. `{"is_active": false}` — скрыть |
| `DELETE` | `/api/vacancies/{id}/` | superuser | Удалить навсегда |

- Аноним и обычный пользователь видят только `is_active = true`. Неактивная вакансия в `retrieve` отдаёт `404`.
- Superuser (JWT `Authorization: Bearer <token>`) видит и неактивные — чтобы мог включить их обратно.
- Запись без токена — `401`, с токеном не-superuser — `403`.
- Пагинации нет, как и у остальных эндпоинтов проекта.
- Сортировка: `-created_at`, при равенстве `-id`.

## Формат ответа

```json
{
  "id": 1,
  "title_uz": "Backend dasturchi",
  "title_ru": "Backend разработчик",
  "title_en": "Backend developer",
  "employment_type": "part_time",
  "description_uz": "...",
  "description_ru": "...",
  "description_en": "...",
  "requirements_uz": ["Python", "Django"],
  "requirements_ru": ["Python", "Django"],
  "requirements_en": ["Python", "Django"],
  "location_uz": "Toshkent",
  "location_ru": "Ташкент",
  "location_en": "Tashkent",
  "is_active": true,
  "created_at": "2026-10-09T18:53:00.123456+05:00"
}
```

Все поля обязательны при создании, кроме `is_active` (по умолчанию `true`). `id` и `created_at` — только чтение.

### `employment_type`

Возвращается код, перевод — на стороне фронтенда.

| Код | uz | ru | en |
|---|---|---|---|
| `full_time` | To'liq stavka | Полная занятость | Full-time |
| `part_time` | Yarim stavka | Частичная занятость | Part-time |
| `internship` | Amaliyot | Стажировка | Internship |
| `contract` | Shartnoma asosida | По договору | Contract |

Удалённый формат работы указывается в `location_*` (например, `Masofaviy`), а не в `employment_type`: это разные оси, и «полставки удалённо» иначе не описать.

### `requirements_*`

В базе — текст, одно требование на строку (так удобно вводить в админке). API отдаёт и принимает массив строк: пустые строки и пробелы по краям отбрасываются. Пустой массив при записи не принимается.

## Админка

`/admin-page-locked/vacancies/vacancy/`

- Поля сгруппированы по языкам: O'zbekcha / Русский / English.
- `is_active` переключается прямо в списке; фильтры по активности и типу; поиск по `title_*`.
- Массовые действия «Activate / Deactivate selected vacancies».
- «Скрыть» = снять `is_active`. «Удалить» — безвозвратно; если вакансия может вернуться, лучше скрывать.

## Тесты

```bash
python manage.py test vacancies
```
