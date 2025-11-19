# text_splitter_streamlit.py
import streamlit as st

def split_text(text, mode, custom_char=None):
    if mode == "Sentence":
        return text.split(".")
    elif mode == "Word":
        return text.split()
    elif mode == "Custom" and custom_char:
        return text.split(custom_char)
    return [text]

# Streamlit UI
st.title(" Text Splitter Tool")

paragraph = st.text_area("Enter a paragraph:")

mode = st.selectbox("Select delimiter:", ["Sentence", "Word", "Custom"])
custom_char = None
if mode == "Custom":
    custom_char = st.text_input("Enter custom delimiter character:")
splitBtn = st.button("Split")

if splitBtn:
    split_items = split_text(paragraph, mode, custom_char)
    split_items = [item.strip() for item in split_items if item.strip()]
    
    st.markdown(f"### Split Results ({len(split_items)} items):")
    for i, item in enumerate(split_items, 1):
        st.write(f"{i}. {item}")
    
    search_word = st.text_input("Optional: Search for a word in the list")
    searchBtn = st.button("Search")

    if searchBtn:
        found = False
        for item in split_items:
            if search_word.lower() in item.lower():
                found = True
                break        
        st.write(f" '{search_word}' found in list: {found}")
