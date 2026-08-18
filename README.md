## API

The project includes a FastAPI inference API for serving the trained
XGBoost + Platt-calibrated credit-risk model.


### Model

The API serves an XGBoost classifier calibrated using Platt scaling.
The model outputs a probability of default rather than only a binary
classification. This probability is then mapped to four risk categories
used by the application.

The inference pipeline reconstructs the engineered features used during
training, applies the fitted preprocessing pipeline, and passes the
result to the calibrated XGBoost model.

### Running Locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the API:
```bash
uvicorn main:app --reload
```

The API will be available at:
http://127.0.0.1:8000

Interactive API documentation:
http://127.0.0.1:8000/docs


### Running with Docker

Build the Docker image:

```bash
docker build -t credit-risk-api .
```

Run the container:
```bash
docker run -d -p 8000:8000 --name credit-risk-api-container credit-risk-api
```

The API will be available at:
http://127.0.0.1:8000

Interactive API documentation:
http://127.0.0.1:8000/docs


### Endpoints 

| Method | Endpoint   | Description                                            |
| ------ | ---------- | ------------------------------------------------------ |
| GET    | `/`        | Basic API information                                  |
| GET    | `/health`  | Check API/model status                                 |
| POST   | `/predict` | Predict default probability and assign a risk category |

### Example Request

POST /predict
```json
{
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
  "has_car": true,
  "has_property": true,
  "children_count": 0,
  "family_member_count": 1,
  "loan_type": "Cash loans",
  "organization_type": "Business Entity Type 3"
}
```

### Example Response

```json
{
  "default_probability": 0.0594146515557329,
  "risk_level": "Medium",
  "decision": "Approve with Conditions"
}
```

### Risk Categories

| Default Probability | Risk Level | Decision                |
| ------------------: | ---------- | ----------------------- |
|                < 5% | Low        | Approve                 |
|           5% – <16% | Medium     | Approve with Conditions |
|          16% – <45% | High       | Manual Review           |
|                ≥45% | Very High  | Reject                  |

