import json, sys, math
from pathlib import Path
import streamlit as st
import pandas as pd
import numpy as np
import folium
from folium.plugins import Draw, HeatMap
from streamlit_folium import st_folium

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/"src"))
from data_loader import load_transactions, load_localities, load_infrastructure
from prediction import predict_price
from investment import investment_summary, appreciation_projection
from deal_scorer import deal_score
from map_analysis import within_radius
from utilities import inr

st.set_page_config(page_title="Real Estate AI Analyzer", page_icon="🏠", layout="wide")

@st.cache_data
def get_data():
    return load_transactions(), load_localities(), load_infrastructure()

df, loc, infra = get_data()

st.sidebar.title("🏠 Real Estate AI")
page=st.sidebar.radio("Navigation",[
    "Market Dashboard","AI Price Prediction","Locality Intelligence",
    "Investment Analyzer","Deal Scorer","Property Comparison","Map Intelligence","Model Evaluation"
])
st.sidebar.caption("Academic major-project demo. Dataset is synthetic.")

def money(x): return f"₹{x:,.0f}"

if page=="Market Dashboard":
    st.title("Real Estate Price Prediction & Investment Analyzer")
    st.write("AI-assisted property valuation, locality intelligence and investment analysis.")
    c1,c2,c3,c4=st.columns(4)
    c1.metric("Properties",f"{len(df):,}")
    c2.metric("Localities",df.locality.nunique())
    c3.metric("Median Price",money(df.price_inr.median()))
    c4.metric("Median Rent",money(df.monthly_rent_inr.median()))
    st.subheader("Price distribution")
    st.bar_chart(df.groupby("locality")["price_inr"].median().sort_values(ascending=False))
    st.subheader("Locality overview")
    view=loc.copy()
    view["median_price_per_sqft"]=view["median_price_per_sqft"].round(0)
    st.dataframe(view,use_container_width=True)

elif page=="AI Price Prediction":
    st.title("🤖 AI Property Price Prediction")
    c1,c2,c3=st.columns(3)
    locality=c1.selectbox("Locality",sorted(df.locality.unique()))
    property_type=c2.selectbox("Property Type",sorted(df.property_type.unique()))
    furnishing=c3.selectbox("Furnishing",sorted(df.furnishing.unique()))
    c1,c2,c3,c4=st.columns(4)
    area=c1.number_input("Area (sq ft)",300,5000,1200)
    beds=c2.number_input("Bedrooms",1,6,2)
    baths=c3.number_input("Bathrooms",1,5,2)
    age=c4.number_input("Property Age",0,60,5)
    c1,c2,c3,c4=st.columns(4)
    floor=c1.number_input("Floor",1,40,5)
    total_floors=c2.number_input("Total Floors",1,50,12)
    parking=c3.number_input("Parking Spaces",0,5,1)
    metro=c4.number_input("Metro Distance (km)",0.1,20.0,2.0)
    c1,c2,c3,c4=st.columns(4)
    school=c1.number_input("School Distance (km)",0.1,20.0,2.0)
    hospital=c2.number_input("Hospital Distance (km)",0.1,20.0,2.0)
    crime=c3.slider("Crime Index",0.0,100.0,30.0)
    infra_score=c4.slider("Future Infrastructure Score",0.0,100.0,75.0)
    growth=st.slider("Historical Price Growth (%)",3.0,15.0,8.0)
    if st.button("Predict Property Price",type="primary"):
        lat=float(loc[loc.locality==locality].latitude.iloc[0]); lon=float(loc[loc.locality==locality].longitude.iloc[0])
        rec={"city":"Ahmedabad","locality":locality,"property_type":property_type,"furnishing":furnishing,
             "area_sqft":area,"bedrooms":beds,"bathrooms":baths,"property_age_years":age,
             "floor_number":floor,"total_floors":total_floors,"parking_spaces":parking,
             "metro_distance_km":metro,"school_distance_km":school,"hospital_distance_km":hospital,
             "crime_index":crime,"future_infrastructure_score":infra_score,
             "historical_price_growth_pct":growth}
        pred=predict_price(rec)
        st.success(f"Estimated market value: {money(pred)}")
        st.metric("Estimated price / sq ft",money(pred/area))
        proj=appreciation_projection(pred,growth,infra_score)
        st.subheader("Predicted appreciation scenarios")
        st.dataframe(pd.DataFrame({"Horizon":["1 year","3 years","5 years"],
            "Projected Value":[proj[1],proj[3],proj[5]]}).assign(**{"Projected Value":lambda x:x["Projected Value"].map(money)}),hide_index=True)

elif page=="Locality Intelligence":
    st.title("📍 Locality Intelligence")
    locality=st.selectbox("Choose locality",sorted(df.locality.unique()))
    x=df[df.locality==locality].copy()
    c1,c2,c3,c4=st.columns(4)
    c1.metric("Median Price",money(x.price_inr.median()))
    c2.metric("Price / sq ft",money((x.price_inr/x.area_sqft).median()))
    c3.metric("Median Rent",money(x.monthly_rent_inr.median()))
    c4.metric("Growth",f"{x.historical_price_growth_pct.mean():.1f}%")
    st.line_chart(x.assign(year=x.date.dt.year).groupby("year")["price_inr"].median())
    st.write("Locality factors")
    st.dataframe(x[["metro_distance_km","school_distance_km","hospital_distance_km","crime_index","future_infrastructure_score","historical_price_growth_pct"]].describe().T,use_container_width=True)

elif page=="Investment Analyzer":
    st.title("💰 Investment Return Projector")
    price=st.number_input("Purchase Price (₹)",100000,100000000,7500000,step=100000)
    down=st.slider("Down Payment (%)",10,100,25)
    rate=st.number_input("Loan Interest (%)",0.0,20.0,8.5,step=0.1)
    loan_years=st.slider("Loan Tenure (years)",1,30,20)
    rent=st.number_input("Monthly Rent (₹)",0,1000000,30000,step=1000)
    maint=st.number_input("Monthly Maintenance (₹)",0,100000,3000,step=500)
    tax=st.number_input("Annual Property Tax (₹)",0,1000000,25000,step=5000)
    trans=st.number_input("Transaction Costs (%)",0.0,20.0,6.0,step=0.5)
    growth=st.slider("Annual Appreciation (%)",0.0,20.0,8.0)
    years=st.slider("Projection Horizon",1,20,5)
    if st.button("Analyze Investment",type="primary"):
        s=investment_summary(price,down,rate,loan_years,rent,maint,tax,trans,growth,years)
        a,b,c,d=st.columns(4)
        a.metric("Monthly EMI",money(s["monthly_emi"]))
        b.metric("Gross Yield",f'{s["gross_yield_pct"]:.2f}%')
        c.metric("Net Yield",f'{s["net_yield_pct"]:.2f}%')
        d.metric("Estimated ROI",f'{s["estimated_roi_pct"]:.2f}%')
        st.write({"Future Value":money(s["future_value"]),"Capital Appreciation":money(s["capital_appreciation"]),
                  "Initial Investment":money(s["total_initial_investment"])})

