import streamlit as st
import finnhub

# Set up the Finnhub API client
api_key = "YOUR_FINNHUB_API_KEY"  # Replace with your Finnhub API key
finnhub_client = finnhub.Client(api_key=api_key)

# Streamlit app
st.title("Live Market Trading Pairs")

# Dropdown to select a market
markets = {
    "US Stocks": "US",
    "Forex": "FOREX",
    "Cryptocurrency": "CRYPTO",
    "Indices": "INDEX"
}
selected_market = st.selectbox("Select a market to fetch trading pairs:", list(markets.keys()))

# Fetch trading pairs
if st.button("Fetch Trading Pairs"):
    try:
        # Fetch symbols based on selected market
        market_type = markets[selected_market]
        symbols = finnhub_client.stock_symbols(market_type.lower())
        trading_pairs = [symbol['displaySymbol'] for symbol in symbols]
        
        if trading_pairs:
            selected_pair = st.selectbox("Select a trading pair to analyze:", trading_pairs)
            st.success(f"You selected: {selected_pair}")
        else:
            st.warning("No trading pairs found.")
    except Exception as e:
        st.error(f"An error occurred: {e}")
