import pandas as pd
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["arxiv_db"]
collection = db["articles"]

def load_to_mongodb(df: pd.DataFrame) -> None:
    records = df.to_dict(orient="records")
    for r in records:
        doc = {
            "title": r["title"],
            "summary": r["summary"],
            "authors": r["authors"],
            "link": r["link"],
            "article_id": r["article_id"],
            "author_id": r["author_id"],
            "text": r.get("html_text", ""),
        }
        collection.insert_one(doc)
