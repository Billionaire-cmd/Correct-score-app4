import streamlit as st
import pandas as pd
import yfinance as yf

# Title of the app
st.title("Moving Average Strategy")

# Sidebar for user inputs
st.sidebar.header("User Inputs")
stock_symbol = st.sidebar.text_input("Stock Symbol (e.g., AAPL, MSFT, TSLA)", "AAPL")
start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2020-01-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("today"))

# Fetch stock data
st.subheader(f"Data for {stock_symbol}")
try:
    # Download stock data
    data = yf.download(stock_symbol, start=start_date, end=end_date)

    # Check if data is retrieved
    if data.empty:
        st.error("No data found. Please enter a valid stock symbol or adjust the date range.")
    else:
        # Display raw data (optional)
        if st.checkbox("Show Raw Data"):
            st.write(data)

        # Ensure the required 'Close' column exists
        if 'Close' not in data.columns:
            st.error("The selected stock data does not have a 'Close' price column.")
        else:
            # Moving average slider
            ma_period = st.slider("Moving Average Period", min_value=5, max_value=100, value=20)

            # Calculate moving average
            data['MA'] = data['Close'].rolling(ma_period).mean()

            # Check if the moving average was calculated properly
            if 'MA' in data.columns:
                # Line chart for closing prices and moving average
                st.line_chart(data[['Close', 'MA']])
            else:
                st.error("Failed to calculate the moving average.")

except Exception as e:
    st.error(f"An unexpected error occurred: {e}")
