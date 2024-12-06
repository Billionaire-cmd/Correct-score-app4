import pandas as pd
import numpy as np
import yfinance as yf
import talib
import matplotlib.pyplot as plt

# Fetch historical price data
symbol = "AAPL"  # Replace with the asset symbol
data = yf.download(symbol, start="2022-01-01", end="2024-12-06")

# Calculate RSI with period 1
data['RSI'] = talib.RSI(data['Close'], timeperiod=1)

# Define levels
data['Signal'] = np.nan
data.loc[data['RSI'] <= 9, 'Signal'] = "Strong Buy (LL Entry)"
data.loc[data['RSI'] >= 90, 'Signal'] = "Strong Sell (HH Entry)"
data.loc[data['RSI'] == 50, 'Signal'] = "Take Profit (Resistance)"
data.loc[data['RSI'] == 80, 'Signal'] = "Strong Sell (LH Entry)"
data.loc[data['RSI'] == 30, 'Signal'] = "Buy to QLH / Sell to HL MSS"
data.loc[data['RSI'] == 40, 'Signal'] = "Buy Entry (HL)"
data.loc[data['RSI'] == 60, 'Signal'] = "Sell Entry (LH Supply)"
data.loc[data['RSI'] == 16, 'Signal'] = "Strong Buy Support (HL)"
data.loc[data['RSI'] == 70, 'Signal'] = "Buy to LH MSS / Sell to QHL"
data.loc[data['RSI'] == 85, 'Signal'] = "Strong Sell Entry"

# Filter for signals
signals = data[data['Signal'].notna()]

# Plot RSI and signals
plt.figure(figsize=(14, 7))
plt.plot(data['RSI'], label="RSI", color='blue')
plt.axhline(9, color='green', linestyle='--', label="LL Entry (Strong Buy)")
plt.axhline(90, color='red', linestyle='--', label="HH Entry (Strong Sell)")
plt.axhline(50, color='purple', linestyle='--', label="Take Profit Resistance")
plt.axhline(80, color='orange', linestyle='--', label="LH Entry (Sell)")
plt.axhline(30, color='gray', linestyle='--', label="Buy to QLH / Sell to HL MSS")
plt.axhline(40, color='brown', linestyle='--', label="Buy Entry (HL)")
plt.axhline(16, color='green', linestyle='-', label="Strong Buy Support (HL)")
plt.axhline(70, color='pink', linestyle='--', label="Buy to LH MSS / Sell to QHL")
plt.axhline(85, color='red', linestyle='-', label="Strong Sell Entry")
plt.legend(loc="best")
plt.title(f"{symbol} RSI with Custom Levels")
plt.xlabel("Date")
plt.ylabel("RSI")
plt.grid()
plt.show()

# Print signals
print(signals[['RSI', 'Signal']])
