# app/parser.py
import requests
from bs4 import BeautifulSoup

def fetch_and_clean_html(url: str):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")

    # Remove unwanted tags
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    # Extract visible text (for embedding)
    text = soup.get_text(separator=" ")
    clean_text = " ".join(text.split())

    # Keep cleaned HTML
    clean_html = str(soup)

    return clean_html, clean_text
