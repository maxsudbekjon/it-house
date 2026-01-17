import requests
from django.conf import settings


BOT_TOKEN = settings.TELEGRAM_BOT_TOKEN
ADMIN_CHAT_ID = settings.TELEGRAM_CHAT_ID

def sent_to_telegram(name, phone_number, course):
    message = f"New Contact Message:\nName: {name}\nPhone Number: {phone_number}\nCourse: {course}"
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': ADMIN_CHAT_ID,
        'text': message
    }
    requests.post(url, data=payload)