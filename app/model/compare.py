import pandas as pd

def get_most_populated_fields(df: pd.DataFrame, top_n: int = 7) -> list:
    """
    Returns top N fields (excluding name/groups) with most non-null values.
    Always includes 'indication', 'toxicity', 'absorption'.
    """
    excluded = {"name", "groups"}
    base_fields = ["indication", "toxicity", "absorption"]

    counts = df.drop(columns=list(excluded), errors='ignore').count().sort_values(ascending=False)
    top_fields = [col for col in counts.index if col not in base_fields]

    return base_fields + top_fields[:top_n]


def compare_drugs(df: pd.DataFrame, drug1: str, drug2: str, fields: list) -> dict:
    """Compare two drugs across selected fields."""
    row1 = df[df["name"].str.lower() == drug1.lower()]
    row2 = df[df["name"].str.lower() == drug2.lower()]

    if row1.empty or row2.empty:
        return {"error": "One or both drugs not found in the database."}

    d1 = row1.iloc[0]
    d2 = row2.iloc[0]

    result = {}
    for field in fields:
        val1 = d1.get(field, "")
        val2 = d2.get(field, "")

        result[field] = {
            "drug1": str(val1).strip() if pd.notna(val1) else "",
            "drug2": str(val2).strip() if pd.notna(val2) else ""
        }

    return result
