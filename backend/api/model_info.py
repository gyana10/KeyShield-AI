import os
import json
from fastapi import APIRouter, HTTPException, status

from backend.db.schemas import ModelInfoResponse
from backend.xai.explainer import explain, FEATURE_NAMES

router = APIRouter(prefix="", tags=["Model Information"])

METRICS_PATH = "backend/ml/models/model_metrics.json"


@router.get("/model-info", response_model=ModelInfoResponse)
def get_model_info():
    if not os.path.exists(METRICS_PATH):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Model metrics file not found. Please train models first."
        )

    with open(METRICS_PATH, "r") as f:
        metrics_data = json.load(f)

    # Sample dummy explanation to extract global importance
    dummy_feats = {f: 0.1 for f in FEATURE_NAMES}
    shap_data = explain(dummy_feats)
    global_importance = shap_data.get("global_importance", {})

    return {
        "architecture": metrics_data.get(
            "architecture",
            "Stacking Ensemble (Isolation Forest + RF + XGBoost + LightGBM -> Logistic Regression)"
        ),
        "base_models": metrics_data.get(
            "base_models",
            ["Isolation Forest", "Random Forest", "XGBoost", "LightGBM"]
        ),
        "meta_learner": metrics_data.get("meta_learner", "Logistic Regression"),
        "features": FEATURE_NAMES,
        "model_comparison": metrics_data.get("metrics", []),
        "global_feature_importance": global_importance
    }
