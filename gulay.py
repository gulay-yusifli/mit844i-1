import requests
from bs4 import BeautifulSoup
import time

# Telegram konfiqurasiyası
BOT_TOKEN = "7589537251:AAFcfx8GKj90cFQYiFfCpnUqXwPysyrC0y8"
CHAT_ID = "5798795140"  # DÜZGÜN chat ID budur!

# Məhsulun izlənəcək URL-i (misal üçün Trendyol)
PRODUCT_URL = "https://www.trendyol.com/sr?q=samsung%20telefon"

# Qiymət limiti (əgər qiymət bu limitdən aşağıdırsa, xəbər göndərilsin)
PRICE_LIMIT = 10000  # dəyişə bilərsən

# Telegram-a mesaj göndərən funksiya
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': message,
        'parse_mode': 'HTML'
    }
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        print("✅ Telegram mesajı göndərildi!")
    else:
        print("❌ Telegram mesaj göndərilə bilmədi:", response.text)

# Scraping funksiyası
def scrape_site():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    }
    response = requests.get(PRODUCT_URL, headers=headers)
    if response.status_code != 200:
        print("❌ Saytdan cavab alınmadı:", response.status_code)
        return

    soup = BeautifulSoup(response.text, "html.parser")

    products = soup.find_all("div", class_="p-card-wrppr")

    print(f"🔎 Tapılan məhsul sayı: {len(products)}")

    if not products:
        print("⚠ Məhsul tapılmadı.")
        return

    for product in products:
        name_tag = product.find("span", class_="prdct-desc-cntnr-name")
        price_tag = product.find("div", class_="prc-box-dscntd")

        if name_tag and price_tag:
            name = name_tag.get_text(strip=True)
            price_text = price_tag.get_text(strip=True).replace("TL", "").replace(".", "").replace(",", ".")
            try:
                price = float(price_text)
            except:
                continue

            print(f"Model: {name} | Qiymət: {price} TL")

            if price < PRICE_LIMIT:
                message = f"Yeni <b>{name}</b> tapıldı!\nQiymət: <b>{price} TL</b>\nLink: {PRODUCT_URL}"
                send_telegram_message(message)
                break
    else:
        print("⚠ Qiymət limitinə uyğun məhsul tapılmadı.")

# Dövri şəkildə yoxlamaq (məsələn, hər 1 saatdan bir)
while True:
    scrape_site()
    print("🔄 10 saniyə gözlənilir...\n")
    time.sleep(10)  # Test üçün 10 saniyə
