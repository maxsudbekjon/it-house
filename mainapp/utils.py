import logging

import requests
from django.conf import settings

logger = logging.getLogger(__name__)

BOT_TOKEN = settings.TELEGRAM_BOT_TOKEN
ADMIN_CHAT_ID = settings.TELEGRAM_CHAT_ID
# The contact form request waits for this call, so it must not hang
TELEGRAM_TIMEOUT = 5

def sent_to_telegram(name, phone_number, course, message=None):
    text = f"New Contact Message:\nName: {name}\nPhone Number: {phone_number}\nCourse: {course}"
    if message:
        text += f"\nMessage: {message}"
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': ADMIN_CHAT_ID,
        'text': text
    }
    try:
        response = requests.post(url, data=payload, timeout=TELEGRAM_TIMEOUT)
    except requests.RequestException as exc:
        # str(exc) contains the request URL with the bot token, so log only the error type
        logger.error("Telegram sendMessage failed: %s", type(exc).__name__)
        return
    if not response.ok:
        logger.error("Telegram sendMessage failed: HTTP %s %s", response.status_code, response.text[:200])