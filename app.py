# -*- coding: utf-8 -*-
from flask import Flask
import threading, requests, re, datetime, pytz
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display

app = Flask(__name__)

BALE_TOKEN = "1522137600:1EsFmhoM7bKsmnoawcgJn_DZVz0fRM8Dpkg"
BALE_CHAT_ID = "1586282542"
FONT_PATH = "adobe_arabic_shin_typo_bold.ttf"
INPUT_IMAGE = "سکه خادمی (34).png"
API_KEY = "f23de2487d6ebe28a48e552080403890"

def get_live_prices():
    try:
        # استفاده از ScraperAPI برای لود کردنِ کاملِ صفحه و اجرای جاوااسکریپت
        target_url = "https://shiraaztala.ir/userarea"
        url = f"http://api.scraperapi.com?api_key={API_KEY}&url={target_url}&render=true"
        response = requests.get(url, timeout=60)
        text = response.text
        
        # استخراج قیمت‌ها
        def find_price(name):
            match = re.search(f"{name}.*?(\d{{1,3}},\d{{3}},\d{{3}})", text, re.DOTALL)
            return match.group(1) if match else "---"

        return {
            "gold_18k": "17,877,086", 
            "coin_emami": find_price("تمام 86"),
            "coin_half": find_price("نیم 86"),
            "coin_quarter": find_price("ربع 86"),
            "coin_old": find_price("تمام بانکی قدیم"),
            "coin_half_old": find_price("نیم بانکی قدیم"),
            "coin_quarter_old": find_price("ربع بانکی قدیم")
        }
    except Exception as e:
        print(f"Error: {e}")
        return {k: "---" for k in ["gold_18k", "coin_emami", "coin_half", "coin_quarter", "coin_old", "coin_half_old", "coin_quarter_old"]}

def generate_and_send():
    prices = get_live_prices()
    img = Image.open(INPUT_IMAGE).convert("RGB")
    draw = ImageDraw.Draw(img)
    font_l = ImageFont.truetype(FONT_PATH, 76)
    font_m = ImageFont.truetype(FONT_PATH, 69)
    
    # تنظیم ساعت دقیق ایران
    iran_tz = pytz.timezone("Asia/Tehran")
    now = datetime.datetime.now(iran_tz)
    
    # چاپ تاریخ و ساعت
    draw.text((605, 475), get_display(arabic_reshaper.reshape("۱۴۰۵/۰۴/۱۷")), font=font_m, fill=(255,255,255))
    draw.text((335, 470), get_display(arabic_reshaper.reshape(now.strftime("%H:%M").replace('0','۰').replace('1','۱').replace('2','۲').replace('3','۳').replace('4','۴').replace('5','۵').replace('6','۶').replace('7','۷').replace('8','۸').replace('9','۹'))), font=font_m, fill=(255,255,255))
    
    # چاپ لیست قیمت‌ها
    keys = ["gold_18k", "coin_emami", "coin_half", "coin_quarter", "coin_old", "coin_half_old", "coin_quarter_old"]
    for i, k in enumerate(keys):
        val = prices[k].replace('0','۰').replace('1','۱').replace('2','۲').replace('3','۳').replace('4','۴').replace('5','۵').replace('6','۶').replace('7','۷').replace('8','۸').replace('9','۹')
        bbox = font_l.getbbox(val)
        draw.text((465 - (bbox[2]-bbox[0]), 620 + (i * 130)), get_display(arabic_reshaper.reshape(val)), font=font_l, fill=(15, 50, 50))
    
    img.save("ready.jpg", "JPEG", quality=90)
    requests.post(f"https://tapi.bale.ai/bot{BALE_TOKEN}/sendPhoto", data={"chat_id": BALE_CHAT_ID}, files={"photo": open("ready.jpg", "rb")})

@app.route('/')
def home():
    threading.Thread(target=generate_and_send).start()
    return "ربات با موتور ScraperAPI فعال شد!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
