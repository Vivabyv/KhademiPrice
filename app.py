# -*- coding: utf-8 -*-
from flask import Flask
import threading, time, requests, jdatetime

app = Flask(__name__)

BALE_TOKEN = "1522137600:1EsFmhoM7bKsmnoawcgJn_DZVz0fRM8Dpkg"
BALE_CHANNEL_ID = "1586282542"

def get_prices():
    try:
        # استفاده از دیتای پایدار طلا و سکه
        url = "https://data.tgju.org/v1/market/indicator/summary"
        r = requests.get(url, timeout=15)
        d = r.json()
        
        # استخراج مقادیر از دیتای استاندارد
        return {
            "gold_18": d.get('gold_18k', '---'),
            "emami": d.get('coin_emami', '---'),
            "half": d.get('coin_half', '---'),
            "quarter": d.get('coin_quarter', '---'),
            "old": d.get('coin_old', '---'),
            "abshode": d.get('gold_abshodeh', '---')
        }
    except:
        return None

def auto_post():
    while True:
        p = get_prices()
        if p:
            now = jdatetime.datetime.now()
            
            msg = f"""⚜️**گالری سکه خادمی**⚜️

**نرخ معاملات:**
تاریخ 🗓️ {now.strftime('%Y/%m/%d')}
ساعت ⏰️ {now.strftime('%H:%M')}

**آبشده نقدی (فردا):**
🔵فروش: {p['abshode']}
🟠خرید: {p['abshode']}

**گرم طلای ۱۸:**
🔵فروش: {p['gold_18']}
🟠خرید: {p['gold_18']}

**تمام ۸۶ بانکی:**
🔵فروش: {p['emami']}
🟠خرید: {p['emami']}

**نیم ۸۶ بانکی:**
🔵فروش: {p['half']}
🟠خرید: {p['half']}

**ربع ۸۶ بانکی:**
🔵فروش: {p['quarter']}
🟠خرید: {p['quarter']}

**تمام غیر بانکی:**
🔵فروش: {p['old']}
🟠خرید: {p['old']}

📍 شیراز، روبروی بازار زرگرها، ابتدای خیابان طالقانی، پاساژ شادی
📞 ۰۹۱۷۵۰۵۰۲۳۰ | ۰۷۱۹۱۰۹۱۱۰۰
🆔 @khademicoin"""

            requests.post(f"https://tapi.bale.ai/bot{BALE_TOKEN}/sendMessage", 
                          data={"chat_id": BALE_CHANNEL_ID, "text": msg, "parse_mode": "Markdown"})
        
        time.sleep(300) # ارسال هر ۵ دقیقه

@app.route('/')
def home():
    return "ربات اتوماسیون با دیتای پایدار فعال است."

if __name__ == "__main__":
    threading.Thread(target=auto_post, daemon=True).start()
    app.run(host='0.0.0.0', port=10000)
