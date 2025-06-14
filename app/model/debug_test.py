# app/model/debug_drug_fields.py

import pandas as pd
from zipfile import ZipFile
from pathlib import Path

ZIP_PATH = Path("app/data/drugbank_clean.csv.zip")
FIELDS_TO_CHECK = [
    "indication", "mechanism_of_action", "toxicity",
    "absorption", "half_life", "route_of_elimination",
    "drug_interactions", "food_interactions", "atc_codes"
]

def load_and_check_fields(zip_path: Path):
    with ZipFile(zip_path, 'r') as z:
        csv_name = [f for f in z.namelist() if f.endswith(".csv")][0]
        with z.open(csv_name) as f:
            df = pd.read_csv(f)

    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
    fields = [f for f in FIELDS_TO_CHECK if f in df.columns]

    print(f"📊 Checking fields in: {csv_name}")
    print("-" * 60)

    for field in fields:
        total = len(df)
        missing = df[field].isna().sum()
        empty_str = (df[field].astype(str).str.strip() == "").sum()
        available = total - missing - empty_str

        print(f"{field.title():<25} ➤ Available: {available:<5} | Missing: {missing:<5} | Empty: {empty_str}")

if __name__ == "__main__":
    load_and_check_fields(ZIP_PATH)
