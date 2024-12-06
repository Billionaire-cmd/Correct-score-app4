import yfinance as yf
import matplotlib.pyplot as plt
import streamlit as st

# Set the title of the app
st.title("Live Market Data Analysis")

# Sidebar for selecting trading pair and timeframe
st.sidebar.header("Select Trading Pair and Timeframe")

# List of trading pairs
symbols = [
    'GBPJPY=X',   # GBP/JPY
    'USDJPY=X',   # USD/JPY
    'XAUUSD=X',   # XAU/USD (Gold/USD)
    'US30=X',     # US30 (Dow Jones Index)
    'GBPUSD=X'    # GBP/USD
]

# Sidebar selection
selected_symbol = st.sidebar.selectbox("Choose a trading pair", symbols)

# Timeframe options in minutes
timeframe_options = {
    "1 Minute": "1m",
    "5 Minutes": "5m",
    "15 Minutes": "15m",
    "30 Minutes": "30m",
    "1 Hour": "1h",
    "4 Hours": "4h"
}

# Sidebar selection for timeframe
selected_timeframe = st.sidebar.selectbox("Choose a timeframe", list(timeframe_options.keys()))

# Mapping the selected timeframe to the yfinance string format
yf_timeframe = timeframe_options[selected_timeframe]

# Function to fetch market data for the selected trading pair and timeframe
def fetch_market_data(symbol, period="1d", interval="1m"):
    data = yf.download(symbol, period=period, interval=interval)
    return data

# Fetch the data based on the selected symbol and timeframe
market_data = fetch_market_data(selected_symbol, period="1d", interval=yf_timeframe)

# Function to plot the closing prices
def plot_closing_prices(data, symbol, timeframe):
    plt.figure(figsize=(12, 6))
    data['Close'].plot(label=f'{symbol} Close Price')
    plt.title(f'{symbol} Closing Price - {timeframe} Interval')
    plt.xlabel('Time')
    plt.ylabel('Price (USD)')
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)  # Display the plot in Streamlit

# Plot the closing prices for the selected trading pair and timeframe
plot_closing_prices(market_data, selected_symbol, selected_timeframe)
