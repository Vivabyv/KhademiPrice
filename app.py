# -*- coding: utf-8 -*-
from flask import Flask
import requests
import jdatetime

app = Flask(__name__)

# اطلاعات ربات و آیدی شخصی شما
BALE_TOKEN = "1522137600:1EsFmhoM7bKsmnoawcgJn_DZVz0fRM8Dpkg"
USER_ID = "1586282542" 

@app.route('/')
def home():
    return "✅ ربات فعال است. برای دریافت قیمت، کلمه /send را به انتهای آدرس سایت اضافه کنید."

@app.route('/send')
def send_price():
    try:
        # ۱. دور زدن فیلترینگ سرور با پراکسی raw (دریافت دیتای خالص بدون نیاز به اسکرپ کردن متن)
        url = "https://api.allorigins.win/raw?url=https://data.tgju.org/v1/market/indicator/summary"
        r = requests.get(url, timeout=20)
        d = r.json() # دریافت مستقیم اطلاعات قیمت‌ها
        
        now = jdatetime.datetime.now()
        
        # ۲. آماده‌سازی پیام با فرمت دلخواه شما
        msg = f"""⚜️**گالری سکه خادمی**⚜️

تاریخ 🗓️ {now.strftime('%Y/%m/%d')}
ساعت ⏰️ {now.strftime('%H:%M')}

**آبشده نقدی:** {d.get('gold_abshodeh', '---')}
**گرم طلای ۱۸:** {d.get('gold_18k', '---')}
**تمام سکه بانکی:** {d.get('coin_emami', '---')}
**نیم سکه بانکی:** {d.get('coin_half', '---')}
**ربع سکه بانکی:** {d.get('coin_quarter', '---')}

🆔 @khademicoin"""

        # ۳. ارسال درخواست به بله
        bale_url = f"https://tapi.bale.ai/bot{BALE_TOKEN}/sendMessage"
        resp = requests.post(bale_url, json={"chat_id": USER_ID, "text": msg})
        
        # بررسی وضعیت ارسال
        if resp.status_code == 200:
            return "پیام با موفقیت به ربات بله ارسال شد! تلگرام/بله خود را چک کنید."
        else:
            return f"داده‌ها دریافت شد اما بله خطا داد: {resp.text}"

    except Exception as e:
        return f"خطا در دریافت اطلاعات از سرور طلا: {str(e)}"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
