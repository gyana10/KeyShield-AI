import pytest
from backend.ml.predictor import predictor_engine
from backend.ml.feature_engineering import extract_keystroke_features, create_behavioral_profile

RAW_EVENTS = [
    {"key": "T", "type": "keydown", "time": 0.0},
    {"key": "T", "type": "keyup", "time": 110.0},
    {"key": "h", "type": "keydown", "time": 140.0},
    {"key": "h", "type": "keyup", "time": 250.0},
    {"key": "e", "type": "keydown", "time": 290.0},
    {"key": "e", "type": "keyup", "time": 400.0}
]


def test_stacking_ensemble_prediction():
    feats = [extract_keystroke_features(RAW_EVENTS)] * 5
    profile = create_behavioral_profile(feats)

    res = predictor_engine.evaluate_verification(RAW_EVENTS, profile)
    assert res["decision"] in ["GENUINE", "SUSPICIOUS"]
    assert "isolation_forest_score" in res
    assert "stacking_probability" in res
    assert "text_explanation" in res
    assert "top_contributing_features" in res
