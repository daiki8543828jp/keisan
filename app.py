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
    buy_amount = st.number_input("購入時の約定代金 (円)", min_value=0, value=100000, step=10000)
with col2:
    sell_amount = st.number_input("売却時の約定代金 (円)", min_value=0, value=110000, step=10000)

# 選択された証券会社に基づいて手数料を計算
if broker == "光証券":
    buy_fee = calc_hikari_fee(buy_amount)
    sell_fee = calc_hikari_fee(sell_amount)
else:
    buy_fee = calc_hirota_fee(buy_amount)
    sell_fee = calc_hirota_fee(sell_amount)

# 損益計算
total_buy_cost = buy_amount + buy_fee
total_sell_revenue = sell_amount - sell_fee
profit = total_sell_revenue - total_buy_cost

st.markdown("---")
st.markdown("### 計算結果")
st.write(f"**購入時:** 約定代金 {buy_amount:,}円 + 手数料 {buy_fee:,}円 = **支払総額 {total_buy_cost:,}円**")
st.write(f"**売却時:** 約定代金 {sell_amount:,}円 - 手数料 {sell_fee:,}円 = **受取総額 {total_sell_revenue:,}円**")

if profit > 0:
    st.success(f"**最終損益: +{profit:,}円 (利益)**")
elif profit < 0:
    st.error(f"**最終損益: {profit:,}円 (損失)**")
else:
    st.info(f"**最終損益: 0円**")