# backend/utils.py

"""
This file contains utility functions for common backend tasks:
- File/folder management for uploads and temp storage
- Generating unique IDs and timestamps
- Miscellaneous helpers reusable throughout the backend

You can extend this file with more utilities as your project grows.
"""

import os
from datetime import datetime
import uuid

UPLOAD_DIR = "uploaded_data"


def ensure_upload_dir():
    """
    Ensures the upload directory exists.
    """
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)


def get_unique_filename(original_filename: str) -> str:
    """
    Generates a unique filename by prepending a timestamp and a UUID to the original filename.
    Args:
        original_filename (str): The filename provided by the user.
    Returns:
        str: A filename guaranteed to be unique in the uploads folder.
    """
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    unique_part = str(uuid.uuid4())[:8]
    return f"{timestamp}_{unique_part}_{original_filename}"


def save_upload_file(file_obj, destination_path: str) -> None:
    """
    Saves the contents of an UploadFile (from FastAPI) or file-like object to disk.
    Args:
        file_obj: The file object from FastAPI UploadFile.
        destination_path (str): Where to save the file.
    """
    with open(destination_path, "wb") as dest:
        content = file_obj.file.read() if hasattr(file_obj, "file") else file_obj.read()
        dest.write(content)


def read_file_bytes(file_path: str) -> bytes:
    """
    Reads and returns the contents of a file as bytes.
    Args:
        file_path (str): Path to the file.
    Returns:
        bytes: Contents of the file.
    """
    with open(file_path, "rb") as f:
        return f.read()


def strip_text(text: str) -> str:
    """
    Strips leading/trailing whitespace and normalizes line endings in text inputs.
    Args:
        text (str): The text to clean.
    Returns:
        str: Cleaned text.
    """
    return text.strip().replace('\r\n', '\n').replace('\r', '\n')


# Add more general-purpose helpers here as needed!
