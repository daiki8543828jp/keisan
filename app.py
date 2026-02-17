import streamlit as st
import math

def calc_hikari_fee(amount):
    """光証券の手数料計算 (円未満切り捨て)"""
    if amount <= 0:
        return 0
    elif amount <= 3000:
        return math.floor(amount * 0.09999)
    elif amount <= 218000:
        return 2750
    elif amount <= 1000000:
        return math.floor((amount * 0.0115) * 1.1)
    elif amount <= 5000000:
        return math.floor((amount * 0.009 + 2500) * 1.1)
    elif amount <= 10000000:
        return math.floor((amount * 0.007 + 12500) * 1.1)
    elif amount <= 30000000:
        return math.floor((amount * 0.00575 + 25000) * 1.1)
    elif amount <= 50000000:
        return math.floor((amount * 0.00375 + 85000) * 1.1)
    elif amount <= 100000000:
        return math.floor((amount * 0.00225 + 160000) * 1.1)
    elif amount <= 300000000:
        return math.floor((amount * 0.002 + 185000) * 1.1)
    elif amount <= 500000000:
        return min(1100000, math.floor((amount * 0.00125 + 410000) * 1.1))
    else:
        return min(1100000, math.floor((amount * 0.001 + 535000) * 1.1))

def calc_hirota_fee(amount):
    """廣田証券の手数料計算 (円未満切り捨て)"""
    if amount <= 0:
        return 0
    elif amount <= 5000:
        return math.floor(amount * 0.5 * 1.1)
    elif amount <= 1000000:
        return max(2750, math.floor(amount * 0.01 * 1.1))
    elif amount <= 5000000:
        return math.floor((amount * 0.008 + 2000) * 1.1)
    elif amount <= 9000000:
        return math.floor((amount * 0.006 + 12000) * 1.1)
    elif amount <= 15000000:
        return math.floor((amount * 0.004 + 30000) * 1.1)
    else:
        return math.floor((amount * 0.002 + 60000) * 1.1)

# StreamlitのUI構築
st.title("証券会社 手数料・損益計算ツール")

broker = st.radio("証券会社を選択してください", ["光証券", "廣田証券"])

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### ▼ 購入")
    
    # --- 購入1（常に表示） ---
    buy_price_1 = st.number_input("【購入1】の取得単価 (円)", min_value=0.0, value=None, placeholder="単価を入力", step=1.0, key="b1_price")
    buy_shares_1 = st.number_input("【購入1】の株数", min_value=0, value=100, step=100, key="b1_shares")
    buy_amount_1 = None
    if buy_price_1 is not None:
        buy_amount_1 = int(buy_price_1 * buy_shares_1)
        st.markdown(f"💴 約定代金: **{buy_amount_1:,} 円**")

    st.markdown("<br>", unsafe_allow_html=True) # 少し余白を空ける

    # --- 購入2（チェックボックスで表示切替） ---
    use_buy_2 = st.checkbox("＋ 購入2を追加する")
    buy_amount_2 = None
    if use_buy_2:
        buy_price_2 = st.number_input("【購入2】の取得単価 (円)", min_value=0.0, value=None, placeholder="単価を入力", step=1.0, key="b2_price")
        buy_shares_2 = st.number_input("【購入2】の株数", min_value=0, value=100, step=100, key="b2_shares")
        if buy_price_2 is not None:
            buy_amount_2 =
