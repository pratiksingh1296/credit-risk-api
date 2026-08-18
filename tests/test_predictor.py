from src.predictor import risk_bucket


def test_low_risk():
    assert risk_bucket(0.03) == ("Low", "Approve")


def test_medium_risk():
    assert risk_bucket(0.12) == (
        "Medium",
        "Approve with Conditions"
    )


def test_high_risk():
    assert risk_bucket(0.185) == (
        "High",
        "Manual Review"
    )


def test_very_high_risk():
    assert risk_bucket(0.50) == (
        "Very High",
        "Reject"
    )


def test_medium_boundary():
    assert risk_bucket(0.05) == (
        "Medium",
        "Approve with Conditions"
    )


def test_high_boundary():
    assert risk_bucket(0.16) == (
        "High",
        "Manual Review"
    )


def test_very_high_boundary():
    assert risk_bucket(0.45) == (
        "Very High",
        "Reject"
    )
