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
    # 購入1（常に表示）
    buy_amount_1 = st.number_input("【購入1】の約定代金 (円)", min_value=0, value=None, placeholder="金額を入力", step=10000, key="buy1")
    if buy_amount_1 is not None:
        st.markdown(f"💴 確認: **{buy_amount_1:,} 円**")

    # 購入2（チェックボックスで表示切替）
    use_buy_2 = st.checkbox("＋ 購入2を追加する")
    buy_amount_2 = None
    if use_buy_2:
        buy_amount_2 = st.number_input("【購入2】の約定代金 (円)", min_value=0, value=None, placeholder="金額を入力", step=10000, key="buy2")
        if buy_amount_2 is not None:
            st.markdown(f"💴 確認: **{buy_amount_2:,} 円**")

    # 購入3（チェックボックスで表示切替）
    use_buy_3 = st.checkbox("＋ 購入3を追加する")
    buy_amount_3 = None
    if use_buy_3:
        buy_amount_3 = st.number_input("【購入3】の約定代金 (円)", min_value=0, value=None, placeholder="金額を入力", step=10000, key="buy3")
        if buy_amount_3 is not None:
            st.markdown(f"💴 確認: **{buy_amount_3:,} 円**")

with col2:
    st.markdown("#### ▼ 売却")
    sell_amount = st.number_input("【売却】の約定代金 (円)", min_value=0, value=None, placeholder="金額を入力", step=10000, key="sell")
    if sell_amount is not None:
        st.markdown(f"💴 確認: **{sell_amount:,} 円**")

st.markdown("---")

# 必須項目（購入1と売却）が入力されているかチェック
if buy_amount_1 is not None and sell_amount is not None:
    
    # 手数料計算用の関数を選択
    fee_func = calc_hikari_fee if broker == "光証券" else calc_hirota_fee
    
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
    
    st.markdown("<br>", unsafe_allow_html=True) # 少し余白を空ける
    
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
    st.info("💡 【購入1】と【売却】の約定代金を入力すると、ここに計算結果が表示されます。")
