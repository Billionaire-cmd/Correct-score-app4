import streamlit as st
import pandas as pd
import v20
import datetime

# OANDA API setup
api_key = 'your_oanda_api_key'  # Replace with your OANDA API key
account_id = 'your_oanda_account_id'  # Replace with your OANDA account ID

# Create an OANDA client instance
client = v20.Client(access_token=api_key)

# Streamlit app layout
st.title("Forex Market Moving Average Strategy")

# Currency pair input
currency_pair = st.text_input("Enter Forex Pair (e.g., EUR/USD)", "EUR/USD").upper()

# Moving average period input
ma_period = st.slider("Moving Average Period", 5, 100, 20)

# Fetch Forex data from OANDA API
def fetch_forex_data(from_symbol, to_symbol):
    try:
        # Set the start date and end date for the data retrieval
        end_date = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        start_date = (datetime.datetime.now() - datetime.timedelta(days=365)).strftime('%Y-%m-%dT%H:%M:%S')

        # Fetch the data for the given currency pair
        response = client.pricing.get(account_id, instruments=f"{from_symbol}_{to_symbol}")
        prices = response.get('prices', [])

        # Parse the data into a DataFrame
        data = pd.DataFrame(prices)
        data['time'] = pd.to_datetime(data['time'])
        data.set_index('time', inplace=True)
        data = data[['closeBid']]  # Use 'closeBid' as the closing price
        data.rename(columns={'closeBid': 'Close'}, inplace=True)

        return data
    except Exception as e:
        st.error(f"Error fetching data for {currency_pair}: {e}")
        return pd.DataFrame()  # Return empty DataFrame in case of error

# Extract the base and quote currency from the pair
from_symbol, to_symbol = currency_pair.split('/')

# Fetch data for the selected Forex pair
data = fetch_forex_data(from_symbol, to_symbol)

# Check if data is available
if not data.empty:
    # Calculate moving average
    data['MA'] = data['Close'].rolling(ma_period).mean()

    # Plot the data using Streamlit
    st.line_chart(data[['Close', 'MA']])
else:
    st.write("No data available to display.")
