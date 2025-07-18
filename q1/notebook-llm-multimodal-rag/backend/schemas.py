# backend/schemas.py

"""
This file defines data models for validating and structuring the requests and responses
used in the FastAPI backend. Pydantic BaseModel is used for type enforcement and 
automatic OpenAPI documentation generation.

You'll extend these as your functionality grows.
"""

from pydantic import BaseModel
from typing import List, Optional, Any

class DocumentIngestRequest(BaseModel):
    """
    (Optional – for advanced ingestion)
    Use if you want to have JSON-based (not file-based) upload in addition to file:
      - filename: Name of uploaded document
      - content: Raw document text/content as a string (optional)
    """
    filename: str
    content: Optional[str] = None

class QueryRequest(BaseModel):
    """
    The schema for incoming search/query requests from the user.
    - query: The user’s text query ("What are the key risks in ...?")
    - top_k: How many relevant results to return (default=5)
    """
    query: str
    top_k: int = 5

class DocumentChunk(BaseModel):
    """
    Represents a snippet/chunk of content retrieved from the database.
    Used in QueryResponse for retrieval augmentation.
    """
    document_id: str
    chunk_id: Optional[str] = None
    content: str
    page_num: Optional[int] = None
    metadata: Optional[dict] = None

class QueryResponse(BaseModel):
    """
    What the backend returns to the frontend after a query.
    - results: List of DocumentChunk objects or text chunks.
    - You can modify/add fields later as you refine your UI and features.
    """
    results: List[DocumentChunk]

class IngestResponse(BaseModel):
    """
    What the backend returns to confirm success (or not) after ingesting a document.
    - status: 'success' or 'error'
    - message: Details (useful for frontend feedback)
    - document_id: ID assigned to the uploaded document (if any)
    """
    status: str
    message: str
    document_id: Optional[str] = None
