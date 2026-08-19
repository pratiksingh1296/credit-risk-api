import joblib
import pandas as pd
import numpy as np
import shap
from src.schemas import CreditRiskRequest

# Load Necessary Data

# maps
preprocessor = joblib.load("models/preprocessor_fit.joblib")
org_risk_map = joblib.load("models/org_risk_map.joblib")
income_map = joblib.load("models/income_map.joblib")
income_risk_map = joblib.load("models/income_risk_map.joblib")
education_map = {
    "Lower secondary": 0,
    "Secondary / secondary special": 1,
    "Incomplete higher": 2,
    "Higher education": 3,
    "Academic degree": 4
}

# Median data
median_row = pd.read_csv("models/app_median_row.csv")

# Model
model = joblib.load("models/xgb_calibrated.joblib")
xgb_model = joblib.load("models/xgb_model.joblib")


# Feature helper
def build_features(request: CreditRiskRequest):

    input_row = median_row.copy()

    income_group = income_map.get(
        request.income_type,
        "Other"
    )

    # Demographics
    input_row["AGE_YEARS"] = request.age
    input_row["CODE_GENDER"] = request.gender
    input_row["NAME_EDUCATION_TYPE"] = request.education
    input_row["NAME_FAMILY_STATUS"] = request.marital_status

    # Employment
    input_row["EMPLOYED_YEARS"] = request.employed_years

    # Family
    input_row["HAS_CAR"] = int(request.has_car)
    input_row["HAS_REALTY"] = int(request.has_property)
    input_row["CNT_CHILDREN"] = request.children_count
    input_row["CNT_FAM_MEMBERS"] = request.family_member_count

    # Loan
    input_row["NAME_CONTRACT_TYPE"] = request.loan_type

    # Financial / Loan values
    input_row["AMT_INCOME_TOTAL"] = request.annual_income
    input_row["AMT_CREDIT"] = request.credit_amount
    input_row["AMT_ANNUITY"] = request.annuity
    input_row["AMT_GOODS_PRICE"] = request.goods_price

    # External credit scores
    input_row["EXT_SOURCE_1"] = request.ext_credit_score_1
    input_row["EXT_SOURCE_2"] = request.ext_credit_score_2
    input_row["EXT_SOURCE_3"] = request.ext_credit_score_3

    # Log features
    input_row["AMT_INCOME_LOG"] = np.log1p(
        input_row["AMT_INCOME_TOTAL"]
    )
    input_row["AMT_CREDIT_LOG"] = np.log1p(
        input_row["AMT_CREDIT"]
    )
    input_row["AMT_ANNUITY_LOG"] = np.log1p(
        input_row["AMT_ANNUITY"]
    )
    input_row["AMT_GOODS_LOG"] = np.log1p(
        input_row["AMT_GOODS_PRICE"]
    )

    # Ratio features
    input_row["CREDIT_INCOME_RATIO"] = (
        input_row["AMT_CREDIT"] /
        input_row["AMT_INCOME_TOTAL"]
    )

    input_row["ANNUITY_INCOME_RATIO"] = (
        input_row["AMT_ANNUITY"] /
        input_row["AMT_INCOME_TOTAL"]
    )

    input_row["GOODS_CREDIT_RATIO"] = (
        input_row["AMT_GOODS_PRICE"] /
        input_row["AMT_CREDIT"]
    )

    input_row["CHILDREN_RATIO"] = (
        input_row["CNT_CHILDREN"] /
        input_row["CNT_FAM_MEMBERS"]
    )

    # Binary engineered features
    input_row["HAS_CHILDREN"] = int(
        request.children_count > 0
    )

    input_row["IS_SINGLE"] = int(
        request.family_member_count == 1
    )

    input_row["LONG_EMPLOYED"] = int(
        request.employed_years > 5
    )

    # Education encoding
    input_row["NAME_EDUCATION_ENC"] = education_map[
        request.education
    ]

    # Target-encoded risk features
    input_row["INCOME_RISK"] = income_risk_map.get(
        income_group,
        income_risk_map.mean()
    )

    input_row["ORG_RISK"] = org_risk_map.get(
        request.organization_type,
        org_risk_map.mean()
    )

    input_row = input_row.reindex(columns=preprocessor.feature_names_in_)

    return input_row


# Risk bucket helper
def risk_bucket(prob):
    if prob < 0.05:
        return "Low", "Approve"
    elif prob < 0.16:
        return "Medium", "Approve with Conditions"
    elif prob < 0.45:
        return "High", "Manual Review"
    else:
        return "Very High", "Reject"


def predict_credit_risk(request: CreditRiskRequest):

    # Build complete feature row
    features = build_features(request)

    # Apply fitted preprocessing
    features_processed = preprocessor.transform(features)

    # Predict probability of default
    probability = model.predict_proba(features_processed)[0, 1]

    # Assign risk bucket and decision
    risk_level, decision = risk_bucket(probability)

    return {
        "default_probability": probability,
        "risk_level": risk_level,
        "decision": decision
    }


def explain_credit_risk(request: CreditRiskRequest):

    input_row = build_features(request)

    input_processed = preprocessor.transform(input_row)

    feature_names = preprocessor.get_feature_names_out()
    clean_names = [name.split("__", 1)[-1] for name in feature_names]

    input_df = pd.DataFrame(input_processed,columns=clean_names)

    explainer = shap.TreeExplainer(xgb_model)
    shap_values = explainer.shap_values(input_df)

    return {
        "feature_names": clean_names,
        "shap_values": shap_values[0].tolist(),
        "base_value": float(explainer.expected_value)
    }

