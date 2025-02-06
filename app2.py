import streamlit as st
from PIL import Image, UnidentifiedImageError
import pytesseract
import io
import tensorflow as tf
import os
import numpy as np
import cv2
import json

# Set the Tesseract path (make sure this path points to where Tesseract is installed on your machine)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Users\shaik\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'  # Update this path if necessary
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Set the Streamlit page configuration
st.set_page_config(page_title="Revolutionizing Handwritten Prescription Recognition: A High-Accuracy CNN Model with Explainable AI", layout="wide")

# Define Color Variables for better UI consistency
PRIMARY_COLOR = '#4CAF50'  # Green
SECONDARY_COLOR = '#2196F3'  # Blue
ALERT_COLOR = '#F44336'  # Red
BACKGROUND_COLOR = '#f0f8ff'  # Soft light blue background
TEXT_COLOR = '#333'  # Dark text for readability
ACCENT_COLOR = '#00bcd4'  # Teal accent color

st.markdown(f"""
    <style>
        /* General Styling */
        body {{
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(
                120deg,
                #ff9a9e 0%,
                #fad0c4 30%,
                #fbc2eb 60%,
                #a6c1ee 100%
            );
            background-size: 400% 400%;
            animation: gradientAnimation 12s ease infinite;
            color: #ffffff;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            overflow-x: hidden;
        }}

        /* Gradient Animation */
        @keyframes gradientAnimation {{
            0% {{
                background-position: 0% 50%;
            }}
            50% {{
                background-position: 100% 50%;
            }}
            100% {{
                background-position: 0% 50%;
            }}
        }}

        /* Main Container */
        .main-container {{
            background: rgba(20, 20, 30, 0.95);
            border-radius: 20px;
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.6);
            padding: 50px;
            max-width: 1100px;
            width: 90%;
            margin: 20px auto;
            display: flex;
            flex-direction: column;
            align-items: center;
            transform: scale(1);
            transition: all 0.4s ease;
        }}

        .main-container:hover {{
            transform: translateY(-10px);
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.8);
        }}

        /* Header Styling */
        .header {{
            font-size: 3rem;
            font-weight: 800;
            background: linear-gradient(to right, #42a5f5, #e040fb);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 25px;
            text-align: center;
            animation: fadeInDown 1s ease-out;
        }}

        /* Subheader Styling */
        .subheader {{
            font-size: 1.4rem;
            color: #c5c5c5;
            text-align: center;
            margin-bottom: 30px;
            line-height: 1.8;
            animation: fadeInUp 1s ease-out;
        }}

        @keyframes fadeInDown {{
            0% {{
                opacity: 0;
                transform: translateY(-30px);
            }}
            100% {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}

        @keyframes fadeInUp {{
            0% {{
                opacity: 0;
                transform: translateY(30px);
            }}
            100% {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}

        /* File Upload Section */
        .file-upload {{
            background: rgba(40, 40, 60, 0.85);
            padding: 25px;
            border-radius: 15px;
            border: 2px dashed #42a5f5;
            text-align: center;
            cursor: pointer;
            width: 100%;
            max-width: 500px;
            transition: all 0.3s ease;
            animation: pulseEffect 2s infinite;
        }}

        .file-upload:hover {{
            background: rgba(60, 60, 80, 0.95);
            transform: scale(1.05);
            border-color: #1e88e5;
        }}

        @keyframes pulseEffect {{
            0% {{
                box-shadow: 0 0 5px rgba(66, 165, 245, 0.5);
            }}
            50% {{
                box-shadow: 0 0 15px rgba(66, 165, 245, 0.8);
            }}
            100% {{
                box-shadow: 0 0 5px rgba(66, 165, 245, 0.5);
            }}
        }}

        /* Buttons */
        .stButton button {{
            background: linear-gradient(90deg, #42a5f5, #1e88e5);
            color: white;
            font-size: 1.2rem;
            font-weight: bold;
            padding: 15px 35px;
            border: none;
            border-radius: 12px;
            margin: 15px 0;
            cursor: pointer;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
            transition: all 0.4s ease;
        }}

        .stButton button:hover {{
            background: linear-gradient(90deg, #1e88e5, #42a5f5);
            box-shadow: 0 6px 15px rgba(0, 0, 0, 0.6);
            transform: translateY(-5px);
        }}

        .stButton button:active {{
            transform: translateY(2px);
            box-shadow: 0 3px 10px rgba(0, 0, 0, 0.5);
        }}

        /* Graph Section */
        .graph-container {{
            background: rgba(30, 30, 50, 0.9);
            padding: 40px;
            border-radius: 15px;
            margin-top: 30px;
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.5);
            display: flex;
            justify-content: space-around;
            align-items: center;
            width: 100%;
            max-width: 900px;
            animation: slideIn 1.2s ease-out;
        }}

        @keyframes slideIn {{
            0% {{
                opacity: 0;
                transform: translateX(-50px);
            }}
            100% {{
                opacity: 1;
                transform: translateX(0);
            }}
        }}

        .graph {{
            display: flex;
            flex-direction: column;
            align-items: center;
        }}

        .bar {{
            width: 50px;
            height: 150px;
            background: linear-gradient(to top, #42a5f5, #e040fb);
            border-radius: 10px;
            margin: 5px;
            transition: height 0.4s ease, transform 0.4s ease;
            animation: floatEffect 3s infinite;
        }}

        .bar:hover {{
            height: 200px;
            transform: translateY(-15px);
        }}

        @keyframes floatEffect {{
            0%, 100% {{
                transform: translateY(0);
            }}
            50% {{
                transform: translateY(-10px);
            }}
        }}

        .bar-label {{
            margin-top: 10px;
            font-size: 1rem;
            color: #c5c5c5;
        }}

        /* Footer Section */
        .footer {{
            background: rgba(20, 20, 30, 0.95);
            padding: 20px;
            margin-top: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
            text-align: center;
        }}

        .footer-content {{
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }}

        .footer-icons {{
            display: flex;
            justify-content: center;
            align-items: center;
            margin-top: 10px;
            gap: 20px;
        }}

        .footer-icons img {{
            width: 40px;
            height: 40px;
            transition: all 0.3s ease;
            cursor: pointer;
        }}

        .footer-icons img:hover {{
            transform: scale(1.1);
            filter: drop-shadow(0 0 5px #42a5f5);
        }}

        .footer-text {{
            font-size: 0.9rem;
            color: #cccccc;
            margin-top: 10px;
        }}

        .footer-text a {{
            color: #42a5f5;
            text-decoration: none;
            font-weight: bold;
        }}

        .footer-text a:hover {{
            color: #e040fb;
        }}
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="header">Revolutionizing Handwritten Prescription Recognition: A High-Accuracy CNN Model with Explainable AI</h1>', unsafe_allow_html=True)

# Load the pre-trained model
@st.cache_resource
def load_model():
    return tf.keras.models.load_model("model_saved.keras")

model = load_model()

# Function to preprocess the image for the model
def preprocess_image(image, target_size=(28, 28)):
    try:
        # Convert to grayscale if not already
        if image.mode != "L":
            image = image.convert("L")  # Convert to grayscale
        
        # Resize to target size
        image = image.resize(target_size)
        
        # Convert to numpy array
        image = np.array(image, dtype=np.float32)
        
        # Normalize pixel values
        image = image / 255.0
        
        # Add batch and channel dimensions
        image = np.expand_dims(image, axis=-1)  # Add channel dimension
        image = np.expand_dims(image, axis=0)   # Add batch dimension
        
        return image
    except Exception as e:
        st.error(f"Error in preprocessing the image: {str(e)}")
        return None

# Function to enhance image for OCR
def enhance_for_ocr(image, grayscale=False):
    try:
        # Convert PIL Image to OpenCV format
        image = np.array(image)

        # Ensure grayscale for adaptive thresholding
        if len(image.shape) == 3 and image.shape[2] == 3:  # Check if the image is RGB
            image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

        # Apply Gaussian Blur for noise reduction
        image = cv2.GaussianBlur(image, (5, 5), 0)

        # Apply adaptive thresholding to improve contrast
        image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

        # Optional: Resize for better OCR performance
        height, width = image.shape[:2]
        image = cv2.resize(image, (width * 2, height * 2), interpolation=cv2.INTER_LINEAR)

        # Convert back to PIL Image
        enhanced_image = Image.fromarray(image)

        # If the user wants grayscale OCR, return as is; otherwise, convert back to original format
        if not grayscale:
            # Convert the image back to RGB
            enhanced_image = enhanced_image.convert("RGB")

        return enhanced_image
    except Exception as e:
        st.error(f"Error in enhancing the image for OCR: {str(e)}")
        return None

# Function to extract text using OCR with confidence evaluation
def extract_text(image, grayscale=False):
    try:
        # Enhance the image for OCR
        enhanced_image = enhance_for_ocr(image, grayscale=grayscale)
        if not enhanced_image:
            return None, 0  # No text and zero confidence

        # Extract text data with confidence
        custom_config = r'--oem 3 --psm 6'  # Optimal settings for mixed text and graphics
        data = pytesseract.image_to_data(enhanced_image, config=custom_config, output_type=pytesseract.Output.DICT)

        # Combine detected text and calculate average confidence
        text = " ".join([data['text'][i] for i in range(len(data['text'])) if int(data['conf'][i]) > 0])
        confidences = [int(data['conf'][i]) for i in range(len(data['conf'])) if int(data['conf'][i]) > 0]
        average_confidence = np.mean(confidences) if confidences else 0

        return text.strip(), average_confidence
    except Exception as e:
        st.error(f"Error during text extraction: {str(e)}")
        return None, 0

# Sidebar for preprocessing options
st.sidebar.header("Preprocessing Options")
grayscale = st.sidebar.checkbox("Convert to Grayscale before OCR", value=False)

# Toggle camera feature
st.sidebar.header("Camera Control")
if "camera_on" not in st.session_state:
    st.session_state["camera_on"] = False

if st.sidebar.button("Turn Camera ON"):
    st.session_state["camera_on"] = True
if st.sidebar.button("Turn Camera OFF"):
    st.session_state["camera_on"] = False

# Layout for camera and file uploader
with st.container():
    st.markdown('<div class="main-container">', unsafe_allow_html=True)

    # Camera Input Section
    captured_image = None
    if st.session_state["camera_on"]:
        captured_image = st.camera_input("Capture Image")
        if captured_image:
            st.image(captured_image, caption="Captured Image", use_container_width=True)

    # File Upload Section
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    image = None

    # Check file size (limit to 5MB)
    if uploaded_file:
        if uploaded_file.size > 5 * 1024 * 1024:
            st.error("The uploaded file exceeds the 5MB size limit. Please upload a smaller file.")
            uploaded_file = None
        else:
            try:
                img_bytes = uploaded_file.read()
                image = Image.open(io.BytesIO(img_bytes))  # Open using PIL
                st.image(image, caption=f"Uploaded Image: {uploaded_file.name}", use_container_width=True)
            except UnidentifiedImageError:
                st.error("The uploaded file is not a valid image. Please upload a valid image file (jpg, jpeg, png).")


    # Model Prediction and OCR
    if st.button("Start Prediction and Text Extraction"):
        if uploaded_file or captured_image:
            with st.spinner("Processing the image... Please wait."):
                try:
                    # Use captured image or uploaded file
                    if captured_image:
                        img_bytes = captured_image.getvalue()  # Convert camera input to bytes
                        image = Image.open(io.BytesIO(img_bytes))

                    if image:
                        # **Step 1: Preprocess image for model**
                        processed_image = preprocess_image(image)
                        
                        # Make prediction using the model
                        if processed_image is not None:
                            prediction = model.predict(processed_image)
                            predicted_class = np.argmax(prediction)
                            classification_confidence = np.max(prediction) * 100

                            # Display classification results
                            st.subheader("Model Prediction:")
                            st.write(f"Predicted Class: {predicted_class}")
                            st.write(f"Confidence: {classification_confidence:.2f}%")
                        else:
                            st.error("Failed to preprocess the image for model prediction.")

                        # **Step 2: Extract text using OCR**
                        extracted_text, ocr_confidence = extract_text(image, grayscale=grayscale)

                        if ocr_confidence < 20:
                            st.write("No Text Found")
                        else:
                            st.subheader("Extracted Text:")
                            st.text_area("", extracted_text, height=200,label_visibility="hidden")

                            # **Download Buttons for OCR text**
                            st.download_button(
                                label="Download Extracted Text",
                                data=extracted_text,
                                file_name="extracted_text.txt",
                                mime="text/plain"
                            )
                    else:
                        st.warning("No valid image found for processing.")
                except Exception as e:
                    st.error(f"An unexpected error occurred: {str(e)}")
        else:
            st.info("Please upload or capture an image for prediction and text extraction.")

    # Clear Session State
    if st.button("Clear Data"):
        st.session_state["camera_on"] = False
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)


