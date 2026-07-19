import os
import joblib
import numpy as np
import pandas as pd


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


class StackingEnsemblePredictor:
    def __init__(self, models_dir="backend/ml/models"):
        self.models_dir = models_dir
        self.scaler = joblib.load(os.path.join(models_dir, "scaler.pkl"))
        self.iso_forest = joblib.load(os.path.join(models_dir, "isolation_forest.pkl"))
        self.rf = joblib.load(os.path.join(models_dir, "random_forest.pkl"))
        self.xgb = joblib.load(os.path.join(models_dir, "xgboost.pkl"))
        self.lgb = joblib.load(os.path.join(models_dir, "lightgbm.pkl"))
        self.meta_learner = joblib.load(os.path.join(models_dir, "meta_learner.pkl"))

    def _convert_if_score_to_prob(self, scores):
        return float(1.0 / (1.0 + np.exp(-3.0 * scores[0])))

    def predict(self, current_features, profile_dict=None):
        """
        Predict genuine vs suspicious biometrics.
        If profile_dict is provided, compute feature differences relative to baseline.
        Otherwise compute normalized differences against defaults.
        """
        diff_vector = []
        for feat in FEATURE_NAMES:
            val = float(current_features.get(feat, 0.0))
            if profile_dict and feat in profile_dict:
                prof_val = float(profile_dict[feat])
                std_val = float(profile_dict.get(feat.replace("mean", "std"), 0.05))
                if std_val <= 0:
                    std_val = 0.05
                diff = abs(val - prof_val) / std_val
            else:
                diff = val
            diff_vector.append(diff)

        X_input = np.array([diff_vector])
        X_scaled = self.scaler.transform(X_input)

        # Base model probabilities
        if_score = float(self.iso_forest.decision_function(X_scaled)[0])
        if_prob = self._convert_if_score_to_prob(np.array([if_score]))

        rf_prob = float(self.rf.predict_proba(X_scaled)[0, 1])
        xgb_prob = float(self.xgb.predict_proba(X_scaled)[0, 1])
        lgb_prob = float(self.lgb.predict_proba(X_scaled)[0, 1])

        meta_input = np.array([[if_prob, rf_prob, xgb_prob, lgb_prob]])
        ensemble_prob = float(self.meta_learner.predict_proba(meta_input)[0, 1])

        # Get weights from Logistic Regression coefficients
        coefs = self.meta_learner.coef_[0]
        abs_coefs = np.abs(coefs)
        total_weight = float(np.sum(abs_coefs)) + 1e-5
        weights = (abs_coefs / total_weight).tolist()

        contributions = {
            "Isolation Forest": {
                "probability": round(if_prob, 4),
                "anomaly_score": round(if_score, 4),
                "weight": round(weights[0], 4)
            },
            "Random Forest": {
                "probability": round(rf_prob, 4),
                "weight": round(weights[1], 4)
            },
            "XGBoost": {
                "probability": round(xgb_prob, 4),
                "weight": round(weights[2], 4)
            },
            "LightGBM": {
                "probability": round(lgb_prob, 4),
                "weight": round(weights[3], 4)
            }
        }

        return {
            "ensemble_probability": round(ensemble_prob, 4),
            "anomaly_score": round(if_score, 4),
            "model_contributions": contributions,
            "feature_diff_vector": diff_vector
        }


# Global singleton predictor instance
_predictor_instance = None


def get_predictor():
    global _predictor_instance
    if _predictor_instance is None:
        _predictor_instance = StackingEnsemblePredictor()
    return _predictor_instance


def predict(features, profile=None):
    predictor = get_predictor()
    profile_dict = None
    if profile:
        profile_dict = {
            "hold_mean": profile.hold_mean,
            "hold_std": profile.hold_std,
            "flight_mean": profile.flight_mean,
            "flight_std": profile.flight_std,
            "total_duration": profile.total_duration,
            "backspaces": profile.backspaces
        }
    return predictor.predict(features, profile_dict)
