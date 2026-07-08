# -*- coding: utf-8 -*-
from flask import Flask
import threading, time, requests, datetime, pytz

app = Flask(__name__)

# اطلاعات ربات و کانال
BALE_TOKEN = "1522137600:1EsFmhoM7bKsmnoawcgJn_DZVz0fRM8Dpkg"
BALE_CHANNEL_ID = "1586282542"

def get_live_data():
    """دریافت قیمت‌ها از منبع اصلی سایت"""
    try:
        # آدرس دیتای خام سایت
        url = "https://shiraaztala.ir/_next/data/gi1JcHYIp3c40BCz7VlES/userarea/prices.json"
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
        return response.json()['pageProps']['prices']
    except:
        return None

def auto_post_task():
    """حلقه اصلی اتوماسیون"""
    while True:
        try:
            prices = get_live_data()
            if prices:
                iran_tz = pytz.timezone("Asia/Tehran")
                now = datetime.datetime.now(iran_tz)
                
                # متن نهایی با فرمت دقیق شما
                msg = f"""⚜️**گالری سکه خادمی**⚜️

**نرخ معاملات:**
تاریخ 🗓️ {now.strftime("%Y/%m/%d")}
ساعت ⏰️ {now.strftime("%H:%M")}

**آبشده نقدی:**
🔵فروش: {prices.get('abshode_sell', '-')}
🟠خرید: {prices.get('abshode_buy', '-')}

**گرم طلای ۱۸:**
🔵فروش: {prices.get('gold_18k', '-')}

**تمام ۸۶ بانکی:**
🔵فروش: {prices.get('coin_emami', '-')}

**نیم ۸۶ بانکی:**
🔵فروش: {prices.get('coin_half', '-')}

**ربع ۸۶ بانکی:**
🔵فروش: {prices.get('coin_quarter', '-')}

**تمام غیر بانکی:**
🔵فروش: {prices.get('coin_old', '-')}

📍 شیراز، روبروی بازار زرگرها، ابتدای خیابان طالقانی، پاساژ شادی
📞 ۰۹۱۷۵۰۵۰۲۳۰ | ۰۷۱۹۱۰۹۱۱۰۰
🆔 @khademicoin"""

                requests.post(f"https://tapi.bale.ai/bot{BALE_TOKEN}/sendMessage", 
                              data={"chat_id": BALE_CHANNEL_ID, "text": msg, "parse_mode": "Markdown"})
        except Exception as e:
            print(f"Error: {e}")
        
        time.sleep(600) # ارسال هر ۱۰ دقیقه یکبار

@app.route('/')
def home():
    return "ربات اتوماسیون گالری خادمی با موفقیت فعال است."

if __name__ == "__main__":
    # اجرای اتوماسیون در پس‌زمینه
    threading.Thread(target=auto_post_task, daemon=True).start()
    app.run(host='0.0.0.0', port=10000)
