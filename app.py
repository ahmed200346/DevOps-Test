from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import joblib

from model import load_model

app = FastAPI(title="API Prédiction Churn", version="1.0")

MODEL_PATH = "modele_churn.pkl"
SCALER_PATH = "scaler.pkl"
COLONNES_PATH = "colonnes.pkl"

# Chargement du modèle, du scaler et des colonnes au démarrage
try:
    model = load_model(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    colonnes_attendues = joblib.load(COLONNES_PATH)
except Exception as e:
    model = None
    scaler = None
    colonnes_attendues = None
    print(f"Erreur au chargement : {e}")


class ClientFeatures(BaseModel):
    CreditScore: int
    Geography: str      # "France", "Germany", "Spain"
    Gender: str          # "Male", "Female"
    Age: int
    Tenure: int
    Balance: float
    NumOfProducts: int
    HasCrCard: int
    IsActiveMember: int
    EstimatedSalary: float

    class Config:
        json_schema_extra = {
            "example": {
                "CreditScore": 600,
                "Geography": "France",
                "Gender": "Male",
                "Age": 40,
                "Tenure": 3,
                "Balance": 60000.0,
                "NumOfProducts": 2,
                "HasCrCard": 1,
                "IsActiveMember": 1,
                "EstimatedSalary": 50000.0,
            }
        }


@app.get("/")
def accueil():
    return {"message": "API de prédiction du Churn opérationnelle"}


@app.post("/predict")
def predict(features: ClientFeatures):
    if model is None or scaler is None or colonnes_attendues is None:
        raise HTTPException(
            status_code=500,
            detail="Modèle, scaler ou colonnes non chargés sur le serveur.",
        )

    try:
        # Transformation en DataFrame
        data = pd.DataFrame([features.model_dump()])

        # Même encodage que dans data_processing.py
        data = pd.get_dummies(data, columns=["Geography", "Gender"], drop_first=True)

        # Aligner les colonnes avec celles utilisées à l'entraînement
        for col in colonnes_attendues:
            if col not in data.columns:
                data[col] = 0
        data = data[colonnes_attendues]

        # Normalisation
        data_scaled = scaler.transform(data)

        # Prédiction
        prediction = model.predict(data_scaled)[0]
        proba = model.predict_proba(data_scaled)[0][1]

        return {
            "prediction": int(prediction),
            "churn": bool(prediction),
            "probabilite_churn": round(float(proba), 4),
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erreur de prédiction : {str(e)}")