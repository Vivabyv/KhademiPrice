# -*- coding: utf-8 -*-
from flask import Flask
import threading, time, requests, jdatetime, re

app = Flask(__name__)

# اطلاعات اصلی شما
BALE_TOKEN = "1522137600:1EsFmhoM7bKsmnoawcgJn_DZVz0fRM8Dpkg"
BALE_CHANNEL_ID = "1586282542"
API_KEY = "f23de2487d6ebe28a48e552080403890"

def get_prices():
    try:
        # استفاده از موتور رندر برای عبور از فیلتر سایت شیراز طلا
        url = f"http://api.scraperapi.com?api_key={API_KEY}&url=https://shiraaztala.ir/userarea&render=true"
        r = requests.get(url, timeout=40)
        text = r.text
        
        # استخراج قیمت‌ها
        def find_p(name):
            match = re.search(f"{name}.*?(\d{{1,3}},\d{{3}},\d{{3}})", text, re.DOTALL)
            return match.group(1) if match else "---"

        return {
            "abshode": find_p("آبشده"),
            "gold": find_p("نرخ هر گرم طلا"),
            "emami": find_p("تمام 86"),
            "half": find_p("نیم 86"),
            "quarter": find_p("ربع 86"),
            "normal": find_p("تمام عادی"),
            "half_normal": find_p("نیم عادی"),
            "quarter_normal": find_p("ربع عادی")
        }
    except:
        return None

def auto_post():
    while True:
        p = get_prices()
        if p and p['gold'] != "---":
            now = jdatetime.datetime.now()
            
            # فرمتِ دقیقِ موردِ نظرِ شما
            msg = f"""⚜️**گالری سکه خادمی**⚜️

**نرخ معاملات:**
تاریخ 🗓️ {now.strftime('%Y/%m/%d')}
ساعت ⏰️ {now.strftime('%H:%M')}

**آبشده نقدی (فردا):**
🔵فروش: {p['abshode']}
🟠خرید: {p['abshode']}

**گرم طلای ۱۸:**
🔵فروش: {p['gold']}
🟠خرید: {p['gold']}

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
🔵فروش: {p['normal']}
🟠خرید: {p['normal']}

**نیم غیر بانکی:**
🔵فروش: {p['half_normal']}
🟠خرید: {p['half_normal']}

**ربع غیر بانکی:**
🔵فروش: {p['quarter_normal']}
🟠خرید: {p['quarter_normal']}

📍 شیراز، روبروی بازار زرگرها، ابتدای خیابان طالقانی، پاساژ شادی
📞 ۰۹۱۷۵۰۵۰۲۳۰ | ۰۷۱۹۱۰۹۱۱۰۰
🆔 @khademicoin"""

            requests.post(f"https://tapi.bale.ai/bot{BALE_TOKEN}/sendMessage", 
                          data={"chat_id": BALE_CHANNEL_ID, "text": msg, "parse_mode": "Markdown"})
        
        time.sleep(300) # فاصله ۵ دقیقه‌ای برای امنیتِ بیشتر سایت و جلوگیری از بلاک

@app.route('/')
def home():
    return "ربات اتوماسیون گالری خادمی فعال است."

if __name__ == "__main__":
    threading.Thread(target=auto_post, daemon=True).start()
    app.run(host='0.0.0.0', port=10000)
