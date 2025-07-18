# frontend/utils.py

"""
Utility functions for the Streamlit frontend:
- Facilitates calls to backend endpoints for document upload, querying, and (in the future) browsing.
- Modular design lets you easily expand with more API helpers later.
- All functions are commented for easy understanding as you build your MVP.
"""

import requests
import streamlit as st

# Define the base URL for your FastAPI backend
BACKEND_URL = "http://localhost:8000"  # Update if you deploy with a different host/port

def upload_document_api(file):
    """
    Uploads a document to the backend for ingestion and indexing.
    Args:
        file: The file-like object returned by Streamlit's file_uploader.
    Returns:
        dict: Response with status, message, document_id (if successful).
    """
    try:
        files = {"file": (file.name, file, file.type)}
        response = requests.post(f"{BACKEND_URL}/ingest", files=files)
        return response.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}

def fetch_documents_api():
    """
    Fetches a list of available documents from the backend.
    NOTE: This is currently a stub. Replace with actual API call if you implement such an endpoint in your backend.
    Returns:
        list: List of document summaries or IDs.
    """
    # Backend API support is not implemented by default; for now, return empty list
    return []

def query_documents_api(query_text):
    """
    Sends a user's question to the backend for semantic search and retrieval.
    Args:
        query_text (str): The user's input query.
    Returns:
        dict: Response from backend, should include list of matching results.
    """
    try:
        payload = {"query": query_text, "top_k": 5}
        response = requests.post(f"{BACKEND_URL}/query", json=payload)
        return response.json()
    except Exception as e:
        return {"results": [], "error": str(e)}

# You can add more utility functions here for future features such as authentication,
# session state management, file deletion, or advanced filtering.
