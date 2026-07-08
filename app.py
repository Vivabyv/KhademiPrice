# -*- coding: utf-8 -*-
from flask import Flask
import requests, jdatetime, re

app = Flask(__name__)

# اطلاعات ربات و کاربری
BALE_TOKEN = "1522137600:1EsFmhoM7bKsmnoawcgJn_DZVz0fRM8Dpkg"
USER_ID = "1586282542"

def get_data():
    """دریافت دیتایِ خام از طریقِ پراکسیِ واسط (برای دور زدن فیلترینگ Render)"""
    try:
        # استفاده از واسطِ allorigins برای خواندنِ سایت شیراز طلا
        url = "https://api.allorigins.win/get?url=https://shiraaztala.ir/userarea"
        response = requests.get(url, timeout=20)
        content = response.json().get('contents', '')
        
        def find_p(label):
            # جستجویِ هوشمندِ اعداد در متن
            pattern = f"{label}.*?([\d,]{{5,}})"
            match = re.search(pattern, content)
            return match.group(1).strip() if match else "---"

        return {
            "abshode": find_p("آبشده"),
            "gold": find_p("طلای ۱۸"),
            "emami": find_p("تمام 86"),
            "half": find_p("نیم 86"),
            "quarter": find_p("ربع 86"),
            "normal": find_p("تمام عادی"),
            "half_normal": find_p("نیم عادی"),
            "quarter_normal": find_p("ربع عادی")
        }
    except:
        return None

@app.route('/')
def send_report():
    p = get_data()
    if not p:
        return "خطا: نتوانستم دیتای سایت را بخوانم."

    now = jdatetime.datetime.now()
    
    msg = f"""⚜️**گالری سکه خادمی**⚜️

**نرخ معاملات:**
تاریخ 🗓️ {now.strftime('%Y/%m/%d')}
ساعت ⏰️ {now.strftime('%H:%M')}

**آبشده نقدی:**
🔵فروش: {p['abshode']} | 🟠خرید: {p['abshode']}

**گرم طلای ۱۸:**
🔵فروش: {p['gold']} | 🟠خرید: {p['gold']}

**تمام ۸۶ بانکی:**
🔵فروش: {p['emami']} | 🟠خرید: {p['emami']}

**نیم ۸۶ بانکی:**
🔵فروش: {p['half']} | 🟠خرید: {p['half']}

**ربع ۸۶ بانکی:**
🔵فروش: {p['quarter']} | 🟠خرید: {p['quarter']}

**تمام غیر بانکی:**
🔵فروش: {p['normal']} | 🟠خرید: {p['normal']}

📍 شیراز، روبروی بازار زرگرها، ابتدای خیابان طالقانی، پاساژ شادی
📞 ۰۹۱۷۵۰۵۰۲۳۰ | ۰۷۱۹۱۰۹۱۱۰۰
🆔 @khademicoin"""

    # ارسال به بله
    resp = requests.post(f"https://tapi.bale.ai/bot{BALE_TOKEN}/sendMessage", 
                         data={"chat_id": USER_ID, "text": msg, "parse_mode": "Markdown"})
    
    return f"عملیات انجام شد. کد وضعیت بله: {resp.status_code}"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
