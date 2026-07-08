# -*- coding: utf-8 -*-
from flask import Flask
import threading, requests, re, datetime
import pytz
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
        # استخراج تمام قیمت‌ها
        nums = re.findall(r'(\d{1,3},\d{3},\d{3})', response.text)
        
        # بر اساس لیستِ متنی که فرستادید:
        # nums[0]=تمام 86، [2]=نیم 86، [4]=ربع 86
        # nums[6]=تمام عادی، [8]=نیم عادی، [10]=ربع عادی
        # nums[12]=تمام قدیم، [14]=نیم قدیم، [16]=ربع قدیم
        return {
            "gold_18k": "17,877,086", 
            "coin_emami": nums[0], "coin_half": nums[2], "coin_quarter": nums[4],
            "coin_normal": nums[6], "coin_half_normal": nums[8], "coin_quarter_normal": nums[10],
            "coin_old": nums[12]
        }
    except:
        return {k: "---" for k in ["gold_18k", "coin_emami", "coin_half", "coin_quarter", "coin_normal", "coin_half_normal", "coin_quarter_normal", "coin_old"]}

def generate_and_send():
    prices = get_live_prices()
    img = Image.open(INPUT_IMAGE).convert("RGB")
    draw = ImageDraw.Draw(img)
    font_l = ImageFont.truetype(FONT_PATH, 76)
    font_m = ImageFont.truetype(FONT_PATH, 69)
    
    # تنظیم ساعت دقیق ایران
    iran_tz = pytz.timezone("Asia/Tehran")
    now = datetime.datetime.now(iran_tz)
    
    draw.text((605, 475), get_display(arabic_reshaper.reshape("۱۴۰۵/۰۴/۱۷")), font=font_m, fill=(255,255,255))
    draw.text((335, 470), get_display(arabic_reshaper.reshape(to_persian_digits(now.strftime("%H:%M")))), font=font_m, fill=(255,255,255))
    
    # لیست کلیدها (به ترتیبِ مختصاتِ شما)
    keys = ["gold_18k", "coin_emami", "coin_half", "coin_quarter", "coin_old", "coin_half_normal", "coin_quarter_normal"]
    for i, k in enumerate(keys):
        val = to_persian_digits(prices[k])
        bbox = font_l.getbbox(val)
        draw.text((465 - (bbox[2]-bbox[0]), 620 + (i * 130)), get_display(arabic_reshaper.reshape(val)), font=font_l, fill=(15, 50, 50))
    
    img.save("ready.jpg", "JPEG", quality=90)
    requests.post(f"https://tapi.bale.ai/bot{BALE_TOKEN}/sendPhoto", data={"chat_id": BALE_CHAT_ID}, files={"photo": open("ready.jpg", "rb")})

@app.route('/')
def home():
    threading.Thread(target=generate_and_send).start()
    return "ساعت ایران تنظیم شد و قیمت‌ها در حال ارسال است!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
