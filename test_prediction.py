import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from prediction import predict_price
def test_prediction_positive():
    r={"city":"Ahmedabad","locality":"Bodakdev","property_type":"Apartment","furnishing":"Semi-Furnished",
       "area_sqft":1200,"bedrooms":2,"bathrooms":2,"property_age_years":5,"floor_number":5,"total_floors":12,
       "parking_spaces":1,"metro_distance_km":1.5,"school_distance_km":1.2,"hospital_distance_km":1.8,
       "crime_index":25,"future_infrastructure_score":80,"historical_price_growth_pct":8}
    assert predict_price(r)>0
