# backend/parsing.py

"""
This file handles parsing documents into their constituent modalities using the Docling + LangChainDocling integration.
- Extracts text, tables, and images from a given document file path.
- Returns a dictionary with separate lists for each modality.
"""

from langchain_docling import DoclingLoader

def parse_document(file_path: str):
    """
    Uses DoclingLoader (from langchain-docling) to extract document components.
    Args:
        file_path (str): The path to the uploaded document file.

    Returns:
        dict: {
            "text_chunks": [dict],  # Each chunk: {'content': str, 'metadata': dict}
            "tables": [dict],       # Each table: {'content': str, 'metadata': dict}
            "images": [dict]        # Each image: {'image': bytes/path, 'metadata': dict}
        }
    Raises:
        Exception: If something goes wrong during parsing.
    """
    # Initialize Docling loader for the uploaded file
    loader = DoclingLoader(file_path=file_path)
    docs = loader.load()  # Returns list of Document objects

    # Initialize result lists
    text_chunks = []
    tables = []
    images = []

    # Iterate through parsed chunks and sort by their type
    for doc in docs:
        # Docling chunk types might be: 'table', 'image', 'text', etc.
        chunk_type = doc.metadata.get("chunk_type", "text")
        
        # For text chunks
        if chunk_type == "text":
            text_chunks.append({
                "content": doc.page_content,
                "metadata": doc.metadata
            })
        
        # For table chunks (often stored as markdown or string)
        elif chunk_type == "table":
            tables.append({
                "content": doc.page_content,
                "metadata": doc.metadata
            })

        # For images, store references or raw bytes depending on Docling output
        elif chunk_type == "image":
            images.append({
                "image": doc.metadata.get("image_path", None),  # Or actual bytes if available
                "metadata": doc.metadata
            })
        # You may extend for 'code', 'chart', etc. as needed

    return {
        "text_chunks": text_chunks,
        "tables": tables,
        "images": images
    }
