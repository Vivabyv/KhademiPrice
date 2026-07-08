# -*- coding: utf-8 -*-
from flask import Flask, request
import requests
import datetime
import pytz

app = Flask(__name__)

BALE_TOKEN = "1522137600:1EsFmhoM7bKsmnoawcgJn_DZVz0fRM8Dpkg"
BALE_CHANNEL_ID = "1586282542"

def get_tehran_time():
    iran_tz = pytz.timezone("Asia/Tehran")
    now = datetime.datetime.now(iran_tz)
    return now.strftime("%Y/%m/%d"), now.strftime("%H:%M")

# اضافه کردن methods=['GET', 'POST'] برای حل مشکل Method Not Allowed
@app.route('/', methods=['GET', 'POST'])
def send_price_list():
    if request.method == 'GET':
        return "ربات آماده دریافت قیمت است!"
    
    # دریافت قیمت‌ها از شما
    data = request.json
    date, time = get_tehran_time()
    
    message = f"""⚜️**گالری سکه خادمی**⚜️

**نرخ معاملات:**
تاریخ 🗓️ {date}
ساعت ⏰️ {time}

**آبشده نقدی (فردا):**
🔵فروش: {data.get('abshode_sell')}
🟠خرید: {data.get('abshode_buy')}

**گرم طلای ۱۸:**
🔵فروش: {data.get('gold_sell')}
🟠خرید: {data.get('gold_buy')}

**تمام ۸۶ بانکی:**
🔵فروش: {data.get('emami_sell')}
🟠خرید: {data.get('emami_buy')}

**نیم ۸۶ بانکی:**
🔵فروش: {data.get('half_sell')}
🟠خرید: {data.get('half_buy')}

**ربع ۸۶ بانکی:**
🔵فروش: {data.get('quarter_sell')}
🟠خرید: {data.get('quarter_buy')}

**تمام غیر بانکی:**
🔵فروش: {data.get('normal_sell')}
🟠خرید: {data.get('normal_buy')}

**نیم غیر بانکی:**
🔵فروش: {data.get('half_normal_sell')}
🟠خرید: {data.get('half_normal_buy')}

**ربع غیر بانکی:**
🔵فروش: {data.get('quarter_normal_sell')}
🟠خرید: {data.get('quarter_normal_buy')}

📍 شیراز، روبروی بازار زرگرها، ابتدای خیابان طالقانی، پاساژ شادی
📞 ۰۹۱۷۵۰۵۰۲۳۰ | ۰۷۱۹۱۰۹۱۱۰۰
🆔 @khademicoin"""

    requests.post(f"https://tapi.bale.ai/bot{BALE_TOKEN}/sendMessage", 
                  data={"chat_id": BALE_CHANNEL_ID, "text": message, "parse_mode": "Markdown"})
    
    return "پیام با موفقیت ارسال شد"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
