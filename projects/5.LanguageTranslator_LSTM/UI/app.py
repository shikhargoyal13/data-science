import streamlit as st
import tensorflow as tf
import pickle
import numpy as np

# Must be the first Streamlit command in the script
st.set_page_config(page_title="Language Translator", layout="centered")

# -------------------
# Model and Tokenizer Loading
# -------------------
@st.cache_resource
def load_models_and_tokenizers():
    model_location = 'data/'  # Update as required

    # Load models
    encoder_model = tf.keras.models.load_model(model_location + 'models/seq2seq_encoder_eng_hin.h5')
    decoder_model = tf.keras.models.load_model(model_location + 'models/seq2seq_decoder_eng_hin.h5')

    # Load tokenizers
    encoder_t = pickle.load(open(model_location + 'models/encoder_tokenizer_eng', 'rb'))
    decoder_t = pickle.load(open(model_location + 'models/decoder_tokenizer_hin', 'rb'))

    # Configuration parameters from training
    max_encoder_seq_length = 22
    max_decoder_seq_length = 27

    # Build a dictionary: key is word index, value is actual word.
    int_to_word_decoder = {i: c for c, i in decoder_t.word_index.items()}

    models = {
        "encoder_model": encoder_model,
        "decoder_model": decoder_model,
        "encoder_t": encoder_t,
        "decoder_t": decoder_t,
        "int_to_word_decoder": int_to_word_decoder,
        "max_encoder_seq_length": max_encoder_seq_length,
        "max_decoder_seq_length": max_decoder_seq_length
    }
    return models

# Load models once at startup
models = load_models_and_tokenizers()

# -------------------
# Helper Functions
# -------------------
def encode_input(input_str, encoder_t, max_encoder_seq_length):
    # Convert words to indexes and pad the sequence.
    encoder_seq = encoder_t.texts_to_sequences([input_str])
    encoder_input_data = tf.keras.preprocessing.sequence.pad_sequences(
        encoder_seq, maxlen=max_encoder_seq_length, padding='pre'
    )
    return encoder_input_data

def decode_sentence(input_str):
    encoder_model = models["encoder_model"]
    decoder_model = models["decoder_model"]
    encoder_t = models["encoder_t"]
    decoder_t = models["decoder_t"]
    int_to_word_decoder = models["int_to_word_decoder"]
    max_encoder_seq_length = models["max_encoder_seq_length"]
    max_decoder_seq_length = models["max_decoder_seq_length"]
    
    # Encode the input string
    input_seq = encode_input(input_str, encoder_t, max_encoder_seq_length)
    # Get the encoder state values
    decoder_initial_states_value = encoder_model.predict(input_seq)

    # Build the initial decoder sequence with the <start> token.
    target_seq = np.zeros((1, 1))
    target_seq[0, 0] = decoder_t.word_index['<start>']

    stop_loop = False
    predicted_sentence = ""

    while not stop_loop:
        predicted_outputs, h, c = decoder_model.predict([target_seq] + decoder_initial_states_value)
        # Select the token with highest probability
        predicted_output = np.argmax(predicted_outputs[0, -1, :])
        predicted_word = int_to_word_decoder.get(predicted_output, '')

        # Stop if end token is reached or max length exceeded.
        if predicted_word == '<end>' or len(predicted_sentence.split()) >= max_decoder_seq_length:
            stop_loop = True
        else:
            # Update predicted sentence
            predicted_sentence = predicted_sentence + (" " if predicted_sentence else "") + predicted_word
            # Update the target sequence with the predicted word
            target_seq[0, 0] = predicted_output
            # Update the decoder states with the latest state values
            decoder_initial_states_value = [h, c]

    return predicted_sentence.strip()

# -------------------
# Streamlit UI Layout
# -------------------

# Header Section
st.title("English to Hindi Translator")
st.markdown("Translate English sentences to Hindi using a sequence-to-sequence deep learning model.")

# Input Section
st.subheader("Enter an English Sentence")
input_text = st.text_area("Your Input", value="I have a dog.", height=100)

# Button to trigger translation
if st.button("Translate"):
    if input_text.strip():
        with st.spinner("Translating..."):
            result = decode_sentence(input_text.strip())
        st.success("Translation Complete!")
        st.markdown("### Hindi Translation")
        st.write(result)
    else:
        st.warning("Please enter a sentence to translate.")

# Footer / Additional Information
st.markdown("---")
st.markdown("Built with TensorFlow and Streamlit.")
