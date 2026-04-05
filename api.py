from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
import uvicorn

# Init API
app = FastAPI(
    title="Getaround Pricing API",
    description="API de prédiction de prix de location de voitures.",
    version="1.0"
)

model = joblib.load("model.joblib")

class PredictionInput(BaseModel):
    input: list[list]

# Accueil
@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API Getaround. Allez sur /docs pour la documentation interactive."}

# Endpoint de prédiction
@app.post("/predict")
def predict(data: PredictionInput):
    columns = [
        'model_key', 'mileage', 'engine_power', 'fuel', 'paint_color', 
        'car_type', 'private_parking_available', 'has_gps', 
        'has_air_conditioning', 'automatic_car', 'has_getaround_connect', 
        'has_speed_regulator', 'winter_tires'
    ]
    
    # Transformation input JSON en DataFrame
    df_input = pd.DataFrame(data.input, columns=columns)
    
    # Prédiction
    prediction = model.predict(df_input)
    
    return {"prediction": prediction.tolist()}

# Endpoint de documentation personnalisé
@app.get("/docs_info")
def docs_info():
    return {
        "title": "Getaround API Documentation",
        "description": "Cette API permet de prédire le prix journalier optimal pour une voiture de location.",
        "endpoints": [
            {
                "path": "/predict",
                "method": "POST",
                "input": "JSON object with 'input' key containing a list of car features",
                "output": "JSON object with 'prediction' key"
            }
        ]
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)