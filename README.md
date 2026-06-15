# FPT Shop AI Assistant (Streamlit + DeepSeek)

Do an dai hoc: **Xay dung chatbot tu van san pham dien thoai cho doanh nghiep FPT Shop su dung mo hinh DeepSeek**.

## Tinh nang chinh

- Du lieu dien thoai mau day du (Samsung, iPhone, Xiaomi, OPPO, Vivo, Realme)
- Sidebar filter: gia, hang, tim kiem, sap xep, thong ke
- Chat UI premium (dark mode + glassmorphism) giong app AI startup
- AI DeepSeek (`deepseek-chat`) tu van nhu nhan vien ban hang
- Xu ly loi API: retry + timeout + fallback local de app khong crash

## Cai dat

```bash
pip install -r requirements.txt
```

## Cau hinh DeepSeek API

Mo file `.env` va them:

```env
DEEPSEEK_API_KEY=YOUR_DEEPSEEK_API_KEY
```

Neu can doi endpoint:

```env
DEEPSEEK_API_BASE=https://api.deepseek.com
```

## Chay app

```bash
streamlit run app.py
```

## Cau truc project

- `app.py`: entry point, session memory, chat loop
- `products.py`: xu ly pandas DataFrame, filter/search/sort, badge/format gia
- `ai.py`: DeepSeek API client + fallback local
- `ui.py`: UI components (header/sidebar/chat/cards/typing)
- `styles.css`: custom CSS premium dark glassmorphism
- `requirements.txt`: dependencies
