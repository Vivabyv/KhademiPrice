# -*- coding: utf-8 -*-
from flask import Flask
import requests, jdatetime

app = Flask(__name__)

# اطلاعات ربات و آیدی شخصی
BALE_TOKEN = "1522137600:1EsFmhoM7bKsmnoawcgJn_DZVz0fRM8Dpkg"
USER_ID = "1586282542"

@app.route('/')
def send_report():
    try:
        # ۱. دریافت قیمت‌ها از منبع معتبر
        r = requests.get("https://data.tgju.org/v1/market/indicator/summary", timeout=15)
        d = r.json()
        now = jdatetime.datetime.now()
        
        # ۲. متن دقیق با فرمتِ درخواستی شما
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

📍 شیراز، روبروی بازار زرگرها، ابتدای خیابان طالقانی، پاساژ شادی
📞 ۰۹۱۷۵۰۵۰۲۳۰ | ۰۷۱۹۱۰۹۱۱۰۰
🆔 @khademicoin"""

        # ۳. ارسال پیام
        resp = requests.post(f"https://tapi.bale.ai/bot{BALE_TOKEN}/sendMessage", 
                             data={"chat_id": USER_ID, "text": msg, "parse_mode": "Markdown"})
        
        return "پیام با موفقیت ارسال شد."
    except Exception as e:
        return f"خطا: {str(e)}"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
