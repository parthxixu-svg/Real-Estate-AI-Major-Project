from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

def load_transactions():
    df = pd.read_csv(DATA / "property_transactions.csv", parse_dates=["date"])
    return df

def load_localities():
    return pd.read_csv(DATA / "locality_data.csv")

def load_infrastructure():
    return pd.read_csv(DATA / "infrastructure.csv")
