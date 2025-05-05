import requests
from bs4 import BeautifulSoup
import threading
import time
from flask import Flask
import os

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
TESLA_URL = 'https://www.tesla.com/tr_TR/inventory/new/my?arrangeby=plh&zip=34025&range=0'

def check_for_long_range():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    try:
        response = requests.get(TESLA_URL, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text().lower()
            if "long range" in text:
                return True
    except Exception as e:
        print(f"Hata oluştu: {e}")
    return False

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Telegram bildirimi gönderilemedi: {e}")

def background_worker():
    print("Tesla 'Long Range' kontrolü başlatıldı...")
    while True:
        print("Kontrol ediliyor...")
        if check_for_long_range():
            send_telegram_message("🚗 Tesla Model Y 'Long Range' stokta! Kontrol et: " + TESLA_URL)
        time.sleep(10)

@app.route('/')
def index():
    return "Tesla Long Range checker is running."

if __name__ == '__main__':
    threading.Thread(target=background_worker).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
