import joblib


# Load mappings used to derive valid input categories
org_risk_map = joblib.load("models/org_risk_map.joblib")
income_map = joblib.load("models/income_map.joblib")

INCOME_TYPES =  sorted(income_map.keys())

ORGANIZATION_TYPES = sorted(org_risk_map.index.tolist())


EDUCATION_TYPES = [
    "Secondary / secondary special",
    "Higher education",
    "Incomplete higher",
    "Lower secondary",
    "Academic degree"
]

LOAN_TYPES = [
    "Cash loans",
    "Revolving loans"
]

MARITAL_STATUSES = [
    "Married",
    "Single / not married",
    "Civil marriage",
    "Widow",
    "Separated"
]