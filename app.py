# -*- coding: utf-8 -*-
from flask import Flask
import requests, datetime, pytz

app = Flask(__name__)

BALE_TOKEN = "1522137600:1EsFmhoM7bKsmnoawcgJn_DZVz0fRM8Dpkg"
BALE_CHANNEL_ID = "1586282542"

@app.route('/')
def home():
    # تستِ مستقیم: همین الان پیام بده
    try:
        now = datetime.datetime.now(pytz.timezone("Asia/Tehran"))
        msg = f"✅ ربات فعال شد! تست ارسال در تاریخ {now.strftime('%Y/%m/%d')} ساعت {now.strftime('%H:%M')}"
        
        response = requests.post(
            f"https://tapi.bale.ai/bot{BALE_TOKEN}/sendMessage", 
            data={"chat_id": BALE_CHANNEL_ID, "text": msg}
        )
        
        if response.status_code == 200:
            return "پیام با موفقیت به بله ارسال شد! کانال را چک کنید."
        else:
            return f"خطا در ارسال: {response.text}"
    except Exception as e:
        return f"خطای سیستمی: {str(e)}"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
