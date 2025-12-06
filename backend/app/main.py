from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.parser import fetch_and_clean_html
from app.embedding import embed_text
from app.weaviate_client import WeaviateHandler
from app.utils import chunk_text
import uvicorn

app = FastAPI()

# -------------------------------
# CORS Middleware - allow all origins
# -------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# Weaviate handler
# -------------------------------
vectordb = WeaviateHandler(host="localhost", port=8080)

# -------------------------------
# Request model
# -------------------------------
class QueryRequest(BaseModel):
    url: str
    query: str

# -------------------------------
# Search endpoint
# -------------------------------
@app.post("/search")
async def search(req: QueryRequest):
    try:
        # 1. Fetch and clean HTML
        html = fetch_and_clean_html(req.url)

        # 2. Split into chunks
        chunks = chunk_text(html, max_tokens=500)

        # 3. Insert chunks into Weaviate
        for chunk in chunks:
            emb = embed_text(chunk)
            vectordb.add_document(chunk, emb)

        # 4. Embed query
        q_embedding = embed_text(req.query)

        # 5. Search top 10 chunks from Weaviate
        top_chunks = vectordb.search(q_embedding, limit=10)

        return {"results": top_chunks}

    except Exception as e:
        return {"error": str(e)}

# -------------------------------
# Run server
# -------------------------------
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
