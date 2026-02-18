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

def calc_kosei_fee(amount):
    """光世証券の手数料計算 (税込表に基づく、最低1100円、円未満切り捨て)"""
    if amount <= 0:
        return 0
    
    # 税込の料率で計算
    if amount <= 1000000:
        fee = amount * 0.00601
    elif amount <= 5000000:
        fee = amount * 0.00440 + 1606
    elif amount <= 10000000:
        fee = amount * 0.00315 + 7848
    elif amount <= 30000000:
        fee = amount * 0.00234 + 15988
    elif amount <= 50000000:
        fee = amount * 0.00134 + 46018
    elif amount <= 100000000:
        fee = amount * 0.00074 + 75993
    elif amount <= 300000000:
        fee = amount * 0.00066 + 84243
    elif amount <= 500000000:
        fee = amount * 0.00041 + 158493
    else:
        fee = amount * 0.00033 + 199743
        
    # 最低手数料1,100円を適用し、小数点以下を切り捨てて返す
    return max(1100, math.floor(fee))

# StreamlitのUI構築
st.title("証券会社 手数料・損益計算ツール")

# ▼ 証券会社の選択肢に「光世証券」を追加
broker = st.radio("証券会社を選択してください", ["光証券", "廣田証券", "光世証券"])

# 株数の選択肢リストを作成（100株から10万株まで、100株刻み）
share_options = list(range(100, 100100, 100))

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### ▼ 購入")
    
    # --- 購入1（常に表示） ---
    buy_price_1 = st.number_input("【購入1】の取得単価 (円)", min_value=0.0, value=None, placeholder="単価を入力", step=1.0, key="b1_price")
    buy_shares_1 = st.selectbox("【購入1】の株数", options=share_options, index=0, key="b1_shares")
    buy_amount_1 = None
    if buy_price_1 is not None:
        buy_amount_1 = int(buy_price_1 * buy_shares_1)
        st.markdown(f"💴 約定代金: **{buy_amount_1:,} 円**")

    st.markdown("<br>", unsafe_allow_html=True) 

    # --- 購入2（チェックボックスで表示切替） ---
    use_buy_2 = st.checkbox("＋ 購入2を追加する")
    buy_amount_2 = None
    if use_buy_2:
        buy_price_2 = st.number_input("【購入2】の取得単価 (円)", min_value=0.0, value=None, placeholder="単価を入力", step=1.0, key="b2_price")
        buy_shares_2 = st.selectbox("【購入2】の株数", options=share_options, index=0, key="b2_shares")
        if buy_price_2 is not None:
            buy_amount_2 = int(buy_price_2 * buy_shares_2)
            st.markdown(f"💴 約定代金: **{buy_amount_2:,} 円**")
            
        st.markdown("<br>", unsafe_allow_html=True)

    # --- 購入3（チェックボックスで表示切替） ---
    use_buy_3 = st.checkbox("＋ 購入3を追加する")
    buy_amount_3 = None
    if use_buy_3:
        buy_price_3 = st.number_input("【購入3】の取得単価 (円)", min_value=0.0, value=None, placeholder="単価を入力", step=1.0, key="b3_price")
        buy_shares_3 = st.selectbox("【購入3】の株数", options=share_options, index=0, key="b3_shares")
        if buy_price_3 is not None:
            buy_amount_3 = int(buy_price_3 * buy_shares_3)
            st.markdown(f"💴 約定代金: **{buy_amount_3:,} 円**")

with col2:
    st.markdown("#### ▼ 売却")
    sell_price = st.number_input("【売却】の単価 (円)", min_value=0.0, value=None, placeholder="単価を入力", step=1.0, key="s_price")
    sell_shares = st.selectbox("【売却】の株数", options=share_options, index=0, key="s_shares")
    sell_amount = None
    if sell_price is not None:
        sell_amount = int(sell_price * sell_shares)
        st.markdown(f"💴 約定代金: **{sell_amount:,} 円**")

st.markdown("---")

# 必須項目（購入1と売却）の単価が入力されているかチェック
if buy_amount_1 is not None and sell_amount is not None:
    
    # ▼ 手数料計算用の関数を3社対応に変更
    if broker == "光証券":
        fee_func = calc_hikari_fee
    elif broker == "廣田証券":
        fee_func = calc_hirota_fee
    else:
        fee_func = calc_kosei_fee
    
    # --- 購入側の計算 ---
    buy_fee_1 = fee_func(buy_amount_1)
    total_buy_cost_1 = buy_amount_1 + buy_fee_1
    
    buy_fee_2 = 0
    total_buy_cost_2 = 0
    if buy_amount_2 is not None:
        buy_fee_2 = fee_func(buy_amount_2)
        total_buy_cost_2 = buy_amount_2 + buy_fee_2

    buy_fee_3 = 0
    total_buy_cost_3 = 0
    if buy_amount_3 is not None:
        buy_fee_3 = fee_func(buy_amount_3)
        total_buy_cost_3 = buy_amount_3 + buy_fee_3
        
    # 購入支払総額（購入代金 + 購入手数料 の合計）
    total_buy_cost = total_buy_cost_1 + total_buy_cost_2 + total_buy_cost_3
    
    # --- 売却側の計算 ---
    sell_fee = fee_func(sell_amount)
    total_sell_revenue = sell_amount - sell_fee
    
    # --- 損益計算 ---
    profit = total_sell_revenue - total_buy_cost

    # --- 結果の表示 ---
    st.markdown("### 計算結果")
    
    st.write(f"**【購入1】:** 約定代金 {buy_amount_1:,}円 + 手数料 {buy_fee_1:,}円 = **支払 {total_buy_cost_1:,}円**")
    if buy_amount_2 is not None:
        st.write(f"**【購入2】:** 約定代金 {buy_amount_2:,}円 + 手数料 {buy_fee_2:,}円 = **支払 {total_buy_cost_2:,}円**")
    if buy_amount_3 is not None:
        st.write(f"**【購入3】:** 約定代金 {buy_amount_3:,}円 + 手数料 {buy_fee_3:,}円 = **支払 {total_buy_cost_3:,}円**")
        
    st.write(f"**🔴 購入・支払総額: {total_buy_cost:,}円**")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.write(f"**【売　却】:** 約定代金 {sell_amount:,}円 - 手数料 {sell_fee:,}円 = **受取 {total_sell_revenue:,}円**")
    st.write(f"**🔵 売却・受取総額: {total_sell_revenue:,}円**")
    
    st.markdown("---")

    if profit > 0:
        st.success(f"**💰 最終損益: +{profit:,}円 (利益)**")
    elif profit < 0:
        st.error(f"**💸 最終損益: {profit:,}円 (損失)**")
    else:
        st.info(f"**⚖️ 最終損益: 0円**")
        
else:
    # まだ入力されていない時に表示するメッセージ
    st.info("💡 【購入1】と【売却】の単価を入力すると、ここに計算結果が表示されます。")
