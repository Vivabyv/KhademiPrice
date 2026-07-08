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
        # ۱. باز کردن تصویر اصلی
        img = Image.open("سکه خادمی (34).png").convert("RGB")
        draw = ImageDraw.Draw(img)
        
        # ۲. استفاده از فونت پیش‌فرض سیستم (برای اطمینان از نمایش متن)
        # در لینوکس Render، این فونت همیشه در دسترس است
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)
        
        # ۳. نوشتن متن تست برای مشاهده تغییرات
        # متن را به فرمت فارسی اصلاح شده تبدیل می‌کنیم
        test_text = get_display(arabic_reshaper.reshape("تست فونت و قیمت"))
        draw.text((100, 620), test_text, font=font, fill=(255, 0, 0)) # رنگ قرمز برای تست
        
        img.save("ready.jpg", "JPEG", quality=85)
        
        # ۴. ارسال
        url = f"https://tapi.bale.ai/bot{BALE_TOKEN}/sendPhoto"
        with open("ready.jpg", "rb") as f:
            requests.post(url, data={"chat_id": BALE_CHAT_ID}, files={"photo": f}, timeout=20)
            
    except Exception as e:
        print(f"Error: {e}")

@app.route('/')
def home():
    threading.Thread(target=generate_and_send).start()
    return "درخواست ارسال عکس با متن تست ثبت شد!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
