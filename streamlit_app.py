import streamlit as st
import pandas as pd
from alpha_vantage.foreignexchange import ForeignExchange
import time

# Set your Alpha Vantage API key here
api_key = "YOUR_ALPHA_VANTAGE_API_KEY"

# Streamlit app title
st.title("Forex & Derivatives Trading System")

# Sidebar for user inputs
st.sidebar.header("User Inputs")
pair = st.sidebar.selectbox("Select Forex Pair", ["EURUSD", "GBPUSD", "USDJPY", "AUDUSD"])
derivative_pair = st.sidebar.selectbox("Select Derivative Pair (e.g., CFD)", ["AAPL", "TSLA", "GOOG"])
ma_period = st.sidebar.slider("Moving Average Period", 5, 100, 20)

# Function to fetch Forex data from Alpha Vantage
def fetch_forex_data(pair, start_date="2020-01-01", end_date="today"):
    try:
        fx = ForeignExchange(key=api_key)
        data, meta_data = fx.get_currency_exchange_history(from_symbol=pair[:3], to_symbol=pair[3:], outputsize="full")
        
        # Convert data to a pandas DataFrame
        df = pd.DataFrame(data).T
        df['timestamp'] = pd.to_datetime(df.index)
        df.set_index('timestamp', inplace=True)
        
        # Filter data by date range
        df = df.loc[start_date:end_date]
        if df.empty:
            st.error(f"No data found for {pair}. Please check the ticker symbol.")
        return df
    except Exception as e:
        st.error(f"Error fetching data for {pair}: {str(e)}")
        return pd.DataFrame()

# Function for calculating moving averages
def add_moving_average(data, period):
    data['MA'] = data['4. close'].rolling(window=period).mean()  # Using the closing price from Alpha Vantage
    return data

# Fetch and display data for selected pair
if pair:
    data = fetch_forex_data(pair)
    
    if not data.empty:
        data = add_moving_average(data, ma_period)
        
        # Display data
        st.subheader(f"Data for {pair}")
        st.line_chart(data[['4. close', 'MA']])

# For Derivatives (example, using Apple stock CFD)
if derivative_pair:
    data = fetch_forex_data(derivative_pair)
    
    if not data.empty:
        data = add_moving_average(data, ma_period)
        
        # Display data
        st.subheader(f"Data for {derivative_pair}")
        st.line_chart(data[['4. close', 'MA']])

# Backtesting functionality
st.sidebar.subheader("Backtesting")
backtest_button = st.sidebar.button("Run Backtest")
if backtest_button:
    # Implement backtesting logic for selected pair
    st.write("Running backtest...")
