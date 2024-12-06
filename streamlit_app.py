import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Function to fetch trading pairs using Selenium
def fetch_trading_pairs():
    st.info("Fetching trading pairs... This may take a few seconds.")
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    # Set up the Selenium driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    url = "https://www.tradingview.com/markets/"  # Replace with the correct TradingView URL
    driver.get(url)

    # Wait for the page to load
    time.sleep(5)  # Adjust the delay as necessary

    # Fetch trading pairs
    trading_pairs = []
    try:
        elements = driver.find_elements(By.CSS_SELECTOR, ".tv-data-symbol-name")  # Adjust CSS selector
        trading_pairs = [element.text for element in elements if element.text.strip()]
    except Exception as e:
        st.error(f"An error occurred while fetching data: {e}")
    finally:
        driver.quit()
    
    return trading_pairs

# Streamlit app
st.title("Live Market Trading Pairs - TradingView")

# Fetch trading pairs and display them
if st.button("Fetch Trading Pairs"):
    trading_pairs = fetch_trading_pairs()

    if trading_pairs:
        st.success(f"Fetched {len(trading_pairs)} trading pairs.")
        selected_pair = st.selectbox("Select a trading pair to analyze:", trading_pairs)
        st.write(f"You selected: {selected_pair}")
    else:
        st.warning("No trading pairs available. Please try again.")
