# -*- coding: utf-8 -*-
from flask import Flask
import threading, time, requests, datetime
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display

app = Flask(__name__)

# تنظیمات ثابت
BALE_TOKEN = "1522137600:1EsFmhoM7bKsmnoawcgJn_DZVz0fRM8Dpkg"
BALE_CHAT_ID = "1586282542"
FONT_PATH = "adobe_arabic_shin_typo_bold.ttf" # نام فونت شما
INPUT_IMAGE = "سکه خادمی (34).png"

# مختصات دقیق شما
PRICE_END_X = 465       
START_Y = 620           
GAP_Y = 130             

def to_persian_digits(text):
    mapping = {'0':'۰', '1':'۱', '2':'۲', '3':'۳', '4':'۴', '5':'۵', '6':'۶', '7':'۷', '8':'۸', '9':'۹'}
    return str(text).translate(str.maketrans(mapping))

def generate_and_send():
    try:
        # قیمت‌ها (برای تست همین‌جا مقداردهی شده، جایگزین تابع قیمت زنده کنید)
        prices = {"gold_18k": 17785000, "coin_emami": 179320000, "coin_half": 93560000, "coin_quarter": 53750000, "coin_old": 174006000, "coin_half_old": 88208000, "coin_quarter_old": 44896000}
        
        img = Image.open(INPUT_IMAGE).convert("RGB")
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(FONT_PATH, 76) # سایز فونت شما
        
        row_keys = ["gold_18k", "coin_emami", "coin_half", "coin_quarter", "coin_old", "coin_half_old", "coin_quarter_old"]
        
        for i, key in enumerate(row_keys):
            # تبدیل عدد به فارسی
            val = to_persian_digits("{:,}".format(int(prices[key])))
            # آماده‌سازی متن فارسی برای نمایش درست
            reshaped_text = get_display(arabic_reshaper.reshape(val))
            
            # محاسبه مختصات راست‌چین
            bbox = font.getbbox(reshaped_text)
            text_width = bbox[2] - bbox[0]
            draw.text((PRICE_END_X - text_width, START_Y + (i * GAP_Y)), reshaped_text, font=font, fill=(15, 50, 50))
        
        img.save("ready.jpg", "JPEG", quality=90)
        
        # ارسال به بله
        url = f"https://tapi.bale.ai/bot{BALE_TOKEN}/sendPhoto"
        with open("ready.jpg", "rb") as f:
            requests.post(url, data={"chat_id": BALE_CHAT_ID}, files={"photo": f}, timeout=20)
            
    except Exception as e:
        print(f"Error: {e}")

@app.route('/')
def home():
    threading.Thread(target=generate_and_send).start()
    return "درخواست ارسال عکس با قیمت‌های دقیق ثبت شد!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
