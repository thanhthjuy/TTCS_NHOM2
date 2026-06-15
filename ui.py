"""Các thành phần giao diện cho chatbot Streamlit FPT Shop."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import streamlit as st

from products import Product, format_price_vnd, get_product_badges


def load_css(path: str = "styles.css") -> None:
    p = Path(path)
    if p.exists():
        st.markdown(f"<style>{p.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)


def render_header() -> None:
    st.markdown(
        """
        <section class="hero">
          <div class="hero-title-row">
            <div class="hero-logo">FPT</div>
            <div>
              <h1 class="hero-title">Trợ lý AI FPT Shop</h1>
              <p class="hero-subtitle">Hệ thống tư vấn điện thoại thông minh</p>
            </div>
          </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_quick_suggestions() -> Optional[str]:
    st.markdown('<div class="quick-title">Gợi ý nhanh</div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)

    picks = [
        ("📱 Dưới 10 triệu pin trâu", "Máy pin trâu dưới 10 triệu"),
        ("🎮 Gaming tốt", "Tư vấn máy chơi game tốt tầm giá 10-15 triệu"),
        ("📷 Camera đẹp", "Máy chụp ảnh đẹp dưới 15 triệu"),
        ("🍎 iPhone", "Tư vấn iPhone phù hợp nhu cầu học tập và quay chụp"),
    ]

    chosen = None

    for col, (label, msg) in zip([c1, c2, c3, c4], picks):
        if col.button(label, use_container_width=True):
            chosen = msg

    return chosen


def render_sidebar(
    df_stats: Dict[str, int],
    brands: List[str],
    price_range_vnd: Tuple[int, int],
) -> Dict[str, Any]:

    st.sidebar.markdown(
        """
        <div class="side-glass">
          <h3 class="side-title">Bộ lọc sản phẩm</h3>
          <p class="side-subtitle">Lọc theo giá, hãng và tìm kiếm</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    min_vnd, max_vnd = price_range_vnd

    if min_vnd <= 0 or max_vnd <= 0:
        chosen_min, chosen_max = 0, 0
    else:
        chosen_min, chosen_max = st.sidebar.slider(
            "Khoảng giá (VND)",
            min_value=int(min_vnd),
            max_value=int(max_vnd),
            value=(int(min_vnd), int(max_vnd)),
            step=100_000,
            format="%d",
        )

    selected_brands = st.sidebar.multiselect(
        "Hãng",
        options=brands,
        default=brands,
        placeholder="Chọn hãng",
    )
    search = st.sidebar.text_input(
        "Tìm kiếm sản phẩm",
        placeholder="..."
    )
    sort_mode = st.sidebar.selectbox(
        "Sắp xếp",
        options=[
            "Mặc định",
            "Giá tăng dần",
            "Giá giảm dần",
            "Tên (A-Z)"
        ],
    )

    st.sidebar.markdown("### Thống kê")

    c1, c2 = st.sidebar.columns(2)

    c1.metric("Tổng SP", df_stats.get("total", 0))
    c2.metric("Đang hiển thị", df_stats.get("shown", 0))

    st.sidebar.metric("Số hãng", df_stats.get("brands", 0))

    clear = st.sidebar.button(
        "Xóa cuộc trò chuyện",
        use_container_width=True,
        type="primary"
    )

    return {
        "min_price_vnd": int(chosen_min),
        "max_price_vnd": int(chosen_max),
        "brands": selected_brands,
        "search": search,
        "sort_mode": sort_mode,
        "clear_chat": clear,
    }


def typing_dots(container) -> None:
    container.markdown(
        '<div class="typing-dots"><span></span><span></span><span></span></div>',
        unsafe_allow_html=True,
    )


def render_chat(messages: List[Dict[str, Any]]) -> None:

    for msg in messages:

        avatar = "🧑" if msg["role"] == "user" else "✨"

        with st.chat_message(msg["role"], avatar=avatar):

            bubble = (
                "bubble-user"
                if msg["role"] == "user"
                else "bubble-assistant"
            )

            st.markdown(
                f'<div class="chat-bubble {bubble}">{msg["content"]}</div>',
                unsafe_allow_html=True,
            )

            if msg["role"] == "assistant":
                recos = msg.get("recommendations", [])

                if recos:
                    render_product_cards(recos)


def render_product_cards(recommendations: List[Product]) -> None:

    st.markdown(
        '<div class="reco-title">Sản phẩm đề xuất</div>',
        unsafe_allow_html=True
    )

    if not recommendations:
        return

    cols_per_row = 3

    for start in range(0, len(recommendations), cols_per_row):

        cols = st.columns(cols_per_row)

        row_products = recommendations[start:start + cols_per_row]

        for col, p in zip(cols, row_products):

            with col:

                badges = "".join(
                    [
                        f'<span class="badge-chip">{b}</span>'
                        for b in get_product_badges(p)
                    ]
                )

                name = str(p.get("name", ""))

                st.markdown(
                    '<div class="product-card">',
                    unsafe_allow_html=True
                )

                img = str(p.get("image_url", ""))

                if img:

                    st.image(
                        img,
                        use_container_width=True
                    )

                else:

                    st.markdown(
                        '<div class="img-placeholder">Không có ảnh</div>',
                        unsafe_allow_html=True
                    )

                st.markdown(
                    f'<div class="product-brand">{p.get("brand","")}</div>',
                    unsafe_allow_html=True
                )

                st.markdown(
                    f'<div class="product-name">{name}</div>',
                    unsafe_allow_html=True
                )

                st.markdown(
                    f'<div class="product-price">{format_price_vnd(p.get("price_vnd"))}</div>',
                    unsafe_allow_html=True
                )

                st.markdown(
                    f'<div class="badge-wrap">{badges}</div>',
                    unsafe_allow_html=True
                )

                if p.get("description"):

                    st.markdown(
                        f'<p class="product-desc">{p.get("description")}</p>',
                        unsafe_allow_html=True
                    )

                st.markdown(
                    "</div>",
                    unsafe_allow_html=True
                )

#streamlit run app.py