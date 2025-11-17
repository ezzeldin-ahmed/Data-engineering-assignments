import pandas as pd

def load_csv_to_df(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, dtype="string")
    return df
