import pytest
from backend.ml.predictor import predict
from backend.xai.explainer import explain

SAMPLE_FEATURES = {
    "hold_mean": 0.11,
    "hold_std": 0.02,
    "hold_min": 0.06,
    "hold_max": 0.15,
    "flight_mean": 0.22,
    "flight_std": 0.08,
    "flight_min": 0.01,
    "flight_max": 0.50,
    "total_duration": 3.2,
    "backspaces": 0
}


def test_stacking_ensemble_prediction():
    res = predict(SAMPLE_FEATURES)
    assert "ensemble_probability" in res
    assert 0.0 <= res["ensemble_probability"] <= 1.0
    assert "anomaly_score" in res
    assert "model_contributions" in res

    contribs = res["model_contributions"]
    assert "Isolation Forest" in contribs
    assert "Random Forest" in contribs
    assert "XGBoost" in contribs
    assert "LightGBM" in contribs


def test_shap_explanation():
    shap_res = explain(SAMPLE_FEATURES)
    assert "global_importance" in shap_res
    assert "local_contributions" in shap_res
    assert "text_explanation" in shap_res
    assert len(shap_res["local_contributions"]) == 10
