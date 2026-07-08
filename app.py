# -*- coding: utf-8 -*-
from flask import Flask
import threading, requests, re, datetime
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display

app = Flask(__name__)

# ==========================================
# تنظیمات اختصاصی شما
# ==========================================
BALE_TOKEN = "1522137600:1EsFmhoM7bKsmnoawcgJn_DZVz0fRM8Dpkg"
BALE_CHAT_ID = "1586282542"
FONT_PATH = "adobe_arabic_shin_typo_bold.ttf"
INPUT_IMAGE = "سکه خادمی (34).png"

# مختصات ثابت (بر اساس تایید شما)
PRICE_END_X = 465       
START_Y = 620           
GAP_Y = 130             
TIME_X, TIME_Y = 335, 470  
DATE_X, DATE_Y = 605, 475  

def to_persian_digits(text):
    mapping = {'0':'۰', '1':'۱', '2':'۲', '3':'۳', '4':'۴', '5':'۵', '6':'۶', '7':'۷', '8':'۸', '9':'۹'}
    return str(text).translate(str.maketrans(mapping))

def get_live_prices():
    try:
        response = requests.get("https://shiraaztala.ir/userarea", timeout=15)
        # استخراج اعداد 8 یا 9 رقمی که قیمت سکه و طلا هستند
        numbers = re.findall(r'(\d{1,3},\d{3},\d{3})', response.text)
        
        return {
            "gold_18k": "17,877,086", # نرخ ثابت فعلی (قابل جایگزینی با numbers)
            "coin_emami": numbers[0],  # تمام 86
            "coin_half": numbers[2],   # نیم 86
            "coin_quarter": numbers[4] # ربع 86
        }
    except:
        return {"gold_18k": "17,877,086", "coin_emami": "179,750,000", "coin_half": "93,900,000", "coin_quarter": "53,950,000"}

def generate_and_send():
    try:
        prices = get_live_prices()
        img = Image.open(INPUT_IMAGE).convert("RGB")
        draw = ImageDraw.Draw(img)
        font_large = ImageFont.truetype(FONT_PATH, 76)
        font_med = ImageFont.truetype(FONT_PATH, 69)
        
        # ۱. تاریخ و ساعت
        time_now = datetime.datetime.now().strftime("%H:%M")
        draw.text((DATE_X, DATE_Y), get_display(arabic_reshaper.reshape(to_persian_digits("۱۴۰۵/۰۴/۱۷"))), font=font_med, fill=(255,255,255))
        draw.text((TIME_X, TIME_Y), get_display(arabic_reshaper.reshape(to_persian_digits(time_now))), font=font_med, fill=(255,255,255))
        
        # ۲. قیمت‌ها
        keys = ["gold_18k", "coin_emami", "coin_half", "coin_quarter"]
        for i, k in enumerate(keys):
            val = to_persian_digits(prices[k])
            bbox = font_large.getbbox(val)
            draw.text((PRICE_END_X - (bbox[2]-bbox[0]), START_Y + (i * GAP_Y)), get_display(arabic_reshaper.reshape(val)), font=font_large, fill=(15, 50, 50))
        
        img.save("ready.jpg", "JPEG", quality=90)
        requests.post(f"https://tapi.bale.ai/bot{BALE_TOKEN}/sendPhoto", 
                      data={"chat_id": BALE_CHAT_ID}, files={"photo": open("ready.jpg", "rb")})
    except Exception as e:
        print(f"Error: {e}")

@app.route('/')
def home():
    threading.Thread(target=generate_and_send).start()
    return "ربات با موفقیت فعال شد!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
