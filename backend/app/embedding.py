# app/embedding.py
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_text(text: str):
    """
    Returns embedding as a Python list (not numpy array).
    """
    return model.encode([text])[0].tolist()
