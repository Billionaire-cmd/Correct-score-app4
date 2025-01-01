import streamlit as st
import pandas as pd
import pandas_ta as ta
import random

# Configure Streamlit App
st.set_page_config(page_title="Real-Time Trading Advisor", layout="wide")
st.title("Real-Time Trading Advisor for Swing & Scalping")

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

# Generate simulated real-time data
def fetch_market_data(symbol, timeframe):
    data_length = 100
    data = {
        "time": pd.date_range(start="2025-01-01", periods=data_length, freq="1min"),
        "open": [random.uniform(100, 200) for _ in range(data_length)],
        "high": [random.uniform(100, 200) for _ in range(data_length)],
        "low": [random.uniform(100, 200) for _ in range(data_length)],
        "close": [random.uniform(100, 200) for _ in range(data_length)],
    }
    return pd.DataFrame(data)

# Fetch and display market data
df = fetch_market_data(selected_symbol, selected_timeframe)

# Calculate technical indicators using pandas_ta
df['RSI'] = ta.rsi(df['close'], length=rsi_period)
df['EMA_Short'] = ta.ema(df['close'], length=ema_short_period)
df['EMA_Long'] = ta.ema(df['close'], length=ema_long_period)
bb = ta.bbands(df['close'], length=bb_period, std=bb_dev)
df['BB_Upper'] = bb['BBU_{}'.format(bb_period)]
df['BB_Lower'] = bb['BBL_{}'.format(bb_period)]

# Display data and indicators
st.subheader("Market Data with Indicators")
st.dataframe(df.tail(10))

# Provide trading recommendations
latest = df.iloc[-1]
rsi = latest['RSI']
advice = None
if rsi < 30 and latest['close'] < latest['BB_Lower'] and latest['EMA_Short'] > latest['EMA_Long']:
    advice = "Strong BUY Signal (Oversold Conditions)"
elif rsi > 70 and latest['close'] > latest['BB_Upper'] and latest['EMA_Short'] < latest['EMA_Long']:
    advice = "Strong SELL Signal (Overbought Conditions)"
else:
    advice = "No clear trading signal. Hold for now."

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
if latest['EMA_Short'] > latest['EMA_Long']:
    st.write("Swing Trading: BUY trend confirmed with EMA crossover.")
elif latest['EMA_Short'] < latest['EMA_Long']:
    st.write("Swing Trading: SELL trend confirmed with EMA crossover.")

# Real-time updates
st.sidebar.header("Real-Time Updates")
st.sidebar.write("Click the button below to refresh the analysis.")
if st.sidebar.button("Refresh Data"):
    st.experimental_rerun()
