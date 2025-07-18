# backend/ingest.py

"""
This file provides the main logic for handling document uploads:
- It saves uploaded files to the designated 'uploaded_data/' directory.
- Calls parsers (via Docling/LangchainDocling) to extract text, images, tables, etc.
- Passes each modality to its embedding/summarization pipeline.
- Indexes the processed results into the vector database (Chroma).
- Returns a response to confirm success/failure.
"""

import os
from fastapi import UploadFile
from datetime import datetime
from parsing import parse_document  # You'll implement this to call Docling
from summarization import summarize_table, summarize_image, summarize_text
from embeddings import embed_text
from chroma_db import index_to_chroma
from schemas import IngestResponse

# Directory where uploaded documents are stored
UPLOAD_DIR = "uploaded_data"

async def handle_ingest(file: UploadFile):
    """
    Handles a document upload:
    1. Saves the file to disk.
    2. Parses the document into different modalities.
    3. Runs each modality through its processing pipeline (summarization/embedding).
    4. Indexes all chunks to ChromaDB.
    5. Returns a confirmation response.
    
    Args:
        file (UploadFile): The uploaded file from the client.

    Returns:
        dict: IngestResponse fields (status, message, document_id).
    """
    # Step 1: Save the file in the uploads directory
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
    filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    
    # Step 2: Parse document (extract text, images, tables, etc.)
    try:
        parsed = parse_document(file_path)
        # Example output: {'text_chunks': [...], 'images': [...], 'tables': [...]}
    except Exception as e:
        return IngestResponse(
            status="error",
            message=f"Failed to parse document: {str(e)}",
            document_id=None,
        )
    
    # Step 3: Summarize/extract/prepare each modality
    all_chunks = []
    # --- Text chunks ---
    for chunk in parsed.get("text_chunks", []):
        # Optionally run summarization if chunk is very long
        summary = summarize_text(chunk['content'])
        embedding = embed_text(summary)
        chunk_obj = {
            "content": summary,
            "embedding": embedding,
            "modality": "text",
            "metadata": chunk.get('metadata', {})
        }
        all_chunks.append(chunk_obj)

    # --- Table chunks ---
    for table in parsed.get("tables", []):
        table_summary = summarize_table(table)
        embedding = embed_text(table_summary)
        chunk_obj = {
            "content": table_summary,
            "embedding": embedding,
            "modality": "table",
            "metadata": table.get('metadata', {})
        }
        all_chunks.append(chunk_obj)

    # --- Image chunks ---
    for image in parsed.get("images", []):
        # Summarize the image with Gemini, returns text summary
        image_summary = summarize_image(image)
        embedding = embed_text(image_summary)
        chunk_obj = {
            "content": image_summary,
            "embedding": embedding,
            "modality": "image",
            "metadata": image.get('metadata', {})
        }
        all_chunks.append(chunk_obj)
    
    # Step 4: Index each chunk+embedding to Chroma Vector DB
    try:
        document_id = index_to_chroma(filename, all_chunks)
    except Exception as e:
        return IngestResponse(
            status="error",
            message=f"Failed to index document: {str(e)}",
            document_id=None,
        )
    
    # Step 5: Return success response
    return IngestResponse(
        status="success",
        message="File ingested, parsed, and indexed successfully.",
        document_id=document_id,
    )
