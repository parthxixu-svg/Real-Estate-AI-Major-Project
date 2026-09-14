def deal_score(listing_price, predicted_price, locality_growth, infrastructure_score):
    if predicted_price <= 0: return {"score":0,"label":"Unknown","gap_pct":0}
    gap=(predicted_price-listing_price)/predicted_price*100
    score=50 + gap*2.0 + (locality_growth-7)*2 + (infrastructure_score-70)*0.15
    score=max(0,min(100,score))
    if gap >= 7: label="Undervalued"
    elif gap <= -7: label="Overpriced"
    else: label="Fairly Priced"
    return {"score":round(score,1),"label":label,"gap_pct":round(gap,2)}
