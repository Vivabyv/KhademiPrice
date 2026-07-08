# -*- coding: utf-8 -*-
from flask import Flask
import threading, time, requests, jdatetime

app = Flask(__name__)

BALE_TOKEN = "1522137600:1EsFmhoM7bKsmnoawcgJn_DZVz0fRM8Dpkg"
BALE_CHANNEL_ID = "1586282542"

def get_prices():
    try:
        # منبع دیتای اقتصادی معتبر
        r = requests.get("https://data.tgju.org/v1/market/indicator/summary", timeout=15)
        return r.json()
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

def auto_post():
    while True:
        try:
            d = get_prices()
            if d:
                now = jdatetime.datetime.now()
                # آماده‌سازی متن دقیق با چک کردن اینکه دیتا موجود باشد
                msg = f"""⚜️**گالری سکه خادمی**⚜️

**نرخ معاملات:**
تاریخ 🗓️ {now.strftime('%Y/%m/%d')}
ساعت ⏰️ {now.strftime('%H:%M')}

**آبشده نقدی:**
🔵فروش: {d.get('gold_abshodeh', 'دریافت نشد')}

**گرم طلای ۱۸:**
🔵فروش: {d.get('gold_18k', 'دریافت نشد')}

**تمام ۸۶ بانکی:**
🔵فروش: {d.get('coin_emami', 'دریافت نشد')}

**نیم ۸۶ بانکی:**
🔵فروش: {d.get('coin_half', 'دریافت نشد')}

**ربع ۸۶ بانکی:**
🔵فروش: {d.get('coin_quarter', 'دریافت نشد')}

📍 شیراز، روبروی بازار زرگرها، ابتدای خیابان طالقانی، پاساژ شادی
📞 ۰۹۱۷۵۰۵۰۲۳۰ | ۰۷۱۹۱۰۹۱۱۰۰
🆔 @khademicoin"""

                # ارسال به بله
                url = f"https://tapi.bale.ai/bot{BALE_TOKEN}/sendMessage"
                resp = requests.post(url, data={"chat_id": BALE_CHANNEL_ID, "text": msg, "parse_mode": "Markdown"})
                print(f"Sent status: {resp.status_code}") # این را در Logs چک کنید
            else:
                print("No data received from API")
        except Exception as e:
            print(f"Loop Error: {e}")
            
        time.sleep(300) # هر ۵ دقیقه

@app.route('/')
def home():
    return "ربات فعال است و در حال تلاش برای ارسال قیمت‌هاست."

if __name__ == "__main__":
    # اجرای رشته جداگانه برای جلوگیری از بلاک شدن سرور
    threading.Thread(target=auto_post, daemon=True).start()
    app.run(host='0.0.0.0', port=10000)
