from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


ROOT_DIR = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT_DIR / "models" / "model.pkl"

model_bundle: dict[str, Any] | None = None
load_error: str | None = None


class PredictionRequest(BaseModel):
    wt: float = Field(..., gt=0, description="Car weight in 1000 lbs")
    hp: float = Field(..., gt=0, description="Gross horsepower")


@asynccontextmanager
async def lifespan(app: FastAPI):
    global model_bundle, load_error

    try:
        if not MODEL_PATH.exists():
            raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")
        model_bundle = joblib.load(MODEL_PATH)
        load_error = None
    except Exception as error:
        model_bundle = None
        load_error = str(error)

    yield


app = FastAPI(
    title="MTCARS MPG Prediction API",
    description="Predicts car miles per gallon using weight and horsepower.",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/ready")
def ready() -> dict[str, Any]:
    if model_bundle is None:
        raise HTTPException(
            status_code=503,
            detail=f"Model is not ready: {load_error}",
        )

    return {
        "status": "ready",
        "features": model_bundle["features"],
        "target": model_bundle["target"],
    }


@app.post("/predict")
def predict(request: PredictionRequest) -> dict[str, Any]:
    if model_bundle is None:
        raise HTTPException(
            status_code=503,
            detail=f"Model is not available: {load_error}",
        )

    input_data = pd.DataFrame(
        [{"wt": request.wt, "hp": request.hp}],
        columns=model_bundle["features"],
    )

    prediction = model_bundle["model"].predict(input_data)[0]

    return {
        "predicted_mpg": round(float(prediction), 2),
        "input": {
            "wt": request.wt,
            "hp": request.hp,
        },
    }