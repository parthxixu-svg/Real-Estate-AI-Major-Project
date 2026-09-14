from pathlib import Path
import json
import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from feature_engineering import model_columns

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT/"data"/"property_transactions.csv"
MODELS = ROOT/"models"
MODELS.mkdir(exist_ok=True)

df = pd.read_csv(DATA)
features = model_columns()
X = df[features]
y = df["price_inr"]
cat = ["city","locality","property_type","furnishing"]
num = [c for c in features if c not in cat]

pre = ColumnTransformer([
    ("cat", Pipeline([("imputer",SimpleImputer(strategy="most_frequent")),
                      ("onehot",OneHotEncoder(handle_unknown="ignore"))]), cat),
    ("num", Pipeline([("imputer",SimpleImputer(strategy="median"))]), num)
])

models = {
    "gradient_boosting": GradientBoostingRegressor(n_estimators=260, learning_rate=0.045, max_depth=3, random_state=42),
    "random_forest": RandomForestRegressor(n_estimators=220, max_depth=18, min_samples_leaf=2, random_state=42, n_jobs=-1)
}
Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=.2,random_state=42)
metrics={}
for name, reg in models.items():
    pipe=Pipeline([("preprocess",pre),("model",reg)])
    pipe.fit(Xtr,ytr)
    pred=pipe.predict(Xte)
    metrics[name]={
        "MAE":float(mean_absolute_error(yte,pred)),
        "RMSE":float(mean_squared_error(yte,pred)**0.5),
        "R2":float(r2_score(yte,pred))
    }
    joblib.dump(pipe, MODELS/f"{name}.joblib")

best=max(metrics,key=lambda k:metrics[k]["R2"])
json.dump({"metrics":metrics,"best_model":best,"features":features},open(MODELS/"model_metrics.json","w"),indent=2)
joblib.dump({"model":joblib.load(MODELS/f"{best}.joblib"),"features":features},MODELS/"best_model_bundle.joblib")
print(json.dumps({"best_model":best,"metrics":metrics},indent=2))
