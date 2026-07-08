# -*- coding: utf-8 -*-
from flask import Flask
from playwright.sync_api import sync_playwright
import threading, requests, datetime
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display

app = Flask(__name__)

# مختصات ثابت شما
FONT_PATH = "adobe_arabic_shin_typo_bold.ttf"
INPUT_IMAGE = "سکه خادمی (34).png"

def get_live_prices_with_chrome():
    with sync_playwright() as p:
        browser = p.chromium.launch() # اجرای کروم در پس‌زمینه
        page = browser.new_page()
        page.goto("https://shiraaztala.ir/userarea")
        # اینجا باید منطق ورود به پنل یا خواندنِ قیمت‌ها باشد
        # فعلاً به صورت عمومی فرض کردیم قیمت‌ها در این آدرس هستند:
        page.goto("https://shiraaztala.ir/userarea/prices") 
        content = page.content()
        # در اینجا با دستوراتی مثل page.query_selector قیمت‌ها را استخراج می‌کنیم
        browser.close()
    return {"gold_18k": 17800000} # نمونه دیتای استخراج شده

def generate_and_send():
    # همان منطق قبلی برای ساخت عکس
    # ...
    pass

@app.route('/')
def home():
    threading.Thread(target=generate_and_send).start()
    return "درخواست دریافت قیمت زنده با کروم ثبت شد!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
