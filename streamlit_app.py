import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime
import time

# Portfolio Tracker with Alerts
st.title("Trading Portfolio Tracker")

# Portfolio data
if "portfolio" not in st.session_state:
    st.session_state.portfolio = pd.DataFrame(columns=["Asset", "Quantity", "Entry Price", "Profit/Loss", "Percentage Change"])

# Function to get current price of asset
def get_current_price(symbol):
    data = yf.download(symbol, period="1d", interval="1m")
    return data['Close'].iloc[-1]

# User Input
asset = st.selectbox("Select Asset", ['AAPL', 'TSLA', 'GOOG', 'AMZN', 'BTC-USD'])
quantity = st.number_input(f"Enter Quantity of {asset}", min_value=1)
entry_price = st.number_input(f"Enter Entry Price for {asset}", min_value=1.0, step=0.1)

# Add Trade to Portfolio
if st.button("Add Trade"):
    current_price = get_current_price(asset)
    profit_loss = (current_price - entry_price) * quantity
    percentage_change = (profit_loss / (entry_price * quantity)) * 100
    new_trade = {"Asset": asset, "Quantity": quantity, "Entry Price": entry_price, 
                 "Profit/Loss": profit_loss, "Percentage Change": percentage_change}
    st.session_state.portfolio = st.session_state.portfolio.append(new_trade, ignore_index=True)

    st.write(f"Current Price of {asset}: ${current_price:.2f}")
    st.write(f"Profit/Loss: ${profit_loss:.2f}")
    st.write(f"Percentage Change: {percentage_change:.2f}%")

# Portfolio Data
st.subheader("Your Portfolio")
st.write(st.session_state.portfolio)

# Total Portfolio Performance
total_value = st.session_state.portfolio["Profit/Loss"].sum()
st.write(f"Total Portfolio Profit/Loss: ${total_value:.2f}")

# Visualization of Portfolio Performance
fig, ax = plt.subplots()
ax.bar(st.session_state.portfolio["Asset"], st.session_state.portfolio["Profit/Loss"])
ax.set_xlabel("Assets")
ax.set_ylabel("Profit/Loss ($)")
ax.set_title("Portfolio Performance")
st.pyplot(fig)

# Price Alert System (example)
alert_price = st.number_input("Set Price Alert for Asset", min_value=1.0)
if st.button("Set Alert"):
    alert_price_current = get_current_price(asset)
    if alert_price_current >= alert_price:
        st.write(f"Alert: {asset} has reached your set price of ${alert_price:.2f}!")
    else:
        st.write(f"{asset} is still below your alert price.")
