
from fastapi import FastAPI
from src.schemas import CreditRiskRequest, CreditRiskResponse, MetadataResponse
from src.predictor import predict_credit_risk, explain_credit_risk
from src.metadata import INCOME_TYPES, ORGANIZATION_TYPES,EDUCATION_TYPES, LOAN_TYPES, MARITAL_STATUSES



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


@app.get("/metadata", response_model=MetadataResponse)
def metadata():
    return{
        "income_types": INCOME_TYPES,
        "organization_types": ORGANIZATION_TYPES,
        "education_types": EDUCATION_TYPES,
        "loan_types": LOAN_TYPES,
        "marital_statuses": MARITAL_STATUSES
    }


@app.post("/predict", response_model=CreditRiskResponse)
def predict(request: CreditRiskRequest):
    return predict_credit_risk(request)


@app.post("/explain")
def explain(request: CreditRiskRequest):
    return explain_credit_risk(request)