elif page=="Deal Scorer":
    st.title("🎯 AI Deal Scorer")
    locality=st.selectbox("Locality",sorted(df.locality.unique()))
    list_price=st.number_input("Listing Price (₹)",100000,100000000,6500000,step=100000)
    x=df[df.locality==locality]
    sample=x.iloc[len(x)//2]
    rec={c:sample[c] for c in ["city","locality","property_type","furnishing","area_sqft","bedrooms","bathrooms",
        "property_age_years","floor_number","total_floors","parking_spaces","metro_distance_km",
        "school_distance_km","hospital_distance_km","crime_index","future_infrastructure_score","historical_price_growth_pct"]}
    rec["area_sqft"]=st.number_input("Area (sq ft)",300,5000,int(sample.area_sqft))
    predicted=predict_price(rec)
    st.metric("Model Estimated Value",money(predicted))
    score=deal_score(list_price,predicted,float(x.historical_price_growth_pct.mean()),float(x.future_infrastructure_score.mean()))
    st.metric("Deal Score",f'{score["score"]}/100')
    if score["label"]=="Undervalued": st.success(score["label"])
    elif score["label"]=="Overpriced": st.error(score["label"])
    else: st.warning(score["label"])
    st.write(f"Price gap vs model: {score['gap_pct']:.2f}%")

elif page=="Property Comparison":
    st.title("⚖️ Property Comparison")
    choices=df.sample(4,random_state=7).copy()
    choices["label"]=choices.apply(lambda r:f'{r["locality"]} | {int(r["area_sqft"])} sq ft | {money(r["price_inr"])}',axis=1)
    selected=st.multiselect("Select up to 4 properties",choices.label.tolist(),default=choices.label.tolist()[:3])
    comp=choices[choices.label.isin(selected)].copy()
    if not comp.empty:
        comp["price_per_sqft"]=comp.price_inr/comp.area_sqft
        st.dataframe(comp[["label","bedrooms","bathrooms","price_inr","price_per_sqft","monthly_rent_inr","historical_price_growth_pct","future_infrastructure_score"]],hide_index=True,use_container_width=True)

elif page=="Map Intelligence":
    st.title("🗺️ Map Intelligence")
    st.caption("Draw a circle to inspect properties in an area. A manual center/radius fallback is also provided.")
    center=[float(df.latitude.mean()),float(df.longitude.mean())]
    m=folium.Map(location=center,zoom_start=11)
    for _,r in df.sample(min(500,len(df)),random_state=3).iterrows():
        folium.CircleMarker([r.latitude,r.longitude],radius=3,popup=f'{r.locality} | {money(r.price_inr)}').add_to(m)
    HeatMap(df[["latitude","longitude","price_inr"]].sample(min(700,len(df)),random_state=5).values.tolist(),
            radius=10,blur=12).add_to(m)
    Draw(export=True,draw_options={"polyline":False,"polygon":False,"rectangle":False,"circle":True,"marker":False,"circlemarker":False},
         edit_options={"edit":True,"remove":True}).add_to(m)
    st_data=st_folium(m,width=None,height=600,key="real_estate_map")
    st.subheader("Manual area analysis")
    c1,c2,c3=st.columns(3)
    lat=c1.number_input("Center latitude",21.0,25.0,23.03,format="%.5f")
    lon=c2.number_input("Center longitude",70.0,75.0,72.52,format="%.5f")
    rad=c3.number_input("Radius (km)",0.1,20.0,2.0)
    area_df=within_radius(df,lat,lon,rad)
    st.metric("Properties in selected radius",len(area_df))
    if len(area_df):
        st.write(f"Median price: {money(area_df.price_inr.median())} | Median growth: {area_df.historical_price_growth_pct.median():.1f}%")
        st.dataframe(area_df[["locality","area_sqft","price_inr","monthly_rent_inr","historical_price_growth_pct"]].head(50),hide_index=True)

elif page=="Model Evaluation":
    st.title("📊 Model Evaluation")
    metrics=json.load(open(ROOT/"models"/"model_metrics.json"))
    st.write(f"Best model: **{metrics['best_model']}**")
    rows=[]
    for name,m in metrics["metrics"].items():
        rows.append({"Model":name,"MAE":m["MAE"],"RMSE":m["RMSE"],"R²":m["R2"]})
    st.dataframe(pd.DataFrame(rows),hide_index=True,use_container_width=True)
    st.bar_chart(pd.DataFrame(rows).set_index("Model")[["R²"]])
    st.info("Metrics are computed on the included synthetic academic dataset. They are not evidence of real-world market accuracy.")
