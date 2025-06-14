import pandas as pd
from pathlib import Path
import zipfile
from model.compare import get_most_populated_fields

ZIP_PATH = Path("app/data/drugbank_clean.csv.zip")

def load_drug_data() -> pd.DataFrame:
    """Load and return the DrugBank dataset from zip."""
    with zipfile.ZipFile(ZIP_PATH, 'r') as archive:
        csv_file = [f for f in archive.namelist() if f.endswith(".csv")][0]
        with archive.open(csv_file) as file:
            df = pd.read_csv(file)

    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
    return df


def get_drug_categories(df: pd.DataFrame) -> list:
    """Return a sorted list of drug categories based on 'groups' field."""
    all_groups = df["groups"].dropna().astype(str).str.split(';')
    flat_groups = [g.strip() for sublist in all_groups for g in sublist if g.strip()]
    return sorted(set(flat_groups))


def get_classification_fields(df: pd.DataFrame) -> list:
    """Return best fields for comparison using coverage logic."""
    return get_most_populated_fields(df, top_n=7)
