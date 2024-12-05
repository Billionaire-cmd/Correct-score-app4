import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf

# Title of the app
st.title("Moving Average Strategy")

# Get the stock data
st.sidebar.header("Stock Input")
stock_symbol = st.sidebar.text_input("Enter Stock Symbol (e.g., AAPL, MSFT)", "AAPL")
start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2020-01-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("today"))

# Fetching data
data = yf.download(stock_symbol, start=start_date, end=end_date)
if not data.empty:
    st.subheader(f"Data for {stock_symbol}")
    st.write(data)

    # Slider for moving average period
    ma_period = st.slider("Moving Average Period", 5, 100, 20)

    # Calculate moving average
    data['MA'] = data['Close'].rolling(ma_period).mean()

    # Plotting the data
    st.line_chart(data[['Close', 'MA']])

    # Optional: Display raw data
    if st.checkbox("Show Raw Data"):
        st.write(data)
else:
    st.error("No data found. Please check the stock symbol or date range.")
