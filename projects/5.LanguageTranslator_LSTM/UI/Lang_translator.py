import streamlit as st
import tensorflow as tf
import numpy as np
import pickle

# ----------- Configuration -----------
MODEL_PATH = 'models/'

max_encoder_seq_length = 22
max_decoder_seq_length = 27

# ----------- Caching models and tokenizers for performance -----------

@st.cache_resource(show_spinner=True)
def load_models_and_tokenizers():
    encoder_model = tf.keras.models.load_model(MODEL_PATH + 'seq2seq_encoder_eng_hin.h5')
    decoder_model = tf.keras.models.load_model(MODEL_PATH + 'seq2seq_decoder_eng_hin.h5')
    encoder_t = pickle.load(open(MODEL_PATH + 'encoder_tokenizer_eng', 'rb'))
    decoder_t = pickle.load(open(MODEL_PATH + 'decoder_tokenizer_hin', 'rb'))

    # Reverse dictionary for decoder
    int_to_word_decoder = {i: w for w, i in decoder_t.word_index.items()}
    return encoder_model, decoder_model, encoder_t, decoder_t, int_to_word_decoder

encoder_model, decoder_model, encoder_t, decoder_t, int_to_word_decoder = load_models_and_tokenizers()

# ----------- Functions -----------

def encode_input(input_str):
    encoder_seq = encoder_t.texts_to_sequences([input_str])
    encoder_input_data = tf.keras.preprocessing.sequence.pad_sequences(
        encoder_seq, maxlen=max_encoder_seq_length, padding='post')
    return encoder_input_data

def decode_sentence(input_str):
    input_seq = encode_input(input_str)
    decoder_initial_states_value = encoder_model.predict(input_seq)
    
    target_seq = np.zeros((1,1))
    target_seq[0,0] = decoder_t.word_index['<start>']

    stop_loop = False
    predicted_sentence = ''

    while not stop_loop:
        predicted_outputs, h, c = decoder_model.predict([target_seq] + decoder_initial_states_value)

        predicted_output = np.argmax(predicted_outputs[0, -1, :])
        predicted_word = int_to_word_decoder.get(predicted_output, '')

        if predicted_word == '<end>' or len(predicted_sentence.split()) > max_decoder_seq_length:
            stop_loop = True
            continue

        predicted_sentence = (predicted_sentence + ' ' + predicted_word).strip()
        target_seq[0,0] = predicted_output
        decoder_initial_states_value = [h,c]

    return predicted_sentence

# ----------- Streamlit UI -----------

st.set_page_config(page_title="English to Hindi Seq2Seq Translator", layout="centered")

st.title("English to Hindi Translator using Seq2Seq Model")
st.markdown(
    """
    This app translates English sentences to Hindi using a trained Seq2Seq model.
    Enter an English sentence below and hit **Translate**.
    """
)

# User input
input_text = st.text_area("Enter English sentence:", height=120)

if st.button("Translate"):
    if not input_text.strip():
        st.error("Please enter a valid sentence.")
    else:
        with st.spinner("Translating..."):
            try:
                translation = decode_sentence(input_text.strip())
                if translation:
                    st.success("Translation:")
                    st.write(f"**{translation}**")
                else:
                    st.warning("Could not generate a translation. Please try a different sentence.")
            except Exception as e:
                st.error(f"An error occurred during translation: {e}")

# Optional: Show model summary if expanded
with st.expander("Show Encoder Model Summary"):
    st.text(encoder_model.summary())

with st.expander("Show Decoder Model Summary"):
    st.text(decoder_model.summary())

st.markdown("---")
st.caption("Built with TensorFlow and Streamlit. Models and tokenizers loaded from Google Drive.")

