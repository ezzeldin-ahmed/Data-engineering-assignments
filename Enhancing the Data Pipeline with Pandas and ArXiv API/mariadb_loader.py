import pandas as pd
import pymysql
from typing import Tuple

connection = pymysql.connect(
    host="localhost",
    user="root",
    password="123456",
    database="arxiv_db",
    charset="utf8mb4",
    cursorclass=pymysql.cursors.DictCursor,
)

def save_row_to_mariadb(row: pd.Series) -> Tuple[int, int]:
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO authors (name) VALUES (%s)", (row["authors"],))
        author_id = cursor.lastrowid
        cursor.execute(
            "INSERT INTO articles (title, summary, link, author_id) VALUES (%s, %s, %s, %s)",
            (row["title"], row["summary"], row["link"], author_id)
        )
        article_id = cursor.lastrowid
        connection.commit()
        return article_id, author_id

def load_to_mariadb(df: pd.DataFrame) -> pd.DataFrame:
    df[["article_id", "author_id"]] = df.apply(save_row_to_mariadb, axis=1, result_type="expand")
    return df
