# string_case_converter_streamlit.py

import streamlit as st

def count_vowels_consonants(text):
    vowels = "aeiouAEIOU"
    v_count = 0
    c_count = 0

    for ch in text:
        if ch.isalpha():
            if ch in vowels:
                v_count += 1
            else:
                c_count += 1

    return v_count, c_count

# def count_vowels_consonants(text):
#     vowels = "aeiouAEIOU"
#     letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
#     v_count = 0
#     c_count = 0

#     for ch in text:
#         if ch in letters:
#             if ch in vowels:
#                 v_count += 1
#             else:
#                 c_count += 1

#     return v_count, c_count


# Streamlit UI
st.title(" String Case Converter Tool")

sentence = st.text_input("Enter a sentence:")

operation = st.selectbox(
    "Choose an operation:",
    ["None", "UPPER case", "lower case", "Title Case", "Reverse"]
)

if sentence and operation != "None":
    if operation == "UPPER case":
        result = sentence.upper()
    elif operation == "lower case":
        result = sentence.lower()
    elif operation == "Title Case":
        result = sentence.title()
    elif operation == "Reverse":
        result = sentence[::-1]

    st.markdown("###  Converted Sentence:")
    st.write(result)

    vowels, consonants = count_vowels_consonants(result)
    st.markdown("###  Character Count:")
    st.write(f"Vowels: {vowels}, Consonants: {consonants}")
