import numpy as np
import pandas as pd

TARGET = "price_inr"
CAT_COLS = ["city","locality","property_type","furnishing"]
NUM_COLS = [
    "area_sqft","bedrooms","bathrooms","property_age_years","floor_number","total_floors",
    "parking_spaces","metro_distance_km","school_distance_km","hospital_distance_km",
    "crime_index","future_infrastructure_score","historical_price_growth_pct"
]

def add_features(df):
    out = df.copy()
    out["price_per_sqft_proxy"] = out["price_inr"] / out["area_sqft"] if "price_inr" in out else 0
    out["amenity_access_score"] = (
        1/(1+out["metro_distance_km"]) +
        1/(1+out["school_distance_km"]) +
        1/(1+out["hospital_distance_km"])
    )
    out["development_adjusted_growth"] = out["historical_price_growth_pct"] * (1 + out["future_infrastructure_score"]/200)
    return out

def model_columns():
    return CAT_COLS + NUM_COLS
