import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import datetime

# Portfolio Tracker with Multiple Assets
st.title("Advanced Portfolio Tracker")

# Initialize portfolio data
if "portfolio" not in st.session_state:
    st.session_state.portfolio = pd.DataFrame(columns=["Asset", "Quantity", "Entry Price", "Profit/Loss", "Percentage Change"])

# Function to get current price of asset
def get_current_price(symbol):
    data = yf.download(symbol, period="1d", interval="1m")
    return data['Close'].iloc[-1]

# Function to get historical data for asset
def get_historical_data(symbol, start_date, end_date):
    data = yf.download(symbol, start=start_date, end=end_date)
    return data['Close']

# User Inputs for multiple assets
assets = st.multiselect("Select Assets", ['AAPL', 'TSLA', 'GOOG', 'AMZN', 'BTC-USD', 'ETH-USD'])
if assets:
    st.write(f"Tracking assets: {', '.join(assets)}")

# User Input for Quantity and Entry Price for each asset
asset_data = {}
for asset in assets:
    asset_data[asset] = {
        "quantity": st.number_input(f"Enter Quantity of {asset}", min_value=1),
        "entry_price": st.number_input(f"Enter Entry Price for {asset}", min_value=1.0, step=0.1)
    }

# Add Trades to Portfolio
if st.button("Add Trade"):
    for asset in assets:
        quantity = asset_data[asset]["quantity"]
        entry_price = asset_data[asset]["entry_price"]
        current_price = get_current_price(asset)
        profit_loss = (current_price - entry_price) * quantity
        percentage_change = (profit_loss / (entry_price * quantity)) * 100
        new_trade = {"Asset": asset, "Quantity": quantity, "Entry Price": entry_price, 
                     "Profit/Loss": profit_loss, "Percentage Change": percentage_change}
        st.session_state.portfolio = st.session_state.portfolio.append(new_trade, ignore_index=True)

# Portfolio Data
st.subheader("Your Portfolio")
st.write(st.session_state.portfolio)

# Total Portfolio Performance
total_value = st.session_state.portfolio["Profit/Loss"].sum()
st.write(f"Total Portfolio Profit/Loss: ${total_value:.2f}")

# Visualizing Portfolio Performance
fig, ax = plt.subplots()
ax.bar(st.session_state.portfolio["Asset"], st.session_state.portfolio["Profit/Loss"])
ax.set_xlabel("Assets")
ax.set_ylabel("Profit/Loss ($)")
ax.set_title("Portfolio Performance")
st.pyplot(fig)

# Historical Data for Portfolio (optional)
st.subheader("Historical Performance of Selected Assets")
start_date = st.date_input("Start Date", value=datetime.date(2023, 1, 1))
end_date = st.date_input("End Date", value=datetime.date.today())

for asset in assets:
    historical_data = get_historical_data(asset, start_date, end_date)
    st.write(f"{asset} Historical Data")
    st.line_chart(historical_data)

