import joblib
from pydantic import BaseModel, Field, field_validator
from typing import Literal


income_map = joblib.load("models/income_map.joblib")
org_risk_map = joblib.load("models/org_risk_map.joblib")

income_types = sorted(income_map.keys())
organization_types = sorted(org_risk_map.index.tolist())

# Pydantic Schema
class CreditRiskRequest(BaseModel):

    # Demographics
    age: int = Field(ge=18, le=120)
    gender: Literal["M", "F"] = Field(
            examples=["M", "F"],
            description="Accepted values: M = Male, F = Female"
        )
    education: Literal["Secondary / secondary special", "Higher education", "Incomplete higher", "Lower secondary", "Academic degree"] = Field(
            examples=["Secondary / secondary special", "Higher education", "Incomplete higher", "Lower secondary", "Academic degree"],
        )
    marital_status: Literal["Married", "Single / not married", "Civil marriage", "Widow", "Separated"] = Field(
            examples=["Married", "Single / not married", "Civil marriage", "Widow", "Separated"]
        )
    
    # Employed / income
    income_type: str = Field(
            examples=income_types
        )
    employed_years: float = Field(ge=0.0, le=40.0)
    annual_income: int = Field(gt=0, le=10000000)

    # Financial / Loan
    ext_credit_score_1: float = Field(ge=0.0, le=1.0)
    ext_credit_score_2: float = Field(ge=0.0, le=1.0)
    ext_credit_score_3: float = Field(ge=0.0, le=1.0)
    credit_amount: int = Field(gt=0, le=5000000)
    annuity: int = Field(ge=0.0, le=5000000)
    goods_price: int = Field(ge=0, le=5000000, description="Value of the goods/property being financed.")

    # Family
    has_car: bool
    has_property: bool
    children_count: int = Field(ge=0, le=20)
    family_member_count: int = Field(ge=1, le=30)

    # Loan
    loan_type: Literal["Cash loans", "Revolving loans"] = Field(
        description="Specify the loan type : Cash loans / Revolving loans"
    )

    # Organization
    organization_type: str = Field(
        examples=organization_types
    )

    # Dynamic validation
    @field_validator("income_type")
    @classmethod
    def validate_income_type(cls, value):
        if value not in income_types:
            raise ValueError(
                f"Invalid income_type: '{value}'"
            )
        return value

    @field_validator("organization_type")
    @classmethod
    def validate_organization_type(cls, value):
        if value not in organization_types:
            raise ValueError(
                f"Invalid organization_type: '{value}'"
            )
        return value


# Response Model
class CreditRiskResponse(BaseModel):
    default_probability: float = Field(ge=0.0, le=1.0)
    risk_level: Literal["Low", "Medium", "High", "Very High"]
    decision: Literal[
        "Approve",
        "Approve with Conditions",
        "Manual Review",
        "Reject"
    ]


# Metadata Response
class MetadataResponse(BaseModel):
    income_types: list[str]
    organization_types: list[str]
    education_types: list[str]
    loan_types: list[str]
    marital_statuses: list[str]