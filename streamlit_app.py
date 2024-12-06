import streamlit as st
import pandas as pd
import yfinance as yf
import requests
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from datetime import datetime

# Initialize session state for portfolio
if "portfolio" not in st.session_state:
    st.session_state.portfolio = pd.DataFrame(columns=["Asset", "Quantity", "Entry Price", "Profit/Loss", "Percentage Change"])

# App Title
st.title("🤖🤖🤖💯Advanced Trading Dashboard")

# Sidebar Navigation
st.sidebar.title("Navigation")
option = st.sidebar.radio("Select a Page", ["Portfolio Tracker", "Market Analytics", "Price Prediction"])

# Utility function: Fetch real-time prices
def get_current_price(symbol):
    try:
        data = yf.download(symbol, period="1d", interval="1m")
        return data['Close'].iloc[-1]
    except:
        st.error("Error fetching the current price. Please check the symbol.")
        return None

# Utility function: Calculate profit/loss
def calculate_profit_loss(entry_price, current_price, quantity):
    profit_loss = (current_price - entry_price) * quantity
    percentage_change = (profit_loss / (entry_price * quantity)) * 100
    return profit_loss, percentage_change

# Page 1: Portfolio Tracker
if option == "Portfolio Tracker":
    st.header("Portfolio Tracker")
    st.subheader("Manage Your Investments")
    
    # User Input for Assets
    asset = st.selectbox("Select Asset", ['AAPL', 'TSLA', 'GOOG', 'AMZN', 'BTC-USD'])
    quantity = st.number_input(f"Enter Quantity of {asset}", min_value=1, step=1)
    entry_price = st.number_input(f"Enter Entry Price for {asset} (USD):", min_value=0.0, step=0.1)

    # Add Trade to Portfolio
    if st.button("Add Trade"):
        current_price = get_current_price(asset)
        if current_price is not None:
            profit_loss, percentage_change = calculate_profit_loss(entry_price, current_price, quantity)
            new_trade = {"Asset": asset, "Quantity": quantity, "Entry Price": entry_price,
                         "Profit/Loss": profit_loss, "Percentage Change": percentage_change}
            st.session_state.portfolio = st.session_state.portfolio.append(new_trade, ignore_index=True)
            st.success(f"Trade for {asset} added successfully!")
    
    # Display Portfolio
    st.subheader("Your Portfolio")
    st.write(st.session_state.portfolio)
    
    # Portfolio Performance
    total_profit_loss = st.session_state.portfolio["Profit/Loss"].sum()
    st.write(f"**Total Portfolio Profit/Loss:** ${total_profit_loss:.2f}")
    
    # Visualization
    if not st.session_state.portfolio.empty:
        fig, ax = plt.subplots()
        ax.bar(st.session_state.portfolio["Asset"], st.session_state.portfolio["Profit/Loss"])
        ax.set_xlabel("Assets")
        ax.set_ylabel("Profit/Loss ($)")
        ax.set_title("Portfolio Performance")
        st.pyplot(fig)

    # Set Price Alert
    st.subheader("Set Price Alert")
    alert_price = st.number_input("Alert Price (USD):", min_value=0.0, step=0.1)
    if st.button("Set Alert"):
        current_price = get_current_price(asset)
        if current_price is not None:
            if current_price >= alert_price:
                st.success(f"Alert: {asset} has reached your set price of ${alert_price:.2f}!")
            else:
                st.info(f"{asset} is still below your alert price.")

# Page 2: Market Analytics
elif option == "Market Analytics":
    st.header("Market Analytics")
    st.subheader("Real-Time Data Visualization")
    
    # Select Asset Type
    asset_type = st.selectbox("Select Asset Type", ["Cryptocurrency", "Stock"])
    asset = st.text_input(f"Enter {asset_type} Symbol (e.g., BTC, AAPL):", "BTC")

    # Fetch Historical Data
    if st.button("Get Data"):
        if asset_type == "Cryptocurrency":
            url = f"https://api.coingecko.com/api/v3/coins/{asset.lower()}/market_chart?vs_currency=usd&days=30"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                prices = data['prices']
                df = pd.DataFrame(prices, columns=['Timestamp', 'Price'])
                df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='ms')
                
                # Plot Data
                st.subheader(f"{asset.capitalize()} - Last 30 Days")
                fig, ax = plt.subplots()
                ax.plot(df['Timestamp'], df['Price'], label="Price (USD)")
                ax.set_xlabel("Date")
                ax.set_ylabel("Price (USD)")
                ax.set_title(f"{asset.capitalize()} Price Trend")
                st.pyplot(fig)
            else:
                st.error("Failed to fetch data. Check the asset name.")
        elif asset_type == "Stock":
            data = yf.download(asset, period="1mo", interval="1d")
            if not data.empty:
                st.line_chart(data['Close'])
            else:
                st.error("Failed to fetch data. Check the stock ticker.")

# Page 3: Price Prediction
elif option == "Price Prediction":
    st.header("AI-Powered Price Prediction")
    st.subheader("Upload Historical Data for Predictions")
    
    # File Upload (Allowing image/jpeg files)
    uploaded_file = st.file_uploader("Upload your historical price data (CSV format or JPEG image)", type=["csv", "jpeg", "jpg"])
    
    if uploaded_file is not None:
        file_extension = uploaded_file.name.split('.')[-1].lower()
        
        # Check if the uploaded file is CSV
        if file_extension == "csv":
            data = pd.read_csv(uploaded_file)
            if 'Date' in data.columns and 'Close' in data.columns:
                st.write("Uploaded Data Preview:")
                st.write(data.head())
                
                # Prepare Data for Prediction
                data['Date'] = pd.to_datetime(data['Date'])
                data['Days'] = (data['Date'] - data['Date'].min()).dt.days
                X = data[['Days']]
                y = data['Close']
                
                # Train/Test Split
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
                
                # Train Model
                model = LinearRegression()
                model.fit(X_train, y_train)
                
                # Predict Future Prices
                future_days = st.number_input("Number of Days to Predict:", min_value=1, max_value=365, value=30)
                future = np.array([[data['Days'].max() + i] for i in range(1, future_days + 1)])
                predictions = model.predict(future)
                
                # Display Predictions
                st.write(f"Predicted Prices for the next {future_days} days:")
                prediction_df = pd.DataFrame({'Day': future.flatten(), 'Predicted Price': predictions})
                st.write(prediction_df)
                
                # Plot Predictions
                st.line_chart(predictions)
            else:
                st.error("CSV must contain 'Date' and 'Close' columns!")
        
        # Check if the uploaded file is JPEG
        elif file_extension in ["jpeg", "jpg"]:
            st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
            st.success("JPEG image uploaded successfully!")
        else:
            st.error("Unsupported file type! Please upload a CSV or JPEG image.")
