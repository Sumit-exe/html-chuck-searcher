# app/utils.py

def chunk_text(text, max_tokens=500):
    """
    Split text into chunks of up to max_tokens words using simple word-based logic.
    No NLTK dependency.
    """
    words = text.split()
    chunks = []
    for i in range(0, len(words), max_tokens):
        chunks.append(" ".join(words[i:i + max_tokens]))
    return chunks
