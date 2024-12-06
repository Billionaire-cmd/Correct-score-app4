import streamlit as st
import cv2
import numpy as np
import pytesseract
from PIL import Image
import matplotlib.pyplot as plt

# Set Tesseract path for Windows (adjust if needed for Linux or macOS)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Windows example

# Function to read and preprocess the image
def preprocess_image(uploaded_image):
    # Convert uploaded image to OpenCV format
    img = np.array(uploaded_image)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)  # Convert to BGR format
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    return img, gray

# Function to perform text extraction from the image (using pytesseract)
def extract_text_from_image(gray_img):
    # Use pytesseract to extract text
    extracted_text = pytesseract.image_to_string(gray_img)
    return extracted_text

# Function to simulate support/resistance and demand/supply analysis
def analyze_trading_levels(gray_img):
    # Example: Perform edge detection to simulate support/resistance detection
    edges = cv2.Canny(gray_img, 100, 200)
    return edges

# Function to plot the analysis result (edges from Canny detection)
def plot_analysis(img, analysis_result):
    # Create a plot with two subplots: original image and analysis result
    fig, ax = plt.subplots(1, 2, figsize=(12, 6))
    
    # Original image
    ax[0].imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    ax[0].set_title("Uploaded Image")
    ax[0].axis("off")

    # Analysis result (edges)
    ax[1].imshow(analysis_result, cmap='gray')
    ax[1].set_title("Analysis Result (Support/Resistance)")
    ax[1].axis("off")
    
    st.pyplot(fig)

# Streamlit GUI setup
st.title("Trading Image Analysis: Support/Resistance, Demand/Supply")

# Image upload
uploaded_file = st.file_uploader("Upload an Image for Analysis", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Load the image
    img = Image.open(uploaded_file)
    
    # Preprocess image
    img_array, gray_img = preprocess_image(img)
    
    # Text extraction
    extracted_text = extract_text_from_image(gray_img)
    st.subheader("Extracted Text from Image")
    st.write(extracted_text)
    
    # Perform analysis for support/resistance, demand/supply (simulated here)
    analysis_result = analyze_trading_levels(gray_img)
    
    # Display the analysis
    st.subheader("Analysis Results")
    plot_analysis(img_array, analysis_result)
    
    # Optionally, add custom logic for snipers entry/exit based on your own strategy here
    st.write("Sniper Entry/Exit positions could be determined from the analysis.")
