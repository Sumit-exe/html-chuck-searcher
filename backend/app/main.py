from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.parser import fetch_and_clean_html
from app.embedding import embed_text
from app.weaviate_client import WeaviateHandler 
import weaviate.classes.query as wvc
from app.utils import chunk_text_and_html, make_summary

import traceback
import uvicorn

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

vectordb = WeaviateHandler(host="localhost", port=8080)

class QueryRequest(BaseModel):
    url: str
    query: str



@app.post("/search")
async def search(req: QueryRequest):
    try:
        clean_html, clean_text = fetch_and_clean_html(req.url)
        chunks = chunk_text_and_html(clean_html, clean_text, max_tokens=200)

        # collection = vectordb.client.collections.get(vectordb.collection_name)
        # collection.data.delete_many()

        # vectordb.client.collections.delete(
        #     vectordb.collection_name
        # ) 
        # where_filter = wvc.Filter.by_property("uuid").

        # Delete objects matching the filter
        # vectordb.client.collections.get(vectordb.collection_name).data.delete_many(
        #     where=where_filter,
        # )
        vectordb.reset_collection()

        # print(f"All entries deleted from collection '{vectordb.collection_name}'.")
        # WeaviateHandler._ensure_collection()
        for chunk in chunks:
            html_part = chunk["html"]
            text_part = chunk["text"]
            summary = make_summary(text_part)
            emb = embed_text(text_part)
            vectordb.add_document(html_part, text_part, summary, emb)

        q_emb = embed_text(req.query)
        results = vectordb.search(q_emb, limit=10)

        return {"results": results}

    except Exception as e:
        print("\n\n🔥 FULL ERROR 🔥")
        print(traceback.format_exc())
        print("🔥 END ERROR 🔥\n\n")

        return {"error": repr(e)}   # <-- REAL ERROR MESSAGE


# Run
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
