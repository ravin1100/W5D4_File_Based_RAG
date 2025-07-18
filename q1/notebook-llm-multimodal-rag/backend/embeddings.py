# backend/embeddings.py

"""
This module handles text embedding generation using the Ollama local model via LangChain.
All textual content (summaries, table summaries, image summaries) is converted to embeddings for vector search.
The default model used is 'nomic-embed-text'.
"""

import os
from typing import List
from langchain_ollama import OllamaEmbeddings

# Read Ollama server endpoint from environment variables
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

# Initialize LangChain Ollama embedding model (uses 'nomic-embed-text')
embedding_model = OllamaEmbeddings(
    base_url=OLLAMA_HOST,
    model="nomic-embed-text"
)

def embed_text(content: str) -> List[float]:
    """
    Converts a single string of text into its corresponding embedding vector using Ollama.
    Args:
        content (str): The text/sentence to embed.
    Returns:
        List[float]: The embedding vector as a list of floats.
    """
    # LangChain's embedding model returns [embedding] for a list of docs.
    embedding = embedding_model.embed_documents([content])
    # embedding is a list of lists, for a single input take the first embedding vector
    return embedding[0] if embedding else []

