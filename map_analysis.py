import math
import pandas as pd

def haversine_km(lat1,lon1,lat2,lon2):
    p=math.pi/180
    a=0.5-math.cos((lat2-lat1)*p)/2+math.cos(lat1*p)*math.cos(lat2*p)*(1-math.cos((lon2-lon1)*p))/2
    return 12742*math.asin(math.sqrt(a))

def within_radius(df,lat,lon,radius_km):
    out=df.copy()
    out["distance_km"]=[haversine_km(lat,lon,a,b) for a,b in zip(out.latitude,out.longitude)]
    return out[out.distance_km<=radius_km].copy()
