from pathlib import Path
import joblib, pandas as pd

ROOT=Path(__file__).resolve().parents[1]
BUNDLE=joblib.load(ROOT/"models"/"best_model_bundle.joblib")

def predict_price(record: dict) -> float:
    X=pd.DataFrame([record])
    return float(BUNDLE["model"].predict(X)[0])
