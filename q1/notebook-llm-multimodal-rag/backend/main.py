# backend/main.py

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from schemas import DocumentIngestRequest, QueryRequest, QueryResponse

from ingest import handle_ingest
from query import handle_query

# Create FastAPI app instance
app = FastAPI(
    title="Notebook LLM Multimodal RAG",
    description="A multimodal research assistant for advanced document retrieval and reasoning.",
    version="0.1.0"
)

# Enable CORS for local development (so Streamlit frontend can reach backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to your frontend's origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check route
@app.get("/")
def read_root():
    """
    Health check endpoint for backend service.
    """
    return {"status": "ok", "message": "Backend up and running!"}

# Document ingestion (upload) route
@app.post("/ingest")
async def ingest_document(file: UploadFile = File(...)):
    """
    Uploads a document, processes and indexes it for search/RAG.
    """
    try:
        result = await handle_ingest(file)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Query/search route
@app.post("/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    """
    Receives a natural language query; returns relevant search results from indexed docs.
    """
    try:
        result = await handle_query(request)
        return result
    except Exception as e:
        print(f"Error while handling query: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# (Optional) Add more endpoints for advanced features as needed
