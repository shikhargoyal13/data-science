import streamlit as st
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
from PIL import Image

# Configure the page
st.set_page_config(
    page_title="Cat vs Dog Classifier",
    page_icon="🐾",
    layout="centered",
)

# Custom CSS for card-style layout
st.markdown("""
    <style>
    .card {
        background-color: #ffffff;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin-top: 2rem;
    }
    .title {
        text-align: center;
        font-size: 2.5rem;
        font-weight: 700;
        color: #3c3c3c;
    }
    .subtitle {
        text-align: center;
        font-size: 1.1rem;
        color: #555;
        margin-bottom: 2rem;
    }
    .result-box {
        font-size: 1.5rem;
        text-align: center;
        padding: 1rem;
        border-radius: 10px;
        margin-top: 1.5rem;
    }
    .cat { background-color: #ffe4e1; color: #c0392b; }
    .dog { background-color: #e0f7fa; color: #00796b; }
    </style>
""", unsafe_allow_html=True)

# Title Section
st.markdown("<div class='title'>🐱🐶 Cat vs Dog Classifier</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Upload an image, and our trained deep learning model will tell you if it's a cat or a dog.</div>", unsafe_allow_html=True)

# Load Model
model = load_model('models/cat_dog_cnn_model.h5')

# Upload Section
with st.container():
    uploaded_file = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        with st.spinner("Processing image..."):
            img = Image.open(uploaded_file).convert('RGB')
            img_resized = img.resize((150, 150))
            img_array = image.img_to_array(img_resized) / 255.0
            img_array = np.expand_dims(img_array, axis=0)

            prediction = model.predict(img_array)[0][0]
            label = "Dog 🐶" if prediction > 0.5 else "Cat 🐱"
            confidence = prediction if prediction > 0.5 else 1 - prediction
            class_style = "dog" if prediction > 0.5 else "cat"

        # Result card
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1])
        with col1:
            st.image(img, caption="Uploaded Image", use_column_width=280)

        with col2:
            st.markdown(f"<div class='result-box {class_style}'><strong>Prediction:</strong> {label}<br><strong>Confidence:</strong> {confidence*100:.2f}%</div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)
