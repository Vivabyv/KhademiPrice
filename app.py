# -*- coding: utf-8 -*-
from flask import Flask, request
import requests, datetime, pytz

app = Flask(__name__)

BALE_TOKEN = "1522137600:1EsFmhoM7bKsmnoawcgJn_DZVz0fRM8Dpkg"
BALE_CHANNEL_ID = "1586282542"

@app.route('/send')
def send():
    # دریافت قیمت‌ها از آدرس (پارامترها)
    iran_tz = pytz.timezone("Asia/Tehran")
    now = datetime.datetime.now(iran_tz)
    
    msg = f"""⚜️**گالری سکه خادمی**⚜️

**نرخ معاملات:**
تاریخ 🗓️ {now.strftime("%Y/%m/%d")}
ساعت ⏰️ {now.strftime("%H:%M")}

**آبشده نقدی (فردا):**
🔵فروش: {request.args.get('abshode_sell', '-')}
🟠خرید: {request.args.get('abshode_buy', '-')}

**گرم طلای ۱۸:**
🔵فروش: {request.args.get('gold_sell', '-')}
🟠خرید: {request.args.get('gold_buy', '-')}

**تمام ۸۶ بانکی:**
🔵فروش: {request.args.get('emami_sell', '-')}
🟠خرید: {request.args.get('emami_buy', '-')}

**نیم ۸۶ بانکی:**
🔵فروش: {request.args.get('half_sell', '-')}
🟠خرید: {request.args.get('half_buy', '-')}

**ربع ۸۶ بانکی:**
🔵فروش: {request.args.get('quarter_sell', '-')}
🟠خرید: {request.args.get('quarter_buy', '-')}

**تمام غیر بانکی:**
🔵فروش: {request.args.get('normal_sell', '-')}
🟠خرید: {request.args.get('normal_buy', '-')}

**نیم غیر بانکی:**
🔵فروش: {request.args.get('half_normal_sell', '-')}
🟠خرید: {request.args.get('half_normal_buy', '-')}

**ربع غیر بانکی:**
🔵فروش: {request.args.get('quarter_normal_sell', '-')}
🟠خرید: {request.args.get('quarter_normal_buy', '-')}

📍 شیراز، روبروی بازار زرگرها، ابتدای خیابان طالقانی، پاساژ شادی
📞 ۰۹۱۷۵۰۵۰۲۳۰ | ۰۷۱۹۱۰۹۱۱۰۰
🆔 @khademicoin"""

    requests.post(f"https://tapi.bale.ai/bot{BALE_TOKEN}/sendMessage", 
                  data={"chat_id": BALE_CHANNEL_ID, "text": msg, "parse_mode": "Markdown"})
    return "ارسال شد"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
