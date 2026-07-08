# -*- coding: utf-8 -*-
from flask import Flask
import requests

app = Flask(__name__)

BALE_BOT_TOKEN = "1522137600:1EsFmhoM7bKsmnoawcgJn_DZVz0fRM8Dpkg"
BALE_CHANNEL_ID = "1586282542"

@app.route('/')
def home():
    url = f"https://tapi.bale.ai/bot{BALE_BOT_TOKEN}/sendMessage"
    response = requests.post(url, data={"chat_id": BALE_CHANNEL_ID, "text": "تست اتصال ربات: سیستم فعال است!"})
    return f"وضعیت ارسال پیام تست به بله: {response.status_code}"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
