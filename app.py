# -*- coding: utf-8 -*-
from flask import Flask
import threading, requests, re, datetime, pytz
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display

app = Flask(__name__)

# ... (تنظیمات همان قبلی) ...
BALE_TOKEN = "1522137600:1EsFmhoM7bKsmnoawcgJn_DZVz0fRM8Dpkg"
BALE_CHAT_ID = "1586282542"
FONT_PATH = "adobe_arabic_shin_typo_bold.ttf"
INPUT_IMAGE = "سکه خادمی (34).png"
API_KEY = "f23de2487d6ebe28a48e552080403890"

def get_live_prices():
    try:
        # درخواست مستقیم با API جهت دور زدن امنیت
        url = f"http://api.scraperapi.com?api_key={API_KEY}&url=https://shiraaztala.ir/userarea&render=true"
        response = requests.get(url, timeout=60)
        
        # شکارِ تمام اعداد با فرمتِ قیمت (مثال: 179,750,000)
        # این لیستِ تمامِ قیمت‌هایِ صفحه است
        nums = re.findall(r'(\d{1,3},\d{3},\d{3})', response.text)
        
        # برگرداندنِ لیست کامل اعداد (اگر سایت تغییر کند هم باز اعداد را پیدا می‌کند)
        return nums if len(nums) > 7 else ["---"] * 10
    except:
        return ["---"] * 10

def generate_and_send():
    prices = get_live_prices()
    img = Image.open(INPUT_IMAGE).convert("RGB")
    draw = ImageDraw.Draw(img)
    font_l = ImageFont.truetype(FONT_PATH, 76)
    
    # لیست قیمت‌ها برای چاپ (از لیستِ nums استفاده می‌کنیم)
    # اگر قیمت‌ها درست چاپ نشد، فقط ایندکس‌ها (مثلا [0], [1]) را تغییر می‌دهیم
    for i in range(7):
        val = prices[i].replace('0','۰').replace('1','۱').replace('2','۲').replace('3','۳').replace('4','۴').replace('5','۵').replace('6','۶').replace('7','۷').replace('8','۸').replace('9','۹')
        bbox = font_l.getbbox(val)
        draw.text((465 - (bbox[2]-bbox[0]), 620 + (i * 130)), get_display(arabic_reshaper.reshape(val)), font=font_l, fill=(15, 50, 50))
    
    img.save("ready.jpg", "JPEG", quality=90)
    requests.post(f"https://tapi.bale.ai/bot{BALE_TOKEN}/sendPhoto", data={"chat_id": BALE_CHAT_ID}, files={"photo": open("ready.jpg", "rb")})

@app.route('/')
def home():
    threading.Thread(target=generate_and_send).start()
    return "ربات با متدِ شکارِ تمامِ اعداد فعال شد!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
