"""Danh mục sản phẩm + xử lý dữ liệu cho trợ lý AI FPT Shop."""

from __future__ import annotations

import re
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd

Product = Dict[str, Any]

SAMPLE_PRODUCTS: List[Product] = [

    {
        "name": "iPhone 15",
        "brand": "Apple",
        "price_vnd": 17990000,
        "description": "iPhone cân bằng, chụp ảnh đẹp, hiệu năng mạnh.",
        "battery": "3349mAh",
        "camera": "48MP",
        "performance": "Apple A16 Bionic",
        "image_url": "https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=1200",
    },

    {
        "name": "iPhone 15 Pro Max",
        "brand": "Apple",
        "price_vnd": 29990000,
        "description": "iPhone cao cấp camera cực đẹp.",
        "battery": "4422mAh",
        "camera": "48MP Zoom 5x",
        "performance": "Apple A17 Pro",
        "image_url": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=1200",
    },

    {
        "name": "iPhone 14",
        "brand": "Apple",
        "price_vnd": 15990000,
        "description": "iPhone giá tốt cho học tập và giải trí.",
        "battery": "3279mAh",
        "camera": "12MP",
        "performance": "Apple A15",
        "image_url": "https://images.unsplash.com/photo-1510557880182-3f8cbf5c2d7d?w=1200",
    },

    {
        "name": "Samsung Galaxy S24 Ultra",
        "brand": "Samsung",
        "price_vnd": 28990000,
        "description": "Flagship Samsung gaming và camera mạnh.",
        "battery": "5000mAh",
        "camera": "200MP",
        "performance": "Snapdragon 8 Gen 3",
        "image_url": "https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?w=1200",
    },

    {
        "name": "Samsung Galaxy S24",
        "brand": "Samsung",
        "price_vnd": 21990000,
        "description": "Màn đẹp, camera đẹp, AI thông minh.",
        "battery": "4000mAh",
        "camera": "50MP",
        "performance": "Exynos 2400",
        "image_url": "https://images.unsplash.com/photo-1580910051074-3eb694886505?w=1200",
    },

    {
        "name": "Samsung Galaxy A55",
        "brand": "Samsung",
        "price_vnd": 9990000,
        "description": "Cân bằng tốt cho học tập và giải trí.",
        "battery": "5000mAh",
        "camera": "50MP",
        "performance": "Exynos 1480",
        "image_url": "https://images.unsplash.com/photo-1592750475338-74b7b21085ab?w=1200",
    },

    {
        "name": "Samsung Galaxy A35",
        "brand": "Samsung",
        "price_vnd": 7990000,
        "description": "Giá rẻ, pin trâu, màn AMOLED.",
        "battery": "5000mAh",
        "camera": "50MP",
        "performance": "Exynos 1380",
        "image_url": "https://images.unsplash.com/photo-1565849904461-04a58ad377e0?w=1200",
    },

    {
        "name": "Samsung Galaxy M54",
        "brand": "Samsung",
        "price_vnd": 10990000,
        "description": "Pin rất trâu, dùng lâu.",
        "battery": "6000mAh",
        "camera": "108MP",
        "performance": "Exynos 1380",
        "image_url": "https://images.unsplash.com/photo-1512499617640-c74ae3a79d37?w=1200",
    },

    {
        "name": "Xiaomi 14",
        "brand": "Xiaomi",
        "price_vnd": 22990000,
        "description": "Gaming mạnh, camera Leica.",
        "battery": "4610mAh",
        "camera": "50MP Leica",
        "performance": "Snapdragon 8 Gen 3",
        "image_url": "https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=1200",
    },

    {
        "name": "Redmi Note 13 Pro 5G",
        "brand": "Xiaomi",
        "price_vnd": 8490000,
        "description": "Giá rẻ, camera 200MP.",
        "battery": "5100mAh",
        "camera": "200MP",
        "performance": "Snapdragon 7s Gen 2",
        "image_url": "https://images.unsplash.com/photo-1592899677977-9c10ca588bbd?w=1200",
    },

    {
        "name": "POCO X6 Pro",
        "brand": "Xiaomi",
        "price_vnd": 9990000,
        "description": "Gaming cực mạnh tầm giá.",
        "battery": "5000mAh",
        "camera": "64MP",
        "performance": "Dimensity 8300 Ultra",
        "image_url": "https://images.unsplash.com/photo-1585060544812-6b45742d762f?w=1200",
    },

    {
        "name": "Redmi 13C",
        "brand": "Xiaomi",
        "price_vnd": 3990000,
        "description": "Máy giá rẻ cho học sinh sinh viên.",
        "battery": "5000mAh",
        "camera": "50MP",
        "performance": "Helio G85",
        "image_url": "https://images.unsplash.com/photo-1574944985070-8f3ebc6b79d2?w=1200",
    },

    {
        "name": "OPPO Reno11 F",
        "brand": "OPPO",
        "price_vnd": 8990000,
        "description": "Selfie đẹp, máy đẹp.",
        "battery": "5000mAh",
        "camera": "64MP",
        "performance": "Dimensity 7050",
        "image_url": "https://images.unsplash.com/photo-1601972602237-8c79241e468b?w=1200",
    },

    {
        "name": "OPPO Find X7",
        "brand": "OPPO",
        "price_vnd": 24990000,
        "description": "Flagship camera đẹp.",
        "battery": "5000mAh",
        "camera": "50MP Hasselblad",
        "performance": "Dimensity 9300",
        "image_url": "https://images.unsplash.com/photo-1546054454-aa26e2b734c7?w=1200",
    },

    {
        "name": "OPPO A98",
        "brand": "OPPO",
        "price_vnd": 6990000,
        "description": "Pin trâu, dùng mượt.",
        "battery": "5000mAh",
        "camera": "64MP",
        "performance": "Snapdragon 695",
        "image_url": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=1200",
    },

    {
        "name": "Vivo V30",
        "brand": "Vivo",
        "price_vnd": 10990000,
        "description": "Chân dung đẹp, selfie đẹp.",
        "battery": "5000mAh",
        "camera": "50MP Zeiss",
        "performance": "Snapdragon 7 Gen 3",
        "image_url": "https://images.unsplash.com/photo-1592899677977-9c10ca588bbd?w=1200",
    },

    {
        "name": "Vivo Y100",
        "brand": "Vivo",
        "price_vnd": 6990000,
        "description": "Pin tốt, thiết kế đẹp.",
        "battery": "5000mAh",
        "camera": "50MP",
        "performance": "Snapdragon 685",
        "image_url": "https://images.unsplash.com/photo-1567581935884-3349723552ca?w=1200",
    },

    {
        "name": "Vivo X100 Pro",
        "brand": "Vivo",
        "price_vnd": 26990000,
        "description": "Camera Zeiss cực đẹp.",
        "battery": "5400mAh",
        "camera": "50MP Zeiss",
        "performance": "Dimensity 9300",
        "image_url": "https://images.unsplash.com/photo-1512941937669-90a1b58e7e9c?w=1200",
    },

    {
        "name": "Realme GT Neo 5 SE",
        "brand": "Realme",
        "price_vnd": 7990000,
        "description": "Gaming mạnh giá tốt.",
        "battery": "5500mAh",
        "camera": "64MP",
        "performance": "Snapdragon 7+ Gen 2",
        "image_url": "https://images.unsplash.com/photo-1512499617640-c74ae3a79d37?w=1200",
    },

    {
        "name": "Realme 12 Pro+",
        "brand": "Realme",
        "price_vnd": 11990000,
        "description": "Camera zoom đẹp.",
        "battery": "5000mAh",
        "camera": "64MP Periscope",
        "performance": "Snapdragon 7s Gen 2",
        "image_url": "https://images.unsplash.com/photo-1565849904461-04a58ad377e0?w=1200",
    },

    {
        "name": "Realme C67",
        "brand": "Realme",
        "price_vnd": 4990000,
        "description": "Giá rẻ pin trâu.",
        "battery": "5000mAh",
        "camera": "108MP",
        "performance": "Snapdragon 685",
        "image_url": "https://images.unsplash.com/photo-1580910051074-3eb694886505?w=1200",
    },

    {
        "name": "ASUS ROG Phone 8",
        "brand": "ASUS",
        "price_vnd": 24990000,
        "description": "Gaming cực khủng.",
        "battery": "5500mAh",
        "camera": "50MP",
        "performance": "Snapdragon 8 Gen 3",
        "image_url": "https://images.unsplash.com/photo-1546054454-aa26e2b734c7?w=1200",
    },

    {
        "name": "ROG Phone 7",
        "brand": "ASUS",
        "price_vnd": 19990000,
        "description": "Gaming pin trâu.",
        "battery": "6000mAh",
        "camera": "50MP",
        "performance": "Snapdragon 8 Gen 2",
        "image_url": "https://images.unsplash.com/photo-1510557880182-3f8cbf5c2d7d?w=1200",
    },

    {
        "name": "Nokia G42",
        "brand": "Nokia",
        "price_vnd": 4990000,
        "description": "Bền bỉ, pin trâu.",
        "battery": "5000mAh",
        "camera": "50MP",
        "performance": "Snapdragon 480+",
        "image_url": "https://images.unsplash.com/photo-1574944985070-8f3ebc6b79d2?w=1200",
    },

    {
        "name": "Tecno Camon 30",
        "brand": "Tecno",
        "price_vnd": 6990000,
        "description": "Camera đẹp giá mềm.",
        "battery": "5000mAh",
        "camera": "50MP",
        "performance": "Helio G99",
        "image_url": "https://images.unsplash.com/photo-1567581935884-3349723552ca?w=1200",
    },

    {
        "name": "Infinix GT 20 Pro",
        "brand": "Infinix",
        "price_vnd": 8990000,
        "description": "Gaming giá rẻ.",
        "battery": "5000mAh",
        "camera": "108MP",
        "performance": "Dimensity 8200",
        "image_url": "https://images.unsplash.com/photo-1512941937669-90a1b58e7e9c?w=1200",
    },

    {
        "name": "Honor X9b",
        "brand": "Honor",
        "price_vnd": 8990000,
        "description": "Pin trâu, màn cong đẹp.",
        "battery": "5800mAh",
        "camera": "108MP",
        "performance": "Snapdragon 6 Gen 1",
        "image_url": "https://images.unsplash.com/photo-1585060544812-6b45742d762f?w=1200",
    },

    {
        "name": "Google Pixel 8",
        "brand": "Google",
        "price_vnd": 18990000,
        "description": "Camera AI đẹp.",
        "battery": "4575mAh",
        "camera": "50MP",
        "performance": "Google Tensor G3",
        "image_url": "https://images.unsplash.com/photo-1601972602237-8c79241e468b?w=1200",
    },

    {
        "name": "Nothing Phone 2",
        "brand": "Nothing",
        "price_vnd": 15990000,
        "description": "Thiết kế độc đáo.",
        "battery": "4700mAh",
        "camera": "50MP",
        "performance": "Snapdragon 8+ Gen 1",
        "image_url": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=1200",
    },
]


def to_dataframe(products: List[Product]) -> pd.DataFrame:
    """Chuyển danh sách sản phẩm sang DataFrame."""

    rows: List[Dict[str, Any]] = []

    for p in products:
        rows.append(
            {
                "name": p.get("name"),
                "brand": p.get("brand"),
                "price_vnd": p.get("price_vnd"),
                "image_url": p.get("image_url"),
                "description": p.get("description"),
                "battery": p.get("battery"),
                "camera": p.get("camera"),
                "performance": p.get("performance"),
            }
        )

    return pd.DataFrame(rows)


def get_price_bounds_vnd(df: pd.DataFrame) -> Tuple[int, int]:
    """Lấy khoảng giá nhỏ nhất và lớn nhất."""

    if df.empty:
        return 0, 0

    return int(df["price_vnd"].min()), int(df["price_vnd"].max())


def filter_df(
    df: pd.DataFrame,
    min_price_vnd: int,
    max_price_vnd: int,
    brands: Optional[List[str]],
    query: str,
    sort_mode: str,
) -> pd.DataFrame:
    """Lọc sản phẩm theo giá, hãng, từ khóa và sắp xếp."""

    out = df.copy()

    out = out[
        (out["price_vnd"] >= min_price_vnd)
        & (out["price_vnd"] <= max_price_vnd)
    ]

    if brands:
        out = out[out["brand"].isin(brands)]

    q = query.lower().strip()

    if q:
        out = out[out["name"].str.lower().str.contains(re.escape(q))]

    if sort_mode == "Giá tăng dần":
        out = out.sort_values(by="price_vnd")

    elif sort_mode == "Giá giảm dần":
        out = out.sort_values(by="price_vnd", ascending=False)

    return out.reset_index(drop=True)


