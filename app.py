# -*- coding: utf-8 -*-
from flask import Flask
import requests
import jdatetime

app = Flask(__name__)

BALE_TOKEN = "1522137600:1EsFmhoM7bKsmnoawcgJn_DZVz0fRM8Dpkg"
USER_ID = "1586282542" 

@app.route('/')
def home():
    return "✅ ربات فعال است. برای دریافت قیمت، کلمه /send را به انتهای آدرس سایت اضافه کنید."

@app.route('/send')
def send_price():
    try:
        # دریافت اطلاعات از API عمومی و بدون فیلتر 
        url = "https://brsapi.ir/FreeTsetmcBourseApi/Api_Free_Gold_Currency_v2.json"
        r = requests.get(url, timeout=20)
        d = r.json() 
        
        now = jdatetime.datetime.now()
        msg = f"⚜️**گالری سکه خادمی**⚜️\n\nتاریخ 🗓️ {now.strftime('%Y/%m/%d')}\nساعت ⏰️ {now.strftime('%H:%M')}\n\n"
        
        # استخراج دیتای طلا
        gold_data = d.get('gold', [])
        
        if gold_data:
            # خواندن خودکار تمام قیمت‌ها و فرمت‌بندی با کاما
            for item in gold_data:
                name = item.get('name', 'نامشخص')
                price = item.get('price', 0)
                msg += f"**{name}:** {price:,} تومان\n"
        else:
            msg += "⚠️ قیمت‌ها در حال حاضر از سیستم دریافت نشدند."
            
        msg += "\n🆔 @khademicoin"

        # ارسال پیام به بله
        bale_url = f"https://tapi.bale.ai/bot{BALE_TOKEN}/sendMessage"
        resp = requests.post(bale_url, json={"chat_id": USER_ID, "text": msg, "parse_mode": "Markdown"})
        
        if resp.status_code == 200:
            return "✅ پیام با قیمت‌های دقیق به بله ارسال شد!"
        else:
            return f"❌ داده‌ها دریافت شد اما بله خطا داد: {resp.text}"

    except Exception as e:
        return f"خطا در دریافت اطلاعات: {str(e)}"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
