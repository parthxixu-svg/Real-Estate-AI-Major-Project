import pandas as pd

def locality_summary(df, locality):
    x=df[df.locality==locality]
    if x.empty: return {}
    return {
        "transactions":len(x),
        "median_price":float(x.price_inr.median()),
        "median_price_per_sqft":float((x.price_inr/x.area_sqft).median()),
        "median_rent":float(x.monthly_rent_inr.median()),
        "avg_growth":float(x.historical_price_growth_pct.mean()),
        "avg_infrastructure":float(x.future_infrastructure_score.mean()),
        "avg_crime":float(x.crime_index.mean())
    }
