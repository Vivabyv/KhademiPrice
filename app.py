def get_live_prices():
    url = "https://shiraaztala.ir/userarea" # به جای لینک JSON، مستقیم به صفحه قیمت‌ها بروید
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "https://shiraaztala.ir/"
    }
    # استفاده از Session برای نگه داشتن کوکی‌ها
    session = requests.Session()
    response = session.get(url, headers=headers, timeout=15)
    
    # حالا در پاسخِ این صفحه، تمام قیمت‌ها در متنِ HTML وجود دارد
    # می‌توانید با کتابخانه BeautifulSoup قیمت‌ها را از داخل متن بیرون بکشید
    return "سایت پاسخ داد (حالا باید با BeautifulSoup متن را پردازش کنیم)"
