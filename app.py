# -*- coding: utf-8 -*-
from flask import Flask
import requests

app = Flask(__name__)

@app.route('/')
def home():
    url = "https://shiraaztala.ir/_next/data/gi1JcHYIp3c40BCz7VlES/userarea/prices.json"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Referer": "https://shiraaztala.ir/userarea"
    }
    cookies = {"token": "4812|0owRaYcCPXWGXMeZpNTFTZheipOcNM04HuzcEkKL3f9b9622"}
    
    try:
        response = requests.get(url, headers=headers, cookies=cookies, timeout=15)
        if response.status_code == 200:
            return f"سایت پاسخ داد: {response.json()['pageProps']['prices']}"
        else:
            return f"خطای سایت: کد {response.status_code} - متن: {response.text}"
    except Exception as e:
        return f"خطای اتصال: {str(e)}"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
