import streamlit as st
import cv2
import numpy as np
import pytesseract
import matplotlib.pyplot as plt
from PIL import Image

# Function to extract price chart from uploaded image
def process_image(uploaded_image):
    # Convert the image to a numpy array and then to grayscale
    img = cv2.cvtColor(np.array(uploaded_image), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Use edge detection to identify possible chart lines (like support and resistance)
    edges = cv2.Canny(gray, threshold1=30, threshold2=100)
    
    # Find contours to identify price levels or zones
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    return contours, img

# Function to predict support, resistance, demand, and supply
def predict_levels(contours):
    # Example prediction - This would typically involve machine learning models
    # Here we use simplistic logic to define support and resistance based on contours.
    
    # For the sake of this example, we'll just assume that the support is the minimum contour
    # and resistance is the maximum contour based on the image data.
    support = np.min([cv2.boundingRect(c)[1] for c in contours])  # min Y-coordinate (support)
    resistance = np.max([cv2.boundingRect(c)[1] for c in contours])  # max Y-coordinate (resistance)
    
    # Define demand and supply zones based on logic
    demand_zone = support * 0.95  # Arbitrary demand zone (5% below support)
    supply_zone = resistance * 1.05  # Arbitrary supply zone (5% above resistance)
    
    # Sniper Entry & Exit Point Logic
    sniper_entry = demand_zone
    sniper_exit = supply_zone
    
    return support, resistance, demand_zone, supply_zone, sniper_entry, sniper_exit

# Function to plot chart and zones
def plot_chart_with_zones(chart_image, support, resistance, demand_zone, supply_zone, sniper_entry, sniper_exit):
    plt.figure(figsize=(10, 5))
    plt.imshow(chart_image)
    plt.axhline(y=support, color='g', linestyle='--', label='Support Zone')
    plt.axhline(y=resistance, color='r', linestyle='--', label='Resistance Zone')
    plt.axhline(y=demand_zone, color='b', linestyle='--', label='Demand Zone')
    plt.axhline(y=supply_zone, color='orange', linestyle='--', label='Supply Zone')
    plt.axhline(y=sniper_entry, color='purple', linestyle=':', label='Sniper Entry')
    plt.axhline(y=sniper_exit, color='yellow', linestyle=':', label='Sniper Exit')
    plt.title('Price Chart with Support, Resistance, Demand, and Supply Zones')
    plt.legend()
    plt.show()

# Streamlit UI
st.title("AI-Powered Price Prediction with Sniper Entry/Exit Points")

# File upload for the price chart image (JPEG)
uploaded_image = st.file_uploader("Upload a Price Chart Image (JPEG)", type=["jpeg", "jpg"])

if uploaded_image is not None:
    # Process the uploaded image
    image = Image.open(uploaded_image)
    contours, chart_image = process_image(image)
    
    # Predict support, resistance, demand, and supply levels
    support, resistance, demand_zone, supply_zone, sniper_entry, sniper_exit = predict_levels(contours)
    
    # Display the predicted levels and sniper points
    st.subheader(f"Predicted Levels:")
    st.write(f"Support Level: {support}")
    st.write(f"Resistance Level: {resistance}")
    st.write(f"Demand Zone: {demand_zone}")
    st.write(f"Supply Zone: {supply_zone}")
    st.write(f"Sniper Entry Point: {sniper_entry}")
    st.write(f"Sniper Exit Point: {sniper_exit}")
    
    # Display the price chart with zones
    plot_chart_with_zones(chart_image, support, resistance, demand_zone, supply_zone, sniper_entry, sniper_exit)
