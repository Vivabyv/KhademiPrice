# -*- coding: utf-8 -*-
from flask import Flask
import threading, requests, re, datetime
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display

app = Flask(__name__)

BALE_TOKEN = "1522137600:1EsFmhoM7bKsmnoawcgJn_DZVz0fRM8Dpkg"
BALE_CHAT_ID = "1586282542"
FONT_PATH = "adobe_arabic_shin_typo_bold.ttf"
INPUT_IMAGE = "سکه خادمی (34).png"

def to_persian_digits(text):
    mapping = {'0':'۰', '1':'۱', '2':'۲', '3':'۳', '4':'۴', '5':'۵', '6':'۶', '7':'۷', '8':'۸', '9':'۹'}
    return str(text).translate(str.maketrans(mapping))

def get_live_prices():
    try:
        response = requests.get("https://shiraaztala.ir/userarea", timeout=15)
        # استخراج تمام اعداد با فرمت قیمت (مثال: 179,750,000)
        nums = re.findall(r'(\d{1,3},\d{3},\d{3})', response.text)
        
        # بر اساس ترتیبی که در متن سایت شما بود:
        return {
            "gold_18k": "17,877,086", 
            "coin_emami": nums[0],       # تمام بانکی
            "coin_half": nums[2],        # نیم بانکی
            "coin_quarter": nums[4],     # ربع بانکی
            "coin_old": nums[8],         # تمام قدیم
            "coin_half_old": nums[10],   # نیم قدیم
            "coin_quarter_old": nums[12] # ربع قدیم
        }
    except:
        return {k: "---" for k in ["gold_18k", "coin_emami", "coin_half", "coin_quarter", "coin_old", "coin_half_old", "coin_quarter_old"]}

def generate_and_send():
    prices = get_live_prices()
    img = Image.open(INPUT_IMAGE).convert("RGB")
    draw = ImageDraw.Draw(img)
    font_l = ImageFont.truetype(FONT_PATH, 76)
    font_m = ImageFont.truetype(FONT_PATH, 69)
    
    # ساعت و تاریخ زنده
    now = datetime.datetime.now()
    time_str = now.strftime("%H:%M")
    date_str = "۱۴۰۵/۰۴/۱۷" # تاریخ امروز
    
    draw.text((605, 475), get_display(arabic_reshaper.reshape(date_str)), font=font_m, fill=(255,255,255))
    draw.text((335, 470), get_display(arabic_reshaper.reshape(to_persian_digits(time_str))), font=font_m, fill=(255,255,255))
    
    # لیست قیمت‌ها برای چاپ
    keys = ["gold_18k", "coin_emami", "coin_half", "coin_quarter", "coin_old", "coin_half_old", "coin_quarter_old"]
    for i, k in enumerate(keys):
        val = to_persian_digits(prices[k])
        bbox = font_l.getbbox(val)
        draw.text((465 - (bbox[2]-bbox[0]), 620 + (i * 130)), get_display(arabic_reshaper.reshape(val)), font=font_l, fill=(15, 50, 50))
    
    img.save("ready.jpg", "JPEG", quality=90)
    requests.post(f"https://tapi.bale.ai/bot{BALE_TOKEN}/sendPhoto", 
                  data={"chat_id": BALE_CHAT_ID}, files={"photo": open("ready.jpg", "rb")})

@app.route('/')
def home():
    threading.Thread(target=generate_and_send).start()
    return "ربات با تمام سکه‌ها و ساعت دقیق فعال شد!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
