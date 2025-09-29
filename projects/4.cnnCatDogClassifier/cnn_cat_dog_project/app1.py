import streamlit as st
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
from PIL import Image

# Page config
st.set_page_config(page_title="Cat vs Dog Classifier", page_icon="🐾", layout="centered")

# Title & subtitle
st.markdown("<h1 style='text-align: center;'>🐱🐶 Cat or Dog Classifier</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Upload an image of a <strong>cat</strong> or <strong>dog</strong>, and the model will predict it!</p>", unsafe_allow_html=True)
st.markdown("---")

# Load model
model = load_model('models/cat_dog_cnn_model.h5')

# Upload container
with st.container():
    st.subheader("📤 Upload Image")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        img = Image.open(uploaded_file).convert('RGB')

        col1, col2 = st.columns([1, 1])

        with col1:
            st.image(img, caption='📷 Uploaded Image', use_container_width =True)

        # Preprocess the image
        img_resized = img.resize((150, 150))
        img_array = image.img_to_array(img_resized) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        # Prediction container
        with col2:
            st.markdown("### 🤖 Model Prediction")
            prediction = model.predict(img_array)

            if prediction[0][0] > 0.5:
                st.success("It's a **Dog 🐶**!")
            else:
                st.success("It's a **Cat 🐱**!")

        st.markdown("---")
