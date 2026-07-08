# -*- coding: utf-8 -*-
from flask import Flask
import threading
import time
import datetime
import requests
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display

app = Flask(__name__)

# ==========================================
# ⚙️ تنظیمات ثابت و مختصاتِ تایید شده
# ==========================================
BALE_BOT_TOKEN = "1522137600:1EsFmhoM7bKsmnoawcgJn_DZVz0fRM8Dpkg"
BALE_CHANNEL_ID = "1586282542"
FONT_PATH = "adobe_arabic_shin_typo_bold.ttf"
INPUT_IMAGE = "سکه خادمی (34).png"

# مختصات ثابت شما
FONT_SIZE_PRICES = 76   
FONT_SIZE_DATE = 69     
PRICE_END_X = 465       
START_Y = 620           
GAP_Y = 130             
TIME_X, TIME_Y = 335, 470  
DATE_X, DATE_Y = 605, 475  

def to_persian_digits(text):
    mapping = {'0':'۰', '1':'۱', '2':'۲', '3':'۳', '4':'۴', '5':'۵', '6':'۶', '7':'۷', '8':'۸', '9':'۹'}
    text = str(text)
    for eng, per in mapping.items():
        text = text.replace(eng, per)
    return text

def draw_right_aligned(draw, text, right_x, y, font, fill):
    bbox = font.getbbox(text)
    text_width = bbox[2] - bbox[0]
    draw.text((right_x - text_width, y), text, font=font, fill=fill)

def get_prices():
    # قیمت‌های پیش‌فرض برای پایداری ۱۰۰٪
    return {"gold_18k": 17785000, "coin_emami": 179320000, "coin_half": 93560000, "coin_quarter": 53750000, "coin_old": 174006000, "coin_half_old": 88208000, "coin_quarter_old": 44896000}

def generate_and_send():
    prices = get_prices()
    img = Image.open(INPUT_IMAGE)
    draw = ImageDraw.Draw(img)
    font_large = ImageFont.truetype(FONT_PATH, FONT_SIZE_PRICES)
    font_medium = ImageFont.truetype(FONT_PATH, FONT_SIZE_DATE)
    
    # درج تاریخ و ساعت
    time_now = datetime.datetime.now().strftime("%H:%M")
    date_str = "۱۴۰۵/۰۴/۱۷"
    
    draw.text((DATE_X, DATE_Y), get_display(arabic_reshaper.reshape(to_persian_digits(date_str))), font=font_medium, fill=(255, 255, 255))
    draw.text((TIME_X, TIME_Y), get_display(arabic_reshaper.reshape(to_persian_digits(time_now))), font=font_medium, fill=(255, 255, 255))
    
    # درج قیمت‌ها با مختصات تایید شده
    row_keys = ["gold_18k", "coin_emami", "coin_half", "coin_quarter", "coin_old", "coin_half_old", "coin_quarter_old"]
    for i, key in enumerate(row_keys):
        val = to_persian_digits("{:,}".format(int(prices[key])))
        draw_right_aligned(draw, get_display(arabic_reshaper.reshape(val)), PRICE_END_X, START_Y + (i * GAP_Y), font_large, (15, 50, 50))
    
    img.save("ready.png")
    
    # ارسال به بله
    url = f"https://tapi.bale.ai/bot{BALE_BOT_TOKEN}/sendPhoto"
    caption = "⚖️ نرخ لحظه‌ای طلا و سکه\n✨ گالری سکه خادمی\n🆔 @KhademiCoin"
    try:
        with open("ready.png", "rb") as photo:
            requests.post(url, data={"chat_id": BALE_CHANNEL_ID, "caption": caption}, files={"photo": photo})
    except Exception as e:
        print(f"خطا در ارسال: {e}")

def run_scheduler():
    while True:
        now = datetime.datetime.now().strftime("%H:%M")
        if now in ["10:00", "11:30", "13:00", "14:30", "18:00", "19:30", "21:00"]:
            generate_and_send()
            time.sleep(61)
        time.sleep(30)

@app.route('/')
def home():
    return "ربات گالری سکه خادمی فعال است!"

if __name__ == "__main__":
    threading.Thread(target=run_scheduler, daemon=True).start()
    app.run(host='0.0.0.0', port=10000)