from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib

# Load trained pipeline (adjust relative path as needed)
clf = joblib.load("../train/heart_pipeline.joblib")

app = FastAPI(title="CVD Prediction API", version="1.0")

# The correct order matching your training and chatbot frontend
feature_names = ["age", "sex", "cp", "trestbps", "chol", "fbs", "restecg",
                 "thalach", "exang", "oldpeak", "slope", "ca", "thal"]

class HeartFeatures(BaseModel):
    age: float
    sex: int
    cp: int
    trestbps: float
    chol: float
    fbs: int
    restecg: int
    thalach: float
    exang: int
    oldpeak: float
    slope: int
    ca: float
    thal: int

@app.post("/predict")
def predict(features: HeartFeatures):
    x_dict = features.dict()
    # Create DataFrame with correct column order
    x_df = pd.DataFrame([x_dict], columns=feature_names)
    proba = float(clf.predict_proba(x_df)[0, 1])
    label = int(proba >= 0.5)
    return {"probability": proba, "label": label}
