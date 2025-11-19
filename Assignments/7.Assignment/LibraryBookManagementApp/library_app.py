import streamlit as st
from book_library import Book, Library

if 'library' not in st.session_state:
    st.session_state.library = Library()

st.title("Library Book Management")

tab1, tab2, tab3 = st.tabs(["Add Book", "Issue/Return", "Status"])

with tab1:
    st.subheader("Add a New Book")
    title = st.text_input("Book Title", key="add_title")
    author = st.text_input("Author", key="add_author")
    if st.button("Add Book"):
        if title and author:
            st.session_state.library.add_book(title, author)
            st.success(f"Added '{title}' by {author}")
        else:
            st.error("Please enter both title and author.")

with tab2:
    st.subheader("Issue or Return a Book")

    with st.form("issue_form"):
        title_to_issue = st.text_input("Title to Issue")
        borrower = st.text_input("Borrower's Name")
        if st.form_submit_button("Issue Book"):
            if st.session_state.library.issue_book(title_to_issue, borrower):
                st.success(f"Issued '{title_to_issue}' to {borrower}")
            else:
                st.error("Book is either not available or already issued.")

    with st.form("return_form"):
        title_to_return = st.text_input("Title to Return")
        if st.form_submit_button("Return Book"):
            if st.session_state.library.return_book(title_to_return):
                st.success(f"Returned '{title_to_return}' successfully.")
            else:
                st.error("Book was not issued or not found.")

with tab3:
    st.subheader("Library Status")
    stats = st.session_state.library.get_stats()
    st.metric("Total Books", stats["Total Books"])
    st.metric("Issued Books", stats["Issued Books"])
    st.metric("Available Books", stats["Available Books"])

    st.write("### Book Details")
    for status in st.session_state.library.get_status():
        st.write("- " + status)