import streamlit as st
import finnhub

# Function to initialize the Finnhub API client
def initialize_finnhub(api_key):
    try:
        return finnhub.Client(api_key=api_key)
    except Exception as e:
        st.error(f"Error initializing Finnhub client: {e}")
        return None

# Function to fetch trading pairs based on market selection
def fetch_trading_pairs(market_type, finnhub_client):
    try:
        symbols = finnhub_client.stock_symbols(market_type)
        return [symbol['displaySymbol'] for symbol in symbols]
    except Exception as e:
        st.error(f"Error fetching trading pairs: {e}")
        return []

# Streamlit app UI
st.title("Live Market Trading Pairs")

# Input: API Key (You can use a text box for the user to input it or hardcode if preferred)
api_key = st.text_input("Enter your Finnhub API Key:", type="password")

# Check if API key is valid and initialize Finnhub client
if api_key:
    finnhub_client = initialize_finnhub(api_key)

    if finnhub_client:
        # Dropdown to select a market (e.g., US Stocks, Forex, Cryptocurrency)
        markets = {
            "US Stocks": "US",
            "Forex": "FOREX",
            "Cryptocurrency": "CRYPTO",
            "Indices": "INDEX"
        }
        
        selected_market = st.selectbox("Select a market to fetch trading pairs:", list(markets.keys()))
        market_type = markets[selected_market]

        # Fetch trading pairs when button is clicked
        if st.button("Fetch Trading Pairs"):
            trading_pairs = fetch_trading_pairs(market_type, finnhub_client)
            
            if trading_pairs:
                selected_pair = st.selectbox("Select a trading pair to analyze:", trading_pairs)
                st.success(f"You selected: {selected_pair}")
            else:
                st.warning("No trading pairs found. Please try again later.")
    else:
        st.error("Invalid API Key. Please check and try again.")
else:
    st.warning("ct952upr01qt3llhear0ct952upr01qt3llhearg")
