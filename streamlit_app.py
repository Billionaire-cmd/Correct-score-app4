import yfinance as yf
import matplotlib.pyplot as plt
import streamlit as st

# Set the title of the app
st.title("Market Data Analyzer")

# Function to fetch forex and market data
def fetch_forex_data(symbols, period="5d", interval="1h"):
    data = {}
    for symbol in symbols:
        try:
            # Download historical data for the forex symbol
            forex_data = yf.download(symbol, period=period, interval=interval)
            
            # Store the data in the dictionary
            data[symbol] = forex_data

            # Optionally: Save to a CSV file for future analysis
            forex_data.to_csv(f"{symbol}_forex_data.csv")
            
            # Print a message confirming successful data fetching
            print(f"Data for {symbol} fetched successfully!")
        
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
    
    return data

# List of symbols to fetch data for
symbols = [
    'GBPJPY=X',   # GBP/JPY
    'USDJPY=X',   # USD/JPY
    'XAUUSD=X',   # XAU/USD (Gold/USD)
    'US30=X',     # US30 (Dow Jones Index)
    'GBPUSD=X'    # GBP/USD
]

# Fetch data for all symbols
market_data = fetch_forex_data(symbols, period="5d", interval="1h")

# Plot closing prices for each symbol
def plot_closing_prices(market_data, symbols):
    plt.figure(figsize=(12, 8))

    for symbol in symbols:
        if symbol in market_data:
            market_data[symbol]['Close'].plot(label=symbol)

    plt.title("Closing Prices for Forex and Market Pairs")
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)  # Display the plot in Streamlit

# Call the function to plot data
plot_closing_prices(market_data, symbols)
