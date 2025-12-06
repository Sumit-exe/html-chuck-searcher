# app/parser.py
import requests
from bs4 import BeautifulSoup

def fetch_and_clean_html(url: str) -> str:
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")

    # Remove unwanted tags
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    text = soup.get_text(separator=" ")
    return " ".join(text.split())
