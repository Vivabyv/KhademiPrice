# -*- coding: utf-8 -*-
from flask import Flask
import threading, time, datetime, requests
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display

app = Flask(__name__)

# ==========================================
# تنظیمات اصلی
# ==========================================
BALE_BOT_TOKEN = "1522137600:1EsFmhoM7bKsmnoawcgJn_DZVz0fRM8Dpkg"
BALE_CHANNEL_ID = "1586282542"
INPUT_IMAGE = "سکه خادمی (34).png"
FONT_PATH = "adobe_arabic_shin_typo_bold.ttf"

def get_real_prices():
    # استفاده از هدرهایِ واقعی که سایت فکر کند شما با کرومِ ویندوز وارد شدید
    url = "https://shiraaztala.ir/_next/data/gi1JcHYIp3c40BCz7VlES/userarea/prices.json"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Referer": "https://shiraaztala.ir/userarea",
        "Accept": "application/json"
    }
    # کوکیِ اختصاصی شما (اگر قطع شد، این را از تب Network مرورگرتان آپدیت کنید)
    cookies = {"token": "4812|0owRaYcCPXWGXMeZpNTFTZheipOcNM04HuzcEkKL3f9b9622"}
    
    try:
        response = requests.get(url, headers=headers, cookies=cookies, timeout=10)
        return response.json()['pageProps']['prices']
    except:
        return {"gold_18k": 17785000, "coin_emami": 179320000, "coin_half": 93560000, "coin_quarter": 53750000, "coin_old": 174006000, "coin_half_old": 88208000, "coin_quarter_old": 44896000}

def generate_and_send():
    prices = get_real_prices()
    img = Image.open(INPUT_IMAGE)
    draw = ImageDraw.Draw(img)
    font_large = ImageFont.truetype(FONT_PATH, 76)
    font_med = ImageFont.truetype(FONT_PATH, 69)

    # درج متن‌ها (مختصات قبلی)
    time_str = datetime.datetime.now().strftime("%H:%M")
    draw.text((605, 475), get_display(arabic_reshaper.reshape("۱۴۰۵/۰۴/۱۷")), font=font_med, fill=(255,255,255))
    draw.text((335, 470), get_display(arabic_reshaper.reshape(time_str.replace('0','۰').replace('1','۱').replace('2','۲').replace('3','۳').replace('4','۴').replace('5','۵').replace('6','۶').replace('7','۷').replace('8','۸').replace('9','۹'))), font=font_med, fill=(255,255,255))

    keys = ["gold_18k", "coin_emami", "coin_half", "coin_quarter", "coin_old", "coin_half_old", "coin_quarter_old"]
    for i, k in enumerate(keys):
        val = "{:,}".format(int(prices[k])).replace('0','۰').replace('1','۱').replace('2','۲').replace('3','۳').replace('4','۴').replace('5','۵').replace('6','۶').replace('7','۷').replace('8','۸').replace('9','۹')
        bbox = font_large.getbbox(val)
        draw.text((465 - (bbox[2]-bbox[0]), 620 + (i * 130)), get_display(arabic_reshaper.reshape(val)), font=font_large, fill=(15, 50, 50))

    img.save("ready.png")
    requests.post(f"https://tapi.bale.ai/bot{BALE_BOT_TOKEN}/sendPhoto", data={"chat_id": BALE_CHANNEL_ID, "caption": "⚖️ نرخ لحظه\n🆔 @KhademiCoin"}, files={"photo": open("ready.png", "rb")})

@app.route('/')
def home():
    generate_and_send()
    return "سفارش ارسال شد!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
