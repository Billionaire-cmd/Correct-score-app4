import pandas as pd
import numpy as np
import yfinance as yf
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import talib  # For technical indicators

# Fetch historical price data
symbol = "AAPL"  # Replace with your chosen asset symbol
data = yf.download(symbol, start="2020-01-01", end="2024-12-06")
data['Date'] = data.index

# Add technical indicators
data['RSI'] = talib.RSI(data['Close'], timeperiod=14)
data['UpperBand'], data['MiddleBand'], data['LowerBand'] = talib.BBANDS(data['Close'], timeperiod=20)

# Prepare data for prediction
data['Days'] = (data['Date'] - data['Date'].min()).dt.days
X = data[['Days']]
y = data['Close']

# Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = LinearRegression()
model.fit(X_train, y_train)

# Predict future prices
future_days = 30  # Predict next 30 days
future_dates = pd.date_range(data['Date'].max(), periods=future_days + 1)[1:]
future = pd.DataFrame({'Date': future_dates, 'Days': (future_dates - data['Date'].min()).days})
future['Predicted_Close'] = model.predict(future[['Days']])

# Visualization
plt.figure(figsize=(12, 6))
plt.plot(data['Date'], data['Close'], label="Historical Close Prices")
plt.plot(future['Date'], future['Predicted_Close'], label="Predicted Close Prices", linestyle="--")
plt.title(f"Price Prediction for {symbol}")
plt.xlabel("Date")
plt.ylabel("Price")
plt.legend()
plt.grid()
plt.show()

# Optimal Entry/Exit
entry_price = future['Predicted_Close'].iloc[0] * 0.95  # Entry at 5% discount from first predicted price
exit_price = future['Predicted_Close'].max() * 0.98   # Exit at 2% below the peak predicted price
print(f"Optimal Entry Price: ${entry_price:.2f}")
print(f"Optimal Exit Price: ${exit_price:.2f}")
