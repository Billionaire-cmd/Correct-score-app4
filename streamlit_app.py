import streamlit as st
import cv2
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from PIL import Image

# Function to calculate Relative Strength Index (RSI)
def calculate_rsi(data, period=14):
    delta = data['Close'].diff()
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)
    
    avg_gain = pd.Series(gain).rolling(window=period).mean()
    avg_loss = pd.Series(loss).rolling(window=period).mean()
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# Function to process uploaded price chart image
def process_image(uploaded_image):
    img = cv2.cvtColor(np.array(uploaded_image), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, threshold1=30, threshold2=100)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours, img

# Function to predict price levels (support, resistance, etc.)
def predict_levels(contours):
    support = np.min([cv2.boundingRect(c)[1] for c in contours])
    resistance = np.max([cv2.boundingRect(c)[1] for c in contours])
    demand_zone = support * 0.95
    supply_zone = resistance * 1.05
    sniper_entry = demand_zone
    sniper_exit = supply_zone
    return support, resistance, demand_zone, supply_zone, sniper_entry, sniper_exit

# Function to plot price chart with zones
def plot_chart_with_zones(chart_image, support, resistance, demand_zone, supply_zone, sniper_entry, sniper_exit):
    plt.figure(figsize=(10, 5))
    plt.imshow(chart_image)
    plt.axhline(y=support, color='g', linestyle='--', label='Support Zone')
    plt.axhline(y=resistance, color='r', linestyle='--', label='Resistance Zone')
    plt.axhline(y=demand_zone, color='b', linestyle='--', label='Demand Zone')
    plt.axhline(y=supply_zone, color='orange', linestyle='--', label='Supply Zone')
    plt.axhline(y=sniper_entry, color='purple', linestyle=':', label='Sniper Entry')
    plt.axhline(y=sniper_exit, color='yellow', linestyle=':', label='Sniper Exit')
    plt.title('Price Chart with Zones')
    plt.legend()
    st.pyplot(plt)

# Function to generate RSI signals
def generate_rsi_signals(data):
    signals = []
    for index, row in data.iterrows():
        rsi = row['RSI']
        if rsi <= 9:
            signals.append("Strong Buy (LL Entry)")
        elif rsi >= 90:
            signals.append("Strong Sell (HH Entry)")
        elif rsi == 50:
            signals.append("Take Profit (Resistance)")
        elif rsi == 80:
            signals.append("Strong Sell (LH Entry)")
        elif rsi == 30:
            signals.append("Buy to QLH / Sell to HL MSS")
        elif rsi == 40:
            signals.append("Buy Entry (HL)")
        elif rsi == 60:
            signals.append("Sell Entry (LH Supply)")
        elif rsi == 16:
            signals.append("Strong Buy Support (HL)")
        elif rsi == 70:
            signals.append("Buy to LH MSS / Sell to QHL")
        elif rsi == 85:
            signals.append("Strong Sell Entry")
        else:
            signals.append(np.nan)
    data['Signal'] = signals
    return data

# Streamlit App
st.title("AI-Powered Price Prediction with RSI and Sniper Entry/Exit Points")

# Upload price chart image
uploaded_image = st.file_uploader("Upload a Price Chart Image (JPEG)", type=["jpeg", "jpg"])

# Upload price data CSV
uploaded_csv = st.file_uploader("Upload Historical Price Data (CSV)", type=["csv"])

if uploaded_csv is not None:
    # Load and process the CSV file
    data = pd.read_csv(uploaded_csv)
    data['RSI'] = calculate_rsi(data)
    data = generate_rsi_signals(data)
    
    # Display RSI signals
    st.subheader("RSI Signals")
    st.write(data[['Close', 'RSI', 'Signal']].dropna())
    
    # Plot RSI chart
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
    plt.title("RSI Chart with Custom Levels")
    plt.xlabel("Time")
    plt.ylabel("RSI")
    plt.grid()
    st.pyplot(plt)

if uploaded_image is not None:
    # Process the image
    image = Image.open(uploaded_image)
    contours, chart_image = process_image(image)
    
    # Predict levels
    support, resistance, demand_zone, supply_zone, sniper_entry, sniper_exit = predict_levels(contours)
    
    # Display levels
    st.subheader("Predicted Price Levels")
    st.write(f"Support Level: {support}")
    st.write(f"Resistance Level: {resistance}")
    st.write(f"Demand Zone: {demand_zone}")
    st.write(f"Supply Zone: {supply_zone}")
    st.write(f"Sniper Entry Point: {sniper_entry}")
    st.write(f"Sniper Exit Point: {sniper_exit}")
    
    # Plot chart with zones
    plot_chart_with_zones(chart_image, support, resistance, demand_zone, supply_zone, sniper_entry, sniper_exit)
