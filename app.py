# -*- coding: utf-8 -*-
from flask import Flask
import threading, time, requests, datetime, pytz

app = Flask(__name__)

BALE_TOKEN = "1522137600:1EsFmhoM7bKsmnoawcgJn_DZVz0fRM8Dpkg"
BALE_CHANNEL_ID = "1586282542"

def get_prices_from_source():
    # لینک مستقیم دیتایِ قیمتِ سایت
    url = "https://shiraaztala.ir/_next/data/gi1JcHYIp3c40BCz7VlES/userarea/prices.json"
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        return response.json()['pageProps']['prices']
    except:
        return None

def auto_post():
    while True:
        prices = get_prices_from_source()
        if prices:
            iran_tz = pytz.timezone("Asia/Tehran")
            now = datetime.datetime.now(iran_tz)
            
            # فرمت دقیق شما
            msg = f"""⚜️**گالری سکه خادمی**⚜️
تاریخ 🗓️ {now.strftime("%Y/%m/%d")} | ساعت ⏰️ {now.strftime("%H:%M")}

**آبشده نقدی:**
🔵فروش: {prices.get('abshode_sell', '-')} | 🟠خرید: {prices.get('abshode_buy', '-')}

**گرم طلای ۱۸:**
🔵فروش: {prices.get('gold_18k', '-')}

**تمام ۸۶:**
🔵فروش: {prices.get('coin_emami', '-')}

📍 شیراز، پاساژ شادی 📞 ۰۹۱۷۵۰۵۰۲۳۰
🆔 @khademicoin"""
            requests.post(f"https://tapi.bale.ai/bot{BALE_TOKEN}/sendMessage", 
                          data={"chat_id": BALE_CHANNEL_ID, "text": msg, "parse_mode": "Markdown"})
        
        time.sleep(600) # هر ۱۰ دقیقه یکبار خودش خودکار پست می‌کند

@app.route('/')
def home():
    return "ربات اتوماسیون در حال کار است..."

if __name__ == "__main__":
    # شروع اتوماسیون در پس‌زمینه
    threading.Thread(target=auto_post, daemon=True).start()
    app.run(host='0.0.0.0', port=10000)
