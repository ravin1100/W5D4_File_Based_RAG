# backend/query.py

"""
This module processes user search queries:
- Embeds the natural language query via Ollama (nomic-embed-text).
- Queries Chroma Cloud for the most relevant document chunks (across modalities).
- Formats and returns retrieval results to the API.
"""

from schemas import QueryRequest, QueryResponse, DocumentChunk
from embeddings import embed_text
from chroma_db import search_chroma


async def handle_query(request: QueryRequest) -> QueryResponse:
    """
    Processes an incoming QueryRequest:
    1. Embeds the user's question using Ollama.
    2. Uses the embedding to semantically search the Chroma vector database.
    3. Formats the results as a list of DocumentChunk objects.

    Args:
        request (QueryRequest): The user's search input.

    Returns:
        QueryResponse: Contains a list of matching DocumentChunk results.
    """
    # Step 1: Embed the question for semantic search
    query_embedding = embed_text(request.query)

    # Step 2: Retrieve relevant chunks from Chroma Cloud
    matches = search_chroma(query_embedding, top_k=request.top_k)
    # print("=" * 100)
    # print("\n", matches)
    # print("=" * 100)

    # Step 3: Format results as a list of DocumentChunk objects
    chunks = []
    for item in matches:
        # Each 'item' is a dict with 'content' and 'metadata' as per chroma_db.py
        meta = item.get("metadata", {})
        chunks.append(
            DocumentChunk(
                document_id=meta.get("document_id", ""),
                chunk_id=str(meta.get("chunk_index", "")),
                content=item.get("content", ""),
                page_num=meta.get("page_num"),
                metadata=meta,
            )
        )

    print("=" * 100)
    print("\n", chunks)
    print("=" * 100)

    return QueryResponse(results=chunks)
