# MTCARS MPG Prediction API

## Project Overview

This project builds a FastAPI application that predicts a car's miles per gallon (`mpg`) using the `mtcars.csv` dataset. The model is trained in Python, saved as a `.pkl` file, served through an API, containerized with Podman, and deployed to Google Cloud Run.

Deployed API:

```text
https://mtcars-fastapi-5130901709.us-west2.run.app
```

## Model

The model is a linear regression model trained with `scikit-learn`.

- Dataset: `mtcars.csv`
- Response variable: `mpg`
- Prediction variables:
  - `wt`: car weight in 1000 lbs
  - `hp`: gross horsepower
- Saved model: `models/model.pkl`
- Training script: `scripts/train_model.py`

To rebuild the model:

```bash
python scripts/train_model.py
```

## Repository Structure

```text
mtcars-fastapi-api/
├── README.md
├── Dockerfile
├── .dockerignore
├── .gcloudignore
├── pytest.ini
├── requirements.txt
├── mtcars.csv
├── app/
│   ├── __init__.py
│   └── main.py
├── models/
│   └── model.pkl
├── scripts/
│   └── train_model.py
└── tests/
    ├── __init__.py
    └── test_api.py
```

## File Descriptions

- `app/main.py`: FastAPI app with `/health`, `/ready`, and `/predict`
- `scripts/train_model.py`: trains and saves the regression model
- `models/model.pkl`: saved trained model
- `tests/test_api.py`: automated API tests
- `Dockerfile`: container build instructions
- `requirements.txt`: Python dependencies
- `mtcars.csv`: training dataset

## Local Setup

Clone the repository:

```bash
git clone YOUR_GITHUB_REPO_URL
cd mtcars-fastapi-api
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Rebuild the model:

```bash
python scripts/train_model.py
```

Run the API locally:

```bash
uvicorn app.main:app --reload --port 8080
```

Open API docs:

```text
http://localhost:8080/docs
```

## API Endpoints

### GET `/health`

Checks whether the API is running.

```bash
curl http://localhost:8080/health
```

Example response:

```json
{
  "status": "ok"
}
```

### GET `/ready`

Checks whether the model is loaded.

```bash
curl http://localhost:8080/ready
```

Example response:

```json
{
  "status": "ready",
  "features": ["wt", "hp"],
  "target": "mpg"
}
```

### POST `/predict`

Predicts `mpg` from `wt` and `hp`.

```bash
curl -X POST "http://localhost:8080/predict" \
  -H "Content-Type: application/json" \
  -d '{"wt": 2.62, "hp": 110}'
```

Example response:

```json
{
  "predicted_mpg": 23.57,
  "input": {
    "wt": 2.62,
    "hp": 110
  }
}
```

## Tests

Run tests:

```bash
python -m pytest
```

## Podman Build and Run

Build the image:

```bash
podman build -t mtcars-fastapi .
```

Run the container locally:

```bash
podman run --rm -p 8080:8080 mtcars-fastapi
```

Test the local container:

```bash
curl http://localhost:8080/health
```

## Deployment Instructions

Set deployment variables:

```bash
export PROJECT_ID="YOUR_PROJECT_ID"
export REGION="YOUR_REGION"
export REPO="mtcars-api-repo"
export IMAGE="mtcars-fastapi"
```

Example:

```bash
export REGION="us-west2"
```

Enable Google Cloud services:

```bash
gcloud services enable run.googleapis.com artifactregistry.googleapis.com cloudbuild.googleapis.com
```

Create Artifact Registry repository:

```bash
gcloud artifacts repositories create $REPO \
  --repository-format=docker \
  --location=$REGION \
  --description="Docker images for mtcars FastAPI API"
```

Tag the image:

```bash
podman tag mtcars-fastapi \
  $REGION-docker.pkg.dev/$PROJECT_ID/$REPO/$IMAGE:latest
```

Log in to Artifact Registry:

```bash
gcloud auth print-access-token | podman login $REGION-docker.pkg.dev \
  -u oauth2accesstoken \
  --password-stdin
```

Push the image:

```bash
podman push $REGION-docker.pkg.dev/$PROJECT_ID/$REPO/$IMAGE:latest
```

Alternatively, build and push with Google Cloud Build:

```bash
gcloud builds submit . \
  --tag $REGION-docker.pkg.dev/$PROJECT_ID/$REPO/$IMAGE:latest \
  --project $PROJECT_ID
```

Deploy to Cloud Run:

```bash
gcloud run deploy mtcars-fastapi \
  --image $REGION-docker.pkg.dev/$PROJECT_ID/$REPO/$IMAGE:latest \
  --region $REGION \
  --allow-unauthenticated \
  --port 8080
```

## Deployed API URL

```text
https://mtcars-fastapi-5130901709.us-west2.run.app
```

Test deployed API:

```bash
curl https://mtcars-fastapi-5130901709.us-west2.run.app/health
```

Prediction example:

```bash
curl -X POST "https://mtcars-fastapi-5130901709.us-west2.run.app/predict" \
  -H "Content-Type: application/json" \
  -d '{"wt": 2.62, "hp": 110}'
```
