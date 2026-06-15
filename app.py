import streamlit as st

from ai import generate_chatbot_reply

from products import (
SAMPLE_PRODUCTS,
to_dataframe,
get_price_bounds_vnd,
filter_df,
df_to_products,
)

from ui import (
load_css,
render_header,
render_sidebar,
render_chat,
render_quick_suggestions,
typing_dots,
)

st.set_page_config(
page_title="FPT Shop AI Assistant",
page_icon="📱",
layout="wide",
)

def init_state():

    if "messages" not in st.session_state:

        st.session_state.messages = [
            {
                "role": "assistant",
                "content": (
                    "Xin chào! Mình là chatbot AI tư vấn điện thoại của FPT Shop."
                ),
                "recommendations": []
            }
        ]

def main():

    load_css()

    init_state()

    render_header()

    df = to_dataframe(SAMPLE_PRODUCTS)

    brands = sorted(df["brand"].dropna().unique().tolist())

    min_vnd, max_vnd = get_price_bounds_vnd(df)

    filters = render_sidebar(
        df_stats={
            "total": len(df),
            "shown": len(df),
            "brands": len(brands),
        },
        brands=brands,
        price_range_vnd=(min_vnd, max_vnd),
    )

    df_filtered = filter_df(
        df,
        filters["min_price_vnd"],
        filters["max_price_vnd"],
        filters["brands"],
        filters["search"],
        filters["sort_mode"],
    )

    picked = render_quick_suggestions()

    render_chat(st.session_state.messages)

    user_input = st.chat_input("Nhập nhu cầu của bạn...")

    if not user_input and picked:
        user_input = picked

    if not user_input:
        return

    st.session_state.messages.append({
        "role": "user",
        "content": user_input,
        "recommendations": []
    })

    with st.chat_message("user", avatar="🧑"):

        st.markdown(
            f'<div class="chat-bubble bubble-user">{user_input}</div>',
            unsafe_allow_html=True
        )

    products = df_to_products(df_filtered, limit=30)

    with st.chat_message("assistant", avatar="✨"):

        box = st.empty()

        typing_dots(box)

        answer, recommendations, err = generate_chatbot_reply(
            user_input,
            st.session_state.messages,
            products
        )

        box.empty()

        st.markdown(
            f'<div class="chat-bubble bubble-assistant">{answer}</div>',
            unsafe_allow_html=True
        )

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "recommendations": recommendations
    })

    st.rerun()


if __name__ == "__main__":
    main()
