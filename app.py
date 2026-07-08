# -*- coding: utf-8 -*-
from flask import Flask
import threading, time, requests, jdatetime

app = Flask(__name__)

# اطلاعات اصلی (دقیق چک شود)
BALE_TOKEN = "1522137600:1EsFmhoM7bKsmnoawcgJn_DZVz0fRM8Dpkg"
USER_ID = "1586282542" # آیدی شخصی که باید پیام را دریافت کند

def get_data():
    """دریافت قیمت‌ها از منبع پایدار"""
    try:
        # منبع دیتای اقتصادی
        r = requests.get("https://data.tgju.org/v1/market/indicator/summary", timeout=15)
        return r.json()
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

def auto_post():
    while True:
        d = get_data()
        if d:
            now = jdatetime.datetime.now()
            # فرمتِ دقیقِ شما
            msg = f"""⚜️**گالری سکه خادمی**⚜️

**نرخ معاملات:**
تاریخ 🗓️ {now.strftime('%Y/%m/%d')}
ساعت ⏰️ {now.strftime('%H:%M')}

**آبشده نقدی:**
🔵فروش: {d.get('gold_abshodeh', '---')}
🟠خرید: {d.get('gold_abshodeh', '---')}

**گرم طلای ۱۸:**
🔵فروش: {d.get('gold_18k', '---')}
🟠خرید: {d.get('gold_18k', '---')}

**تمام ۸۶ بانکی:**
🔵فروش: {d.get('coin_emami', '---')}
🟠خرید: {d.get('coin_emami', '---')}

**نیم ۸۶ بانکی:**
🔵فروش: {d.get('coin_half', '---')}
🟠خرید: {d.get('coin_half', '---')}

**ربع ۸۶ بانکی:**
🔵فروش: {d.get('coin_quarter', '---')}
🟠خرید: {d.get('coin_quarter', '---')}

**تمام غیر بانکی:**
🔵فروش: {d.get('coin_old', '---')}
🟠خرید: {d.get('coin_old', '---')}

📍 شیراز، روبروی بازار زرگرها، ابتدای خیابان طالقانی، پاساژ شادی
📞 ۰۹۱۷۵۰۵۰۲۳۰ | ۰۷۱۹۱۰۹۱۱۰۰
🆔 @khademicoin"""

            # ارسال به پی‌وی (حتماً در ربات دکمه استارت زده شود)
            url = f"https://tapi.bale.ai/bot{BALE_TOKEN}/sendMessage"
            resp = requests.post(url, data={"chat_id": USER_ID, "text": msg, "parse_mode": "Markdown"})
            print(f"Bale Status: {resp.status_code}")
        
        time.sleep(300) # هر ۵ دقیقه

@app.route('/')
def home():
    return "ربات فعال است."

if __name__ == "__main__":
    threading.Thread(target=auto_post, daemon=True).start()
    app.run(host='0.0.0.0', port=10000)
