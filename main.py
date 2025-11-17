from arxiv_fetcher import fetch_arxiv_to_df
from html_fetcher import download_html_text
from mariadb_loader import load_to_mariadb
from mongodb_loader import load_to_mongodb

def main() -> None:
    print("Fetching data from ArXiv...")
    df = fetch_arxiv_to_df("machine learning")

    print("Downloading HTML content...")
    df["html_text"] = df["link"].apply(download_html_text)

    print("Loading into MariaDB (SQL)...")
    df = load_to_mariadb(df)

    print("Loading into MongoDB (NoSQL)...")
    load_to_mongodb(df)

    print("Pipeline finished successfully.")

if __name__ == "__main__":
    main()
