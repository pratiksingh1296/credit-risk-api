from fastapi import FastAPI
from src.schemas import CreditRiskRequest, CreditRiskResponse
from src.predictor import predict_credit_risk


app = FastAPI()

@app.get("/")
def home():
    return {"message": "Credit Risk API"}


@app.get("/health")
def health():
    return {
        "status": "ok",
        "model": "xgboost_platt"
    }


# Endpoint
@app.post("/predict", response_model=CreditRiskResponse)
def predict(request: CreditRiskRequest):
    return predict_credit_risk(request)

