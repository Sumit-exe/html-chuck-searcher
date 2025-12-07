# app/utils.py

def chunk_text_and_html(html: str, text: str, max_tokens=200):
    words = text.split()
    chunks = []

    for i in range(0, len(words), max_tokens):
        text_chunk = " ".join(words[i:i + max_tokens])
        chunks.append({
            "html": html,
            "text": text_chunk
        })

    return chunks


def make_summary(text_chunk: str):
    sentences = text_chunk.split(".")
    return ". ".join(sentences[:2]) + "." if len(sentences) > 1 else text_chunk

