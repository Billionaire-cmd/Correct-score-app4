import streamlit as st
import requests
from bs4 import BeautifulSoup

# Streamlit app
st.title("Live Market Trading Pairs - TradingView")

# Function to fetch live trading pairs (web scraping example)
def fetch_trading_pairs():
    url = "https://www.tradingview.com/markets/"  # Replace with a valid TradingView markets URL
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        trading_pairs = []

        # Example of how to extract data from TradingView (depends on page structure)
        for pair in soup.select(".tv-data-symbol-name"):  # Update selector based on TradingView structure
            trading_pairs.append(pair.text)

        return trading_pairs
    else:
        st.error("Failed to fetch data from TradingView.")
        return []

# Fetch and display trading pairs
st.subheader("Available Trading Pairs")
trading_pairs = fetch_trading_pairs()

if trading_pairs:
    st.write("Number of Trading Pairs:", len(trading_pairs))
    for pair in trading_pairs:
        st.write(pair)
else:
    st.warning("No trading pairs available.")

# Run the app using: streamlit run script_name.py
