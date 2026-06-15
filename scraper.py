from __future__ import annotations

import json
import re
from typing import List, Dict

import requests
from bs4 import BeautifulSoup


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/125.0 Safari/537.36"
    )
}


def clean_price(text: str) -> int:
    nums = re.sub(r"[^\d]", "", text)
    if nums:
        return int(nums)
    return 0


def scrape_fptshop_phones(limit: int = 30) -> List[Dict]:
    url = "https://fptshop.com.vn/dien-thoai"

    response = requests.get(url, headers=HEADERS, timeout=20)

    if response.status_code != 200:
        print("Khong truy cap duoc FPT Shop")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    products = []

    cards = soup.select(".cdt-product")

    for card in cards[:limit]:
        try:
            name_tag = card.select_one(".cdt-product__name")
            price_tag = card.select_one(".price")
            image_tag = card.select_one("img")

            if not name_tag:
                continue

            name = name_tag.get_text(strip=True)

            price = 0
            if price_tag:
                price = clean_price(price_tag.get_text())

            image = ""
            if image_tag:
                image = (
                    image_tag.get("data-src")
                    or image_tag.get("src")
                    or ""
                )

            brand = "Khac"

            lower_name = name.lower()

            if "iphone" in lower_name:
                brand = "Apple"
            elif "samsung" in lower_name:
                brand = "Samsung"
            elif "xiaomi" in lower_name:
                brand = "Xiaomi"
            elif "oppo" in lower_name:
                brand = "OPPO"
            elif "vivo" in lower_name:
                brand = "Vivo"
            elif "realme" in lower_name:
                brand = "Realme"

            product = {
                "name": name,
                "brand": brand,
                "price_vnd": price,
                "description": "Dien thoai chinh hang tai FPT Shop",
                "battery": "Dang cap nhat",
                "camera": "Dang cap nhat",
                "performance": "Dang cap nhat",
                "image_url": image,
            }

            products.append(product)

        except Exception as e:
            print("Loi:", e)

    return products


def save_products_json(products, filename="fptshop_cache_products.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(products, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    data = scrape_fptshop_phones(limit=30)

    save_products_json(data)

    print(f"Da lay {len(data)} san pham")


