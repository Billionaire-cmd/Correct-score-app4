import streamlit as st
import MetaTrader5 as mt5
import pandas as pd

# Connect to MetaTrader 5
def connect_to_mt5():
    if not mt5.initialize():
        st.error(f"Failed to initialize MT5: {mt5.last_error()}")
        return False
    return True

# Login to MT5 account
def login_to_mt5(account_number, password, server):
    if not mt5.login(account_number, password=password, server=server):
        st.error(f"Failed to log in: {mt5.last_error()}")
        return False
    return True

# Get account information
def get_account_info():
    account_info = mt5.account_info()
    if account_info is None:
        st.error(f"Failed to retrieve account info: {mt5.last_error()}")
        return None
    return account_info._asdict()

# Place a trade
def place_trade(symbol, lot_size, trade_type):
    symbol_info = mt5.symbol_info(symbol)
    if not symbol_info:
        st.error(f"Symbol {symbol} not found")
        return

    if not symbol_info.visible:
        if not mt5.symbol_select(symbol, True):
            st.error(f"Failed to select symbol {symbol}")
            return

    # Create a trade request
    trade_request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot_size,
        "type": trade_type,
        "price": mt5.symbol_info_tick(symbol).ask if trade_type == mt5.ORDER_TYPE_BUY else mt5.symbol_info_tick(symbol).bid,
        "deviation": 10,
        "magic": 123456,
        "comment": "Streamlit Trade",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    # Send trade request
    result = mt5.order_send(trade_request)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        st.error(f"Trade failed: {result}")
    else:
        st.success(f"Trade successful: {result}")

# Streamlit app interface
st.title("🤖🤖🤖 MT5 Trading App")

# Connect to MT5
if connect_to_mt5():
    st.success("Connected to MetaTrader 5")

    # Login details
    account_number = st.text_input("Account Number", type="password")
    password = st.text_input("Password", type="password")
    server = st.text_input("Server")

    if st.button("Login"):
        if login_to_mt5(account_number, password, server):
            st.success("Logged in successfully!")

            # Display account information
            account_info = get_account_info()
            if account_info:
                st.write("Account Information:")
                st.json(account_info)

            # Trading section
            st.subheader("Place a Trade")
            symbol = st.text_input("Symbol (e.g., EURUSD)")
            lot_size = st.number_input("Lot Size", min_value=0.01, step=0.01)
            trade_type = st.selectbox("Trade Type", ["Buy", "Sell"])
            trade_type_code = mt5.ORDER_TYPE_BUY if trade_type == "Buy" else mt5.ORDER_TYPE_SELL

            if st.button("Execute Trade"):
                place_trade(symbol, lot_size, trade_type_code)

# Shutdown MT5 connection
if mt5.shutdown():
    st.info("MetaTrader 5 connection closed")
