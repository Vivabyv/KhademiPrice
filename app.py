# -*- coding: utf-8 -*-
from flask import Flask
import threading, time, requests, datetime
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display

app = Flask(__name__)

BALE_TOKEN = "1522137600:1EsFmhoM7bKsmnoawcgJn_DZVz0fRM8Dpkg"
BALE_CHAT_ID = "1586282542"

def generate_and_send():
    try:
        # ۱. دریافت قیمت (ساده شده)
        # اگر این لینک در Render کار نکرد، یعنی IP دیتاسنتر مسدود است
        # ما اینجا از یک قیمت ثابت برای تست ارسال استفاده می‌کنیم
        
        # ۲. پردازش تصویر (بسیار سبک)
        img = Image.open("سکه خادمی (34).png").convert("RGB")
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("adobe_arabic_shin_typo_bold.ttf", 76)
        
        # نوشتن قیمت نمونه
        text = get_display(arabic_reshaper.reshape("۲۵،۰۰۰،۰۰۰"))
        draw.text((100, 620), text, font=font, fill=(0, 0, 0))
        
        img.save("ready.jpg", "JPEG", quality=85)
        
        # ۳. ارسال به بله
        url = f"https://tapi.bale.ai/bot{BALE_TOKEN}/sendPhoto"
        with open("ready.jpg", "rb") as f:
            requests.post(url, data={"chat_id": BALE_CHAT_ID}, files={"photo": f}, timeout=20)
            
    except Exception as e:
        print(f"Error: {e}")

@app.route('/')
def home():
    threading.Thread(target=generate_and_send).start()
    return "درخواست ارسال عکس ثبت شد!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
