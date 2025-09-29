# app.py

import streamlit as st
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
from PIL import Image

st.title("🐱🐶 Cat or Dog Classifier")
st.write("Upload an image of a **cat** or a **dog**, and the model will predict it!")

model = load_model('models/cat_dog_cnn_model.h5')

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    img = Image.open(uploaded_file).convert('RGB')
    st.image(img, caption='Uploaded Image', use_column_width=True)

    img = img.resize((150, 150))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    prediction = model.predict(img_array)

    if prediction[0][0] > 0.5:
        st.success("It's a Dog 🐶!")
    else:
        st.success("It's a Cat 🐱!")