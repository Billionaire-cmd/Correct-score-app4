import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go

# App Title
st.title("Trading Analytics Dashboard")

# Select Asset Type
asset_type = st.selectbox("Select Asset Type", ["Cryptocurrency", "Stock", "Forex"])

# User Input for Ticker/Asset
asset = st.text_input(f"Enter {asset_type} Symbol (e.g., BTC, AAPL, EUR/USD):", "BTC")

# Fetching Real-Time Data
if st.button("Get Data"):
    if asset_type == "Cryptocurrency":
        url = f"https://api.coingecko.com/api/v3/coins/{asset.lower()}/market_chart?vs_currency=usd&days=7"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            prices = data['prices']
            df = pd.DataFrame(prices, columns=['Timestamp', 'Price'])
            df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='ms')

            # Display Data Table
            st.write(f"Last 7 Days Price Data for {asset.upper()}:")
            st.write(df)

            # Plot Price Chart
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df['Timestamp'], y=df['Price'], mode='lines', name=f"{asset.upper()} Price"))
            fig.update_layout(title=f"{asset.upper()} Price Trend", xaxis_title="Date", yaxis_title="Price (USD)")
            st.plotly_chart(fig)

        else:
            st.error("Failed to fetch data. Please check the asset name.")
    else:
        st.warning(f"Support for {asset_type} is coming soon!")
