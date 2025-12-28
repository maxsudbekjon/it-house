import requests
from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")

def sent_to_telegram(name, phone_number, course):
    message = f"New Contact Message:\nName: {name}\nPhone Number: {phone_number}\nCourse: {course}"
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': ADMIN_CHAT_ID,
        'text': message
    }
    requests.post(url, data=payload)