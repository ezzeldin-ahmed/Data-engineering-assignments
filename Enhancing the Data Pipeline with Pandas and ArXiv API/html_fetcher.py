import requests
from bs4 import BeautifulSoup

def download_html_text(url: str) -> str:
    if not url:
        return ""
    r = requests.get(url, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")
    content = soup.find("div", class_="abstract") or soup
    text = content.get_text(separator="\n").strip()
    return text
