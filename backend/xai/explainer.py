import os
import joblib
import numpy as np
import shap


FEATURE_NAMES = [
    "hold_mean",
    "hold_std",
    "hold_min",
    "hold_max",
    "flight_mean",
    "flight_std",
    "flight_min",
    "flight_max",
    "total_duration",
    "backspaces"
]

FEATURE_DESCRIPTIONS = {
    "hold_mean": "Average Key Hold Time",
    "hold_std": "Hold Time Consistency",
    "hold_min": "Minimum Key Press Duration",
    "hold_max": "Maximum Key Press Duration",
    "flight_mean": "Average Key Transition Speed",
    "flight_std": "Transition Speed Consistency",
    "flight_min": "Minimum Key Inter-arrival Time",
    "flight_max": "Maximum Key Inter-arrival Time",
    "total_duration": "Total Typing Duration",
    "backspaces": "Correction Rate"
}


def _safe_get_feature(obj, key, default=0.0):
    if obj is None:
        return default
    if isinstance(obj, dict):
        return float(obj.get(key, default))
    try:
        val = getattr(obj, key, default)
        return float(val) if val is not None else default
    except Exception:
        return default


class KeyShieldExplainer:
    def __init__(self, models_dir="backend/ml/models"):
        self.models_dir = models_dir
        self.rf_model = joblib.load(os.path.join(models_dir, "random_forest.pkl"))
        self.xgb_model = joblib.load(os.path.join(models_dir, "xgboost.pkl"))
        self.scaler = joblib.load(os.path.join(models_dir, "scaler.pkl"))
        self.rf_explainer = shap.TreeExplainer(self.rf_model)

    def explain_sample(self, features, profile=None):
        diff_vector = []
        for feat in FEATURE_NAMES:
            val = float(features.get(feat, 0.0))
            if profile:
                prof_val = _safe_get_feature(profile, feat, 0.0)
                std_key = feat.replace("mean", "std").replace("min", "std").replace("max", "std")
                std_val = _safe_get_feature(profile, std_key, 0.05)
                if std_val <= 0:
                    std_val = 0.05
                diff = abs(val - prof_val) / std_val
            else:
                diff = val
            diff_vector.append(diff)

        X_input = np.array([diff_vector])
        X_scaled = self.scaler.transform(X_input)

        raw_shap = self.rf_explainer.shap_values(X_scaled)
        if isinstance(raw_shap, list):
            shap_vals = raw_shap[1][0]
        elif isinstance(raw_shap, np.ndarray) and raw_shap.ndim == 3:
            shap_vals = raw_shap[0, :, 1]
        else:
            shap_vals = raw_shap[0]

        local_contributions = {}
        for feat, v in zip(FEATURE_NAMES, shap_vals):
            local_contributions[feat] = round(float(v), 4)

        sorted_feats = sorted(
            local_contributions.items(),
            key=lambda x: abs(x[1]),
            reverse=True
        )

        top_positive = [f for f, v in sorted_feats if v > 0][:2]
        top_negative = [f for f, v in sorted_feats if v < 0][:2]

        explanations_text = []
        if top_positive:
            pos_names = [FEATURE_DESCRIPTIONS.get(f, f) for f in top_positive]
            explanations_text.append(
                f"Strongest genuine biometrics indicators: {', '.join(pos_names)}."
            )
        if top_negative:
            neg_names = [FEATURE_DESCRIPTIONS.get(f, f) for f in top_negative]
            explanations_text.append(
                f"Primary deviation factors: {', '.join(neg_names)}."
            )

        text_summary = " ".join(explanations_text) if explanations_text else "Keystroke pattern closely matches baseline."

        global_importance = {}
        for feat, imp in zip(FEATURE_NAMES, self.rf_model.feature_importances_):
            global_importance[feat] = round(float(imp), 4)

        return {
            "global_importance": global_importance,
            "local_contributions": local_contributions,
            "text_explanation": text_summary,
            "strongest_model": "Random Forest Tree SHAP"
        }


_explainer_instance = None


def get_explainer():
    global _explainer_instance
    if _explainer_instance is None:
        _explainer_instance = KeyShieldExplainer()
    return _explainer_instance


def explain(features, profile=None):
    explainer = get_explainer()
    return explainer.explain_sample(features, profile)
