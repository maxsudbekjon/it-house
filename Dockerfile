# Rasm: Python 3.12
FROM python:3.12-slim

# Ishchi katalog
WORKDIR /app

# Kerakli fayllarni ko‘chiramiz
COPY requirements.txt .

# Kutubxonalarni o‘rnatamiz
RUN pip install --no-cache-dir -r requirements.txt

# Barcha loyihani konteynerga ko‘chiramiz
COPY . .

# Portni ochamiz
EXPOSE 8000

# Django serverni ishga tushirish komandasi
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]
