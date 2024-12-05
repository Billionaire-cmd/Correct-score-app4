import streamlit as st
import pandas as pd
import yfinance as yf  # For fetching stock prices
from datetime import datetime

# Title
st.title("Trading Portfolio Tracker")

# Sample Portfolio
st.subheader("Enter Your Trades")

# User Inputs for the Portfolio
asset = st.selectbox("Select Asset", ['AAPL', 'TSLA', 'GOOG', 'AMZN', 'BTC-USD'])
quantity = st.number_input(f"Enter Quantity of {asset}", min_value=1)
entry_price = st.number_input(f"Enter Entry Price for {asset}", min_value=1.0, step=0.1)

# Fetch the latest market price
def get_current_price(symbol):
    data = yf.download(symbol, period="1d", interval="1m")
    return data['Close'].iloc[-1]

# Get current price for the selected asset
current_price = get_current_price(asset)

# Calculate profit or loss
profit_loss = (current_price - entry_price) * quantity
percentage_change = (profit_loss / (entry_price * quantity)) * 100

# Display Results
st.write(f"Current Price of {asset}: ${current_price:.2f}")
st.write(f"Profit/Loss: ${profit_loss:.2f}")
st.write(f"Percentage Change: {percentage_change:.2f}%")

# Store the portfolio in a dataframe
if "portfolio" not in st.session_state:
    st.session_state.portfolio = pd.DataFrame(columns=["Asset", "Quantity", "Entry Price", "Profit/Loss", "Percentage Change"])

# Append new trade to portfolio
new_trade = {"Asset": asset, "Quantity": quantity, "Entry Price": entry_price, 
             "Profit/Loss": profit_loss, "Percentage Change": percentage_change}
st.session_state.portfolio = st.session_state.portfolio.append(new_trade, ignore_index=True)

# Show Portfolio
st.subheader("Your Portfolio")
st.write(st.session_state.portfolio)

# Total Portfolio Performance
total_value = st.session_state.portfolio["Profit/Loss"].sum()
st.write(f"Total Portfolio Profit/Loss: ${total_value:.2f}")
