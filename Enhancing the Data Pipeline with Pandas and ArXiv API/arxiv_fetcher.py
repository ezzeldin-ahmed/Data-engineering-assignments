import pandas as pd
import requests
import xml.etree.ElementTree as ET

def fetch_arxiv_to_df(query: str) -> pd.DataFrame:
    url = (
        "http://export.arxiv.org/api/query?"
        f"search_query=all:{query}&start=0&max_results=10"
    )
    response = requests.get(url, timeout=10)
    xml_data = response.text
    root = ET.fromstring(xml_data)
    records = []
    namespace = "{http://www.w3.org/2005/Atom}"
    for entry in root.findall(f"{namespace}entry"):
        title = entry.find(f"{namespace}title").text.strip()
        summary = entry.find(f"{namespace}summary").text.strip()
        authors = [
            author.find(f"{namespace}name").text.strip()
            for author in entry.findall(f"{namespace}author")
        ]
        authors_str = ", ".join(authors)
        link = ""
        for l in entry.findall(f"{namespace}link"):
            if l.attrib.get("rel") == "alternate":
                link = l.attrib.get("href")
        records.append(
            {
                "title": title,
                "summary": summary,
                "authors": authors_str,
                "link": link,
            }
        )
    df = pd.DataFrame(records).astype("string")
    return df
