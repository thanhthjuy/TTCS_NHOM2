from __future__ import annotations

import os
import re
from typing import Dict, List, Tuple

import google.generativeai as genai
from dotenv import load_dotenv

from products import Product, format_product_for_prompt

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()

if GEMINI_API_KEY:

    genai.configure(
        api_key=GEMINI_API_KEY
    )


def _call_gemini(messages: List[Dict[str, str]]) -> str:

    if not GEMINI_API_KEY:
        raise RuntimeError("missing_gemini_key")

    model = genai.GenerativeModel(
        "gemini-1.5-flash"
    )

    prompt = ""

    for msg in messages:

        role = msg.get("role", "")
        content = msg.get("content", "")

        if role == "system":

            prompt += f"""
[SYSTEM]
{content}

"""

        elif role == "user":

            prompt += f"""
[USER]
{content}

"""

    response = model.generate_content(prompt)

    if not response.text:
        return ""

    return response.text.strip()


def _extract_budget_vnd(text: str) -> Tuple[int, int]:

    raw = text.lower()

    nums = [int(x) for x in re.findall(r"\d+", raw)]

    if not nums:
        return 0, 0

    n = nums[0]

    value = n * 1_000_000 if n < 1000 else n

    if "duoi" in raw or "dưới" in raw:
        return 0, value

    if "tren" in raw or "trên" in raw:
        return value, 999_999_999

    if "tu" in raw and len(nums) >= 2:

        a = nums[0] * 1_000_000
        b = nums[1] * 1_000_000

        return min(a, b), max(a, b)

    return 0, 0


def _build_system_prompt(products: List[Product]) -> str:

    product_text = "\n".join(
        format_product_for_prompt(p)
        for p in products[:20]
    )

    return f"""
Bạn là chatbot AI tư vấn điện thoại cho FPT Shop.

Hãy trả lời hoàn toàn bằng tiếng Việt có dấu.

Phong cách trả lời:
- Thân thiện
- Tự nhiên như nhân viên tư vấn thật
- Ngắn gọn, dễ hiểu
- Không quá dài dòng

Chỉ được tư vấn sản phẩm dựa trên danh sách bên dưới.

Quy tắc tư vấn:
- gaming → ưu tiên hiệu năng, chip mạnh, khả năng xử lý game
- camera → ưu tiên khả năng chụp ảnh
- pin → ưu tiên dung lượng pin và thời gian sử dụng
- học tập → ưu tiên sự ổn định, pin và khả năng sử dụng lâu dài

Khi tư vấn sản phẩm hãy nêu:
- Tên máy
- Giá
- Điểm mạnh phù hợp với nhu cầu khách hàng

Danh sách sản phẩm:

{product_text}
"""


def _pick_recommendations(
    user_text: str,
    products: List[Product],
    limit: int = 8
) -> List[Product]:

    text = user_text.lower()

    scored = []

    budget_min, budget_max = _extract_budget_vnd(text)

    for product in products:

        score = 0

        content = f"""
{product.get("name", "")}
{product.get("description", "")}
{product.get("battery", "")}
{product.get("camera", "")}
{product.get("performance", "")}
""".lower()

        price = int(product.get("price_vnd") or 0)

        # Gaming
        if "gaming" in text or "game" in text:

            if (
                "snapdragon" in content
                or "dimensity" in content
                or "gaming" in content
            ):
                score += 5

        # Camera
        if (
            "camera" in text
            or "chup" in text
            or "chụp" in text
        ):

            if "mp" in content:
                score += 4

        # Pin
        if "pin" in text:

            if (
                "5000" in content
                or "5500" in content
                or "6000" in content
            ):
                score += 4

        # Giá
        if budget_max and price <= budget_max:
            score += 5

        if budget_min and price >= budget_min:
            score += 5

        scored.append((score, product))

    ranked = sorted(
        scored,
        key=lambda x: x[0],
        reverse=True
    )

    result = [
        item[1]
        for item in ranked
        if item[0] > 0
    ]

    if result:
        return result[:limit]

    return products[:limit]


def _local_sales_reply(
    user_message: str,
    recommendations: List[Product]
) -> str:

    if not recommendations:

        return (
            "Mình chưa tìm được sản phẩm phù hợp. "
            "Bạn cho mình thêm ngân sách nhé."
        )

    lines = [
        "Mình gợi ý cho bạn các mẫu máy sau:"
    ]

    for p in recommendations:

        price = p.get("price_vnd")

        if isinstance(price, int):
            price_text = f"{price:,}".replace(",", ".") + "đ"
        else:
            price_text = "Liên hệ"

        lines.append(
            f"- {p.get('name')} - {price_text}"
        )

    lines.append(
        "Bạn còn yêu cầu gì không?"
    )

    return "\n".join(lines)


def generate_chatbot_reply(
    user_message: str,
    chat_history: List[Dict[str, str]],
    products: List[Product],
):

    recommendations = _pick_recommendations(
        user_message,
        products
    )

    history = []

    for item in chat_history[-6:]:

        role = (
            "Khách"
            if item["role"] == "user"
            else "Tư vấn viên"
        )

        history.append(
            f"{role}: {item['content']}"
        )

    history_text = "\n".join(history)

    messages = [
        {
            "role": "system",
            "content": _build_system_prompt(products)
        },
        {
            "role": "user",
            "content": history_text
        },
        {
            "role": "user",
            "content": user_message
        }
    ]

    try:

        answer = _call_gemini(messages)

        if not answer:

            answer = _local_sales_reply(
                user_message,
                recommendations
            )

        return answer, recommendations, ""

    except Exception as e:

        fallback = _local_sales_reply(
            user_message,
            recommendations
        )

        return fallback, recommendations, str(e)