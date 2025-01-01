import streamlit as st
import requests
import time

# Configure Streamlit App
st.set_page_config(page_title="Real-Time Trading Advisor", layout="wide")
st.title("📉📈🤖Rabiotic Real-Time Trading Advisor for Swing & Scalping")

# Dropdown for market symbols
market_symbols = [
    "Volatility 10 Index", "Volatility 25 Index", "Volatility 50 Index",
    "Volatility 75 Index", "Volatility 100 Index", "Crash 1000 Index",
    "Crash 500 Index", "Boom 1000 Index", "Boom 500 Index", "Step Index",
    "Range Break 100 Index", "Range Break 200 Index", "EURUSD", "GBPUSD",
    "USDJPY", "USDCHF", "AUDUSD", "USDCAD", "NZDUSD", "EURGBP", "EURJPY",
    "BTCUSD", "ETHUSD", "LTCUSD", "XRPUSD", "BCHUSD", "ADAUSD", "DOTUSD",
    "BNBUSD", "SOLUSD", "DOGEUSD", "MATICUSD", "AVAXUSD"
]

selected_symbol = st.selectbox("Select Market Symbol", market_symbols)

# Timeframe selection
timeframes = ["1m", "5m", "15m", "30m", "1h", "4h", "1d"]
selected_timeframe = st.selectbox("Select Timeframe", timeframes)

# Parameters for indicators
st.sidebar.header("Indicator Settings")
rsi_period = st.sidebar.slider("RSI Period", 5, 50, 14)
ema_short_period = st.sidebar.slider("Short EMA Period", 5, 50, 10)
ema_long_period = st.sidebar.slider("Long EMA Period", 20, 200, 30)
bb_period = st.sidebar.slider("Bollinger Bands Period", 5, 50, 20)
bb_dev = st.sidebar.slider("Bollinger Bands Deviation", 0.5, 3.0, 2.0)

# Fetch real-time market data
def fetch_market_data(symbol, timeframe):
    # Example API request (replace this with your actual data source)
    url = f"https://api.example.com/get_data?symbol={symbol}&timeframe={timeframe}"
    response = requests.get(url)
    data = response.json()  # Assuming the API returns JSON data
    return data

# Calculate RSI (Relative Strength Index)
def calculate_rsi(prices, period):
    gains = [max(prices[i] - prices[i-1], 0) for i in range(1, len(prices))]
    losses = [max(prices[i-1] - prices[i], 0) for i in range(1, len(prices))]
    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period
    
    rsi = []
    rsi.append(100 - (100 / (1 + avg_gain / avg_loss)))
    
    for i in range(period, len(prices)):
        gain = max(prices[i] - prices[i-1], 0)
        loss = max(prices[i-1] - prices[i], 0)
        avg_gain = (avg_gain * (period - 1) + gain) / period
        avg_loss = (avg_loss * (period - 1) + loss) / period
        rs = avg_gain / avg_loss if avg_loss != 0 else float('inf')
        rsi.append(100 - (100 / (1 + rs)))
    
    return rsi

# Calculate EMA (Exponential Moving Average)
def calculate_ema(prices, period):
    ema = [sum(prices[:period]) / period]
    multiplier = 2 / (period + 1)
    for price in prices[period:]:
        ema.append((price - ema[-1]) * multiplier + ema[-1])
    return ema

# Calculate Bollinger Bands
def calculate_bollinger_bands(prices, period, dev):
    sma = [sum(prices[:period]) / period]
    for i in range(period, len(prices)):
        sma.append(sum(prices[i-period:i]) / period)
    
    upper_band = []
    lower_band = []
    for i in range(period, len(prices)):
        rolling_std = (sum((prices[i-period:i] - sma[i-period])**2) / period) ** 0.5
        upper_band.append(sma[i] + dev * rolling_std)
        lower_band.append(sma[i] - dev * rolling_std)
    
    return upper_band, lower_band

# Generate simulated market data (or fetch real-time data)
market_data = fetch_market_data(selected_symbol, selected_timeframe)
close_prices = [entry['close'] for entry in market_data]

# Calculate indicators
rsi = calculate_rsi(close_prices, rsi_period)[-1]
ema_short = calculate_ema(close_prices, ema_short_period)[-1]
ema_long = calculate_ema(close_prices, ema_long_period)[-1]
upper_band, lower_band = calculate_bollinger_bands(close_prices, bb_period, bb_dev)

# Latest data
latest_close = close_prices[-1]
latest_upper_band = upper_band[-1]
latest_lower_band = lower_band[-1]

# Display data and indicators
st.subheader("Market Data with Indicators")
st.write(f"Latest Close Price: {latest_close}")
st.write(f"RSI: {rsi}")
st.write(f"Short EMA: {ema_short}")
st.write(f"Long EMA: {ema_long}")
st.write(f"Bollinger Bands: Upper - {latest_upper_band}, Lower - {latest_lower_band}")

# Apply Strategy to Determine Trading Signals
advice = None

# Strategy Logic (you can expand or refine this logic)
if rsi < 30 and latest_close < latest_lower_band and ema_short > ema_long:
    advice = "Strong BUY Signal (Oversold Conditions)"
elif rsi > 70 and latest_close > latest_upper_band and ema_short < ema_long:
    advice = "Strong SELL Signal (Overbought Conditions)"
elif ema_short > ema_long:
    advice = "BUY Signal (Uptrend)"
elif ema_short < ema_long:
    advice = "SELL Signal (Downtrend)"
else:
    advice = "No clear trading signal. Hold for now."

# Display Advice
st.subheader("Trading Advice")
st.write(f"**Symbol**: {selected_symbol}")
st.write(f"**Timeframe**: {selected_timeframe}")
st.write(f"**Advice**: {advice}")

# Scalping and Swing Strategy
st.subheader("Scalping and Swing Strategy Analysis")
if rsi < 30:
    st.write("Scalping: Potential quick entry for BUY at oversold levels.")
if rsi > 70:
    st.write("Scalping: Potential quick entry for SELL at overbought levels.")
if ema_short > ema_long:
    st.write("Swing Trading: BUY trend confirmed with EMA crossover.")
elif ema_short < ema_long:
    st.write("Swing Trading: SELL trend confirmed with EMA crossover.")

# Real-time updates
st.sidebar.header("Real-Time Updates")
st.sidebar.write("Click the button below to refresh the analysis.")
if st.sidebar.button("Refresh Data"):
    st.experimental_rerun()

# Add a timer for updates (optional)
time.sleep(5)  # Simulate real-time data update every 5 seconds
