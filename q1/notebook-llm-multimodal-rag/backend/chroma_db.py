# backend/chroma_db.py

"""
This module wraps all interactions with the Chroma Cloud vector database service.
It handles:
    - Creating/updating collections for documents and their embeddings.
    - Bulk upserting of data chunks (text/table/image) with embeddings and metadata.
    - Querying for retrieval augmentation (semantic search).
Environment variables configure connection parameters.
"""

import os
from typing import List, Dict, Any
import chromadb
from chromadb.config import Settings
import json

# Chroma Cloud configuration is set via environment variables from .env
CHROMA_DB_API_KEY = os.getenv("CHROMA_DB_API_KEY")
CHROMA_DB_TENANT_ID = os.getenv("CHROMA_DB_TENANT_ID")
CHROMA_DB_DATABASE_ID = os.getenv("CHROMA_DB_DATABASE_ID")

# Single unified collection for all document chunks (cross-modality)
COLLECTION_NAME = "Notebook_LLM"


def get_chroma_client():
    """
    Instantiate the Chroma client with cloud endpoint and credentials.
    Returns:
        chromadb.Client: Authenticated Chroma Cloud client object.
    """

    client = chromadb.CloudClient(
        api_key=os.getenv("CHROMA_DB_API_KEY"),
        tenant=os.getenv("CHROMA_DB_TENANT_ID"),
        database=os.getenv("CHROMA_DB_DATABASE_ID"),
    )
    return client


def flatten_metadata(md: dict) -> dict:
    """
    Ensures all metadata values are primitive types. 
    If a value is a list/dict, it is converted to a JSON string.
    """
    new_md = {}
    for k, v in md.items():
        if isinstance(v, (str, int, float, bool)) or v is None:
            new_md[k] = v
        else:
            new_md[k] = json.dumps(v)
    return new_md

def index_to_chroma(document_name: str, chunks: list) -> str:
    """
    Stores a list of chunks (text/table/image) from an uploaded document into the Chroma Cloud vector database.

    Args:
        document_name (str): The name of the ingested document.
        chunks (List[dict]): List of dicts with keys:
            - content: The summary or extracted content
            - embedding: The embedding vector (list of floats)
            - modality: The chunk type ('text', 'table', 'image', etc.)
            - metadata: (optional) Additional info

    Returns:
        str: The unique document_id assigned (for downstream reference)
    """
    import uuid
    client = get_chroma_client()
    collection = client.get_or_create_collection(COLLECTION_NAME)
    document_id = str(uuid.uuid4())

    ids, embeddings, metadatas, documents = [], [], [], []

    for idx, chunk in enumerate(chunks):
        # --- Only keep the required metadata fields ---
        base_metadata = chunk.get("metadata") or {}
        filtered_metadata = {
            "filename": document_name,
            "document_id": document_id,
            "chunk_index": idx,
            "modality": chunk.get("modality", "text"),
            "page_no": base_metadata.get("page_no")  # Will be None if not present
        }
        # Flatten filtered metadata (convert any lists/dicts to strings)
        flat_metadata = flatten_metadata(filtered_metadata)

        ids.append(f"{document_id}_{idx}")
        embeddings.append(chunk["embedding"])
        metadatas.append(flat_metadata)
        documents.append(chunk["content"])

    collection.upsert(
        ids=ids,
        embeddings=embeddings,
        metadatas=metadatas,
        documents=documents,
    )
    return document_id



def search_chroma(query_embedding: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
    """
    Performs a semantic search against Chroma using an embedding vector query.

    Args:
        query_embedding (List[float]): The vector embedding of the query.
        top_k (int): How many results to retrieve.

    Returns:
        List[dict]: List of retrieved chunks/documents (with content and metadata).
    """
    client = get_chroma_client()
    collection = client.get_collection(COLLECTION_NAME)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
    )
    # print(results)
    results_list = []
    for match, meta in zip(results["documents"][0], results["metadatas"][0]):
        entry = {"content": match, "metadata": meta}
        results_list.append(entry)

    return results_list
