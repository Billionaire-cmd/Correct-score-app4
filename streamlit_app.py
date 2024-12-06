import streamlit as st
import cv2
import numpy as np
import pandas as pd
import talib
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from PIL import Image

# Function to extract price chart from uploaded image
def process_image(uploaded_image):
    img = cv2.cvtColor(np.array(uploaded_image), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, threshold1=30, threshold2=100)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours, img

# Function to calculate RSI
def calculate_rsi(prices, period=14):
    rsi = talib.RSI(prices, timeperiod=period)
    return rsi

# Function to predict levels
def predict_levels(contours, rsi):
    support = np.min([cv2.boundingRect(c)[1] for c in contours])
    resistance = np.max([cv2.boundingRect(c)[1] for c in contours])
    demand_zone = support * 0.95
    supply_zone = resistance * 1.05
    sniper_entry = demand_zone if rsi[-1] <= 30 else None
    sniper_exit = supply_zone if rsi[-1] >= 70 else None
    return support, resistance, demand_zone, supply_zone, sniper_entry, sniper_exit

# Function to plot the chart
def plot_chart_with_zones(chart_image, support, resistance, demand_zone, supply_zone, sniper_entry, sniper_exit, rsi):
    plt.figure(figsize=(14, 7))
    plt.imshow(chart_image)
    plt.axhline(y=support, color='g', linestyle='--', label='Support Zone')
    plt.axhline(y=resistance, color='r', linestyle='--', label='Resistance Zone')
    plt.axhline(y=demand_zone, color='b', linestyle='--', label='Demand Zone')
    plt.axhline(y=supply_zone, color='orange', linestyle='--', label='Supply Zone')
    if sniper_entry:
        plt.axhline(y=sniper_entry, color='purple', linestyle=':', label='Sniper Entry')
    if sniper_exit:
        plt.axhline(y=sniper_exit, color='yellow', linestyle=':', label='Sniper Exit')
    plt.title('Price Chart with Support, Resistance, RSI, and Zones')
    plt.legend()
    plt.show()

    # Plot RSI
    plt.figure(figsize=(14, 5))
    plt.plot(rsi, label="RSI", color='blue')
    plt.axhline(30, color='green', linestyle='--', label="Buy Zone (RSI < 30)")
    plt.axhline(70, color='red', linestyle='--', label="Sell Zone (RSI > 70)")
    plt.title("RSI Levels")
    plt.legend()
    plt.grid()
    plt.show()

# Streamlit UI
st.title("Advanced Price Prediction with RSI and Sniper Levels")

uploaded_image = st.file_uploader("Upload a Price Chart Image (JPEG)", type=["jpeg", "jpg"])
rsi_period = st.slider("Select RSI Period", 1, 30, 14)

if uploaded_image is not None:
    image = Image.open(uploaded_image)
    contours, chart_image = process_image(image)

    # Mock price data (replace with actual price data)
    prices = np.linspace(100, 200, num=100)  # Example price data
    rsi = calculate_rsi(prices, period=rsi_period)

    support, resistance, demand_zone, supply_zone, sniper_entry, sniper_exit = predict_levels(contours, rsi)

    st.subheader("Predicted Levels")
    st.write(f"Support Level: {support}")
    st.write(f"Resistance Level: {resistance}")
    st.write(f"Demand Zone: {demand_zone}")
    st.write(f"Supply Zone: {supply_zone}")
    st.write(f"Sniper Entry Point: {sniper_entry}")
    st.write(f"Sniper Exit Point: {sniper_exit}")
    st.write(f"Latest RSI Value: {rsi[-1]:.2f}")

    plot_chart_with_zones(chart_image, support, resistance, demand_zone, supply_zone, sniper_entry, sniper_exit, rsi)
