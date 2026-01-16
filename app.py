import os
import urllib.request
import joblib
import pandas as pd
import numpy as np

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

# =====================================================
# DOWNLOAD LARGE FILES (DATASET + MODEL) AT RUNTIME
# =====================================================

DATASET_PATH = "data/Bengaluru_House_Data.csv"
MODEL_PATH = "model/land_model.pkl"

DATASET_URL = "https://huggingface.co/Uday-22/land_price_prediction/resolve/main/Bengaluru_House_Data.csv"
MODEL_URL = "https://huggingface.co/Uday-22/land_price_prediction/resolve/main/land_model.pkl"

# Download dataset if not present
if not os.path.exists(DATASET_PATH):
    os.makedirs("data", exist_ok=True)
    urllib.request.urlretrieve(DATASET_URL, DATASET_PATH)

# Download model if not present
if not os.path.exists(MODEL_PATH):
    os.makedirs("model", exist_ok=True)
    urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)

# =====================================================
# LOAD DATA & MODEL
# =====================================================

model = joblib.load(MODEL_PATH)

train_df = pd.read_csv(DATASET_PATH)
location_counts = train_df["location"].value_counts()

# =====================================================
# FASTAPI APP SETUP
# =====================================================

app = FastAPI(title="Land Price Prediction System")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# =====================================================
# INPUT SCHEMA
# =====================================================

class LandInput(BaseModel):
    location: str
    total_sqft: float
    bath: int
    bhk: int

# =====================================================
# ROUTES
# =====================================================

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

@app.post("/predict")
def predict_price(data: LandInput):
    """
    Predict land price per square foot
    """

    # Safe location density lookup
    loc_density = location_counts.get(data.location, 1)

    # Feature engineering (must match training)
    input_df = pd.DataFrame([{
        "location": data.location,
        "log_total_sqft": np.log(data.total_sqft),
        "location_density": loc_density,
        "infrastructure_score": data.bath + data.bhk
    }])

    prediction = model.predict(input_df)[0]

    return {
        "predicted_price_per_sqft": round(float(prediction), 2)
    }
