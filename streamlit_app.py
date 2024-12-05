import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# Title
st.title("Crypto Price Tracker")

# User input
crypto = st.text_input("Enter Cryptocurrency (e.g., bitcoin, ethereum):", "bitcoin")

# Fetch data from API
url = f"https://api.coingecko.com/api/v3/coins/{crypto}/market_chart?vs_currency=usd&days=7"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    prices = data['prices']
    
    # Convert to DataFrame
    df = pd.DataFrame(prices, columns=['Timestamp', 'Price'])
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='ms')

    # Plot data
    st.write(f"Last 7 days price for {crypto.capitalize()}:")
    fig = px.line(df, x='Timestamp', y='Price', title=f"{crypto.capitalize()} Price Chart")
    st.plotly_chart(fig)

else:
    st.error("Failed to fetch data. Please check the cryptocurrency name.")
