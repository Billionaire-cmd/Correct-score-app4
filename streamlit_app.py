import streamlit as st
import pandas as pd
import yfinance as yf

# Title of the app
st.title("Moving Average Strategy with Streamlit")

# Sidebar for user inputs
st.sidebar.header("User Inputs")
stock_symbol = st.sidebar.text_input("Stock Symbol (e.g., AAPL, MSFT, TSLA)", "AAPL")
start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2020-01-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("today"))

# Fetch stock data
st.subheader(f"Stock Data for {stock_symbol}")
try:
    data = yf.download(stock_symbol, start=start_date, end=end_date)

    if data.empty:
        st.error("No data found. Please enter a valid stock symbol or adjust the date range.")
    else:
        # Display the raw data
        if st.checkbox("Show Raw Data"):
            st.write(data)

        # Add a slider for the moving average period
        ma_period = st.slider("Moving Average Period", min_value=5, max_value=100, value=20)

        # Calculate moving average
        data['MA'] = data['Close'].rolling(ma_period).mean()

        # Line chart for closing prices and moving average
        st.line_chart(data[['Close', 'MA']])

except Exception as e:
    st.error(f"An error occurred: {e}")
