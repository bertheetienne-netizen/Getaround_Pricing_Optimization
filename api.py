from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
import uvicorn

app = FastAPI(
    title="Getaround Pricing API",
    description=(
        "Cette API permet de prédire le prix journalier optimal pour une voiture de location.\n\n"
        "### Endpoints disponibles :\n"
        "* **POST /predict** : Soumettre des caractéristiques de véhicules pour obtenir les prix estimés.\n"
        "Accédez à la documentation Swagger interactive ci-dessous pour tester directement."
    ),
    version="1.0"
)

# Chargement du modèle entraîné
model = joblib.load("model.joblib")

class PredictionInput(BaseModel):
    input: list[list]

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API Getaround. Allez sur /docs pour la documentation interactive."}

@app.post("/predict")
def predict(data: PredictionInput):
    columns = [
        'model_key', 'mileage', 'engine_power', 'fuel', 'paint_color', 
        'car_type', 'private_parking_available', 'has_gps', 
        'has_air_conditioning', 'automatic_car', 'has_getaround_connect', 
        'has_speed_regulator', 'winter_tires'
    ]
    
    df_input = pd.DataFrame(data.input, columns=columns)
    
    df_input['mileage'] = df_input['mileage'].astype(float)
    df_input['engine_power'] = df_input['engine_power'].astype(float)
    
    bool_cols = [
        'private_parking_available', 'has_gps', 'has_air_conditioning', 
        'automatic_car', 'has_getaround_connect', 'has_speed_regulator', 'winter_tires'
    ]
    for col in bool_cols:
        df_input[col] = df_input[col].astype(bool)
    
    prediction = model.predict(df_input)
    return {"prediction": prediction.tolist()}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)