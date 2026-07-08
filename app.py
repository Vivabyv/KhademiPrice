# -*- coding: utf-8 -*-
from flask import Flask
import threading, time, requests, datetime
from PIL import Image, ImageDraw, ImageFont
from bs4 import BeautifulSoup
import arabic_reshaper
from bidi.algorithm import get_display

app = Flask(__name__)

BALE_TOKEN = "1522137600:1EsFmhoM7bKsmnoawcgJn_DZVz0fRM8Dpkg"
BALE_CHAT_ID = "1586282542"

def get_real_prices():
    # استفاده از یک Session که تنظیمات مرورگر را شبیه‌سازی می‌کند
    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }
    try:
        # درخواست به صفحه اصلی که قیمت‌ها در آنجا لود می‌شوند
        response = session.get("https://shiraaztala.ir/userarea", headers=headers, timeout=20)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # در اینجا باید با استفاده از کلاس‌های CSS سایتتان، قیمت‌ها را استخراج کنید
        # این یک مثال است؛ ممکن است لازم باشد کلاس زیر را بر اساس سایت خود تغییر دهید
        prices = {"gold_18k": 17785000, "coin_emami": 179320000} # نمونه
        return prices
    except:
        return {"gold_18k": 17785000, "coin_emami": 179320000}

def generate_and_send():
    try:
        prices = get_real_prices()
        img = Image.open("سکه خادمی (34).png").convert("RGB")
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("adobe_arabic_shin_typo_bold.ttf", 76)
        
        # درج قیمت (مثال برای طلا)
        price_text = "{:,}".format(int(prices["gold_18k"]))
        draw.text((350, 620), get_display(arabic_reshaper.reshape(price_text)), font=font, fill=(15, 50, 50))
        
        img.save("ready.jpg", "JPEG", quality=85)
        requests.post(f"https://tapi.bale.ai/bot{BALE_TOKEN}/sendPhoto", 
                      data={"chat_id": BALE_CHAT_ID}, files={"photo": open("ready.jpg", "rb")})
    except Exception as e:
        print(f"Error: {e}")

@app.route('/')
def home():
    threading.Thread(target=generate_and_send).start()
    return "ربات فعال شد و قیمت‌ها در حال پردازش است!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
