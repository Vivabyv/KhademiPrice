# -*- coding: utf-8 -*-
from flask import Flask
import threading, requests, datetime, pytz
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display

app = Flask(__name__)

BALE_TOKEN = "1522137600:1EsFmhoM7bKsmnoawcgJn_DZVz0fRM8Dpkg"
BALE_CHAT_ID = "1586282542"
FONT_PATH = "adobe_arabic_shin_typo_bold.ttf"
INPUT_IMAGE = "سکه خادمی (34).png"

def get_live_prices():
    # لینک مستقیم دیتای سایت (این دقیق‌ترین روش است)
    url = "https://shiraaztala.ir/_next/data/gi1JcHYIp3c40BCz7VlES/userarea/prices.json"
    try:
        # استفاده از API_KEY برای دسترسی به دیتا
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()['pageProps']['prices']
        return data # این دیکشنری حاوی تمام قیمت‌هاست
    except:
        return None

def generate_and_send():
    prices = get_live_prices()
    if not prices: return # اگر دیتا نیامد، ارسال نکن

    img = Image.open(INPUT_IMAGE).convert("RGB")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT_PATH, 76)
    
    # چاپ قیمت‌ها (از دیکشنری prices استفاده کن)
    keys = ["gold_18k", "coin_emami", "coin_half", "coin_quarter"]
    for i, k in enumerate(keys):
        val = "{:,}".format(int(prices.get(k, 0)))
        draw.text((400, 620 + (i * 130)), get_display(arabic_reshaper.reshape(val)), font=font, fill=(0,0,0))
    
    img.save("ready.jpg", "JPEG", quality=90)
    requests.post(f"https://tapi.bale.ai/bot{BALE_TOKEN}/sendPhoto", 
                  data={"chat_id": BALE_CHAT_ID}, files={"photo": open("ready.jpg", "rb")})

@app.route('/')
def home():
    threading.Thread(target=generate_and_send).start()
    return "اتصال مستقیم برقرار شد."
