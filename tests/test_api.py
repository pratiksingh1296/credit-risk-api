from fastapi.testclient import TestClient
from main import app    


client = TestClient(app)

def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "model": "xgboost_platt"
    }


def test_predict():
    payload = {
        "age": 35,
        "gender": "M",
        "education": "Higher education",
        "marital_status": "Married",
        "income_type": "Working",
        "employed_years": 5,
        "annual_income": 500000,
        "ext_credit_score_1": 0.51,
        "ext_credit_score_2": 0.57,
        "ext_credit_score_3": 0.54,
        "credit_amount": 500000,
        "annuity": 25000,
        "goods_price": 500000,
        "has_car": True,
        "has_property": True,
        "children_count": 0,
        "family_member_count": 1,
        "loan_type": "Cash loans",
        "organization_type": "Business Entity Type 3"
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert "default_probability" in data
    assert "risk_level" in data
    assert "decision" in data

    assert 0.0 <= data["default_probability"] <= 1.0

    assert data["risk_level"] in {
        "Low",
        "Medium",
        "High",
        "Very High"
    }

    assert data["decision"] in {
        "Approve",
        "Approve with Conditions",
        "Manual Review",
        "Reject"
    }


def test_predict_invalid_age():
    payload = {
        "age": 10,
        "gender": "M",
        "education": "Higher education",
        "marital_status": "Married",
        "income_type": "Working",
        "employed_years": 5,
        "annual_income": 500000,
        "ext_credit_score_1": 0.51,
        "ext_credit_score_2": 0.57,
        "ext_credit_score_3": 0.54,
        "credit_amount": 500000,
        "annuity": 25000,
        "goods_price": 500000,
        "has_car": True,
        "has_property": True,
        "children_count": 0,
        "family_member_count": 1,
        "loan_type": "Cash loans",
        "organization_type": "Business Entity Type 3"
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 422


def test_predict_invalid_income_type():
    payload = {
        "age": 35,
        "gender": "M",
        "education": "Higher education",
        "marital_status": "Married",
        "income_type": "Definitely Not A Real Income Type",
        "employed_years": 5,
        "annual_income": 500000,
        "ext_credit_score_1": 0.51,
        "ext_credit_score_2": 0.57,
        "ext_credit_score_3": 0.54,
        "credit_amount": 500000,
        "annuity": 25000,
        "goods_price": 500000,
        "has_car": True,
        "has_property": True,
        "children_count": 0,
        "family_member_count": 1,
        "loan_type": "Cash loans",
        "organization_type": "Business Entity Type 3"
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 422


