from pathlib import Path

import joblib
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score


ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT_DIR / "mtcars.csv"
MODEL_PATH = ROOT_DIR / "models" / "model.pkl"

FEATURES = ["wt", "hp"]
TARGET = "mpg"


def main() -> None:
    df = pd.read_csv(DATA_PATH)

    X = df[FEATURES]
    y = df[TARGET]

    model = LinearRegression()
    model.fit(X, y)

    predictions = model.predict(X)
    r2 = r2_score(y, predictions)
    rmse = mean_squared_error(y, predictions) ** 0.5

    model_bundle = {
        "model": model,
        "features": FEATURES,
        "target": TARGET,
        "metrics": {
            "r2": float(r2),
            "rmse": float(rmse),
        },
    }

    MODEL_PATH.parent.mkdir(exist_ok=True)
    joblib.dump(model_bundle, MODEL_PATH)

    print(f"Saved model to {MODEL_PATH}")
    print(f"Features: {FEATURES}")
    print(f"R2: {r2:.3f}")
    print(f"RMSE: {rmse:.3f}")


if __name__ == "__main__":
    main()