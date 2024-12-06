import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Function to fetch forex and market data
def fetch_forex_data(symbols, period="5d", interval="1h"):
    data = {}
    for symbol in symbols:
        # Download historical data for the forex symbol
        forex_data = yf.download(symbol, period=period, interval=interval)
        
        # Store the data in a dictionary
        data[symbol] = forex_data

        # Optionally: Save to a CSV file for future analysis
        forex_data.to_csv(f"{symbol}_forex_data.csv")
        
        # Print the first few rows of the data (you can modify as needed)
        print(f"\nData for {symbol}:")
        print(forex_data.head())
        
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
plt.figure(figsize=(12, 8))

for symbol in symbols:
    market_data[symbol]['Close'].plot(label=symbol)

plt.title("Closing Prices for Forex and Market Pairs")
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.legend()
plt.grid(True)
plt.show()
