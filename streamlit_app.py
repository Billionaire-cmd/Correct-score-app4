import streamlit as st
import pandas as pd
import yfinance as yf

# Streamlit app title
st.title("Forex & Derivatives Trading System")

# Sidebar for user inputs
st.sidebar.header("User Inputs")
pair = st.sidebar.selectbox("Select Forex Pair", ["EURUSD=X", "GBPUSD=X", "USDJPY=X", "AUDUSD=X"])
derivative_pair = st.sidebar.selectbox("Select Derivative Pair (e.g., CFD)", ["AAPL", "TSLA", "GOOG"])
ma_period = st.sidebar.slider("Moving Average Period", 5, 100, 20)

# Fetch data for selected Forex or Derivatives pair
def fetch_data(pair, start_date="2020-01-01", end_date="today"):
    data = yf.download(pair, start=start_date, end=end_date)
    return data

# Function for calculating moving averages
def add_moving_average(data, period):
    data['MA'] = data['Close'].rolling(window=period).mean()
    return data

# Fetch and display data for selected pair
if pair:
    data = fetch_data(pair)
    data = add_moving_average(data, ma_period)
    
    # Display data
    st.subheader(f"Data for {pair}")
    st.line_chart(data[['Close', 'MA']])

    # Trading Strategy example (Simple Moving Average crossover)
    if st.button("Run Strategy"):
        if data['Close'].iloc[-1] > data['MA'].iloc[-1]:
            st.success("Buy Signal")
        else:
            st.warning("Sell Signal")

# For Derivatives (example, using Apple stock CFD)
if derivative_pair:
    data = fetch_data(derivative_pair)
    data = add_moving_average(data, ma_period)

    # Display data
    st.subheader(f"Data for {derivative_pair}")
    st.line_chart(data[['Close', 'MA']])

    # Implement strategy for derivative pair
    if st.button("Run Strategy for Derivatives"):
        if data['Close'].iloc[-1] > data['MA'].iloc[-1]:
            st.success("Buy Signal for Derivative")
        else:
            st.warning("Sell Signal for Derivative")

# Backtesting functionality
st.sidebar.subheader("Backtesting")
backtest_button = st.sidebar.button("Run Backtest")
if backtest_button:
    # Implement backtesting logic for selected pair
    st.write("Running backtest...")
