# frontend/app.py

"""
This file is the main entrypoint for your Streamlit frontend.
It:
  - Provides navigation for document upload, browsing, and chat-based querying.
  - Ties together all UI and backend API communication (handled in components.py and utils.py).
  - Uses session state for user experience consistency across page navigation.
"""

import streamlit as st
from components import show_upload_ui, show_browser_ui, show_chat_ui

# Set the Streamlit app title and layout
st.set_page_config(
    page_title="Notebook LLM Multimodal RAG",
    layout="wide"
)

# Sidebar navigation
st.sidebar.title("Multimodal Research Assistant")
selection = st.sidebar.radio(
    "Go to:",
    options=["Upload Document", "Browse Documents", "Chat/Query"]
)

# Simple session state to track UI context (optional, for advanced navigation)
if "last_page" not in st.session_state:
    st.session_state["last_page"] = selection

# Render the page based on user navigation
if selection == "Upload Document":
    show_upload_ui()
    st.session_state["last_page"] = "Upload Document"

elif selection == "Browse Documents":
    show_browser_ui()
    st.session_state["last_page"] = "Browse Documents"

elif selection == "Chat/Query":
    show_chat_ui()
    st.session_state["last_page"] = "Chat/Query"

# (Optional) You can add more sections or customize the sidebar as your UI grows.