def format_price_vnd(price_vnd: Any) -> str:
    """Định dạng giá tiền VNĐ."""

    if not isinstance(price_vnd, int):
        return "Liên hệ"

    return f"{price_vnd:,}".replace(",", ".") + " đ"


def format_product_for_prompt(product: Product) -> str:
    """Format sản phẩm thành chuỗi cho prompt AI."""

    return (
        f"{product['name']} | "
        f"{product['brand']} | "
        f"{format_price_vnd(product['price_vnd'])} | "
        f"{product['description']}"
    )


def get_product_badges(product: Product) -> List[str]:
    """Tạo nhãn (badge) cho sản phẩm."""

    badges = []

    content = (
        f"{product.get('description','')} "
        f"{product.get('battery','')} "
        f"{product.get('performance','')}"
    ).lower()

    if "5000" in content or "5500" in content or "6000" in content:
        badges.append("Pin trâu")

    if "snapdragon" in content or "gaming" in content:
        badges.append("Gaming")

    if "camera" in content or "108mp" in content or "200mp" in content:
        badges.append("Camera đẹp")

    return badges


def df_to_products(df: pd.DataFrame, limit: int = 30) -> List[Product]:
    """Chuyển DataFrame về danh sách sản phẩm."""

    result = []

    for _, row in df.head(limit).iterrows():
        result.append(
            {
                "name": row["name"],
                "brand": row["brand"],
                "price_vnd": row["price_vnd"],
                "image_url": row["image_url"],
                "description": row["description"],
                "battery": row["battery"],
                "camera": row["camera"],
                "performance": row["performance"],
            }
        )

    return result