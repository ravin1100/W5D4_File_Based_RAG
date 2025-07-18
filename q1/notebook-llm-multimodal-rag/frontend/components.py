# frontend/components.py

"""
This module defines all Streamlit UI components and logic.
- Contains separate functions for document upload, browsing, and chat/query UI.
- Handles communication with backend API endpoints (see utils.py).
- Thoroughly commented for clarity.
"""

import streamlit as st
from utils import upload_document_api, fetch_documents_api, query_documents_api

def show_upload_ui():
    """
    Renders the document upload interface.
    - Lets user select and upload a file.
    - Shows upload progress and backend feedback.
    """
    st.header("Upload Document")
    uploaded_file = st.file_uploader(
        "Select a file to upload (PDF, DOCX, CSV, PPTX, etc.)",
        type=["pdf", "docx", "csv", "pptx", "xlsx", "html", "jpg", "png"]
    )
    if uploaded_file is not None:
        if st.button("Ingest Document"):
            with st.spinner("Uploading and processing..."):
                response = upload_document_api(uploaded_file)
            if response.get("status") == "success":
                st.success(f"Document uploaded and indexed! Doc ID: {response.get('document_id')}")
            else:
                st.error(f"Error: {response.get('message')}")
    st.write("---")

def show_browser_ui():
    """
    Renders a document browser.
    - Fetches list of uploaded documents from backend.
    - Displays simple document table for browsing (extend as needed!).
    """
    st.header("Browse Uploaded Documents")
    docs = fetch_documents_api()
    if docs:
        st.table(docs)
    else:
        st.info("No documents uploaded yet.")
    st.write("---")

def show_chat_ui():
    """
    Renders the chat/query interface for semantic document search.
    - User can input natural language questions.
    - Displays retrieved chunks/results from the backend in a human-friendly way.
    """
    st.header("Ask a Question")
    user_query = st.text_input("Enter your question or query here and press Enter")
    if st.button("Search") and user_query.strip():
        with st.spinner("Searching documents..."):
            results = query_documents_api(user_query)
        if results and "results" in results and results["results"]:
            for idx, chunk in enumerate(results["results"], 1):
                st.markdown(f"### Result {idx}")
                # Show the content text as normal markdown
                st.markdown(f"**Excerpt:**<br>{chunk['content']}", unsafe_allow_html=True)
                # Display selected metadata in a key-value table
                meta = chunk.get("metadata", {})
                visible_keys = ['filename', 'modality', 'chunk_index', 'page_no']
                if any(key in meta for key in visible_keys):
                    st.markdown("**Document Info:**")
                    info = {k: v for k, v in meta.items() if k in visible_keys and v is not None}
                    # Build a table
                    if info:
                        st.table([info])
                st.markdown("---")
        else:
            st.warning("No relevant results found for your query.")
    st.write("---")
