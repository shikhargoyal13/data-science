import streamlit as st
import tensorflow as tf
import pickle
import numpy as np

# Load TensorFlow models
model_location = 'data/'

encoder_model = tf.keras.models.load_model(model_location + 'models/seq2seq_encoder_eng_hin.h5')
decoder_model = tf.keras.models.load_model(model_location + 'models/seq2seq_decoder_eng_hin.h5')

# Load tokenizers
encoder_t = pickle.load(open(model_location + 'models/encoder_tokenizer_eng', 'rb'))
decoder_t = pickle.load(open(model_location + 'models/decoder_tokenizer_hin', 'rb'))

# Configuration parameters
max_encoder_seq_length = 22
max_decoder_seq_length = 27
int_to_word_decoder = dict((i, c) for c, i in decoder_t.word_index.items())

# Function to generate padded sequences for input string
def encode_input(input_str):
    encoder_seq = encoder_t.texts_to_sequences([input_str])
    encoder_input_data = tf.keras.preprocessing.sequence.pad_sequences(encoder_seq, 
                                                                       maxlen=max_encoder_seq_length,
                                                                       padding='pre')
    return encoder_input_data

# Prediction function
def decode_sentence(input_str):
    input_seq = encode_input(input_str)
    decoder_initial_states_value = encoder_model.predict(input_seq)

    target_seq = np.zeros((1, 1))
    target_seq[0][0] = decoder_t.word_index['<start>']
    stop_loop = False
    predicted_sentence = ''

    while not stop_loop:
        predicted_outputs, h, c = decoder_model.predict([target_seq] + decoder_initial_states_value)
        predicted_output = np.argmax(predicted_outputs[0, -1, :])
        predicted_word = int_to_word_decoder[predicted_output]

        if predicted_word == '<end>' or len(predicted_sentence) > max_decoder_seq_length:
            stop_loop = True
            continue

        if len(predicted_sentence) == 0:
            predicted_sentence = predicted_word
        else:
            predicted_sentence = predicted_sentence + ' ' + predicted_word

        target_seq[0][0] = predicted_output
        decoder_initial_states_value = [h, c]

    return predicted_sentence

# Streamlit UI
st.title("Language Translation App (English to Hindi)")

st.markdown("""
    This app uses a sequence-to-sequence model trained on English and Hindi texts to translate user input.
    Enter a sentence in English, and the model will output the translation in Hindi.
""")

# User input
input_text = st.text_input("Enter an English sentence:", "")

# Translate button
if st.button("Translate"):
    if input_text:
        with st.spinner('Translating...'):
            translated_sentence = decode_sentence(input_text)
        st.success("Translation:")
        st.write(translated_sentence)
    else:
        st.error("Please enter a sentence to translate.")

# Optional: Add some predefined test cases
if st.button("Translate Example Sentences"):
    test_sentences = ["I understand.", "I have a dog.", "I have a car.", "I have a xyz."]
    for sentence in test_sentences:
        st.subheader(f"Input: {sentence}")
        with st.spinner(f'Translating: {sentence}'):
            translated = decode_sentence(sentence)
        st.write(f"Translated: {translated}")
