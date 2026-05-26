from fastapi.testclient import TestClient

from app.main import app


def test_health() -> None:
    with TestClient(app) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_ready() -> None:
    with TestClient(app) as client:
        response = client.get("/ready")

    assert response.status_code == 200
    assert response.json()["status"] == "ready"


def test_predict_success() -> None:
    with TestClient(app) as client:
        response = client.post(
            "/predict",
            json={"wt": 2.62, "hp": 110},
        )

    assert response.status_code == 200
    data = response.json()
    assert "predicted_mpg" in data


def test_predict_missing_field() -> None:
    with TestClient(app) as client:
        response = client.post(
            "/predict",
            json={"wt": 2.62},
        )

    assert response.status_code == 422