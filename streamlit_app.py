import yfinance as yf
stock = st.text_input("Enter Stock Ticker:", "AAPL")
data = yf.download(stock, start="2023-01-01")
st.line_chart(data['Close'])


ma_period = st.slider("Moving Average Period", 5, 100, 20)
data['MA'] = data['Close'].rolling(ma_period).mean()
st.line_chart(data[['Close', 'MA']])
