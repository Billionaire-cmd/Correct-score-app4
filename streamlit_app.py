ma_period = st.slider("Moving Average Period", 5, 100, 20)
data['MA'] = data['Close'].rolling(ma_period).mean()
st.line_chart(data[['Close', 'MA']])
