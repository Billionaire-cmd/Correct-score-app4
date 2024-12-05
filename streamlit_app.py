import streamlit as st
import pandas as pd
from alpha_vantage.foreignexchange import ForeignExchange
import datetime

# Your Alpha Vantage API Key
api_key = 'your_alpha_vantage_api_key'  # Replace with your actual Alpha Vantage API key

# Create an instance of the ForeignExchange class
fx = ForeignExchange(key=api_key)

# Streamlit app layout
st.title("Forex Market Moving Average Strategy")

# Currency pair input
currency_pair = st.text_input("Enter Forex Pair (e.g., EUR/USD)", "EUR/USD").upper()

# Moving average period input
ma_period = st.slider("Moving Average Period", 5, 100, 20)

# Fetch Forex data using Alpha Vantage API
def fetch_forex_data(from_symbol, to_symbol):
    try:
        data, meta_data = fx.get_currency_exchange_intraday(from_symbol=from_symbol, to_symbol=to_symbol, interval='5min')
        df = pd.DataFrame.from_dict(data).T  # Transpose to have the correct format
        df.index = pd.to_datetime(df.index)  # Convert index to datetime
        df = df[['4. close']].rename(columns={'4. close': 'Close'})  # Select Close price
        return df
    except Exception as e:
        st.error(f"Error fetching data for {currency_pair}: {e}")
        return pd.DataFrame()  # Return empty DataFrame in case of error

# Extract the base and quote currency from the pair
from_symbol, to_symbol = currency_pair.split('/')

# Fetch data for the selected Forex pair
data = fetch_forex_data(from_symbol, to_symbol)

# Check if data is available
if not data.empty:
    # Calculate Moving Average
    data['MA'] = data['Close'].rolling(ma_period).mean()

    # Plot the data using Streamlit
    st.line_chart(data[['Close', 'MA']])
else:
    st.write("No data available to display.")

