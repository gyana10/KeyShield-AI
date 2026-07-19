import numpy as np


class TriLayerFusionEngine:
    """
    Fuses predictions from:
    1. Stacking Ensemble Meta Learner (50% weight)
    2. Statistical Profile Similarity Engine (35% weight)
    3. Isolation Forest Anomaly Detection (15% weight)
    """

    @staticmethod
    def evaluate(ensemble_result, profile_result):
        ensemble_prob = float(ensemble_result.get("ensemble_probability", 0.5))
        anomaly_score = float(ensemble_result.get("anomaly_score", 0.0))

        # Convert Isolation Forest score to pseudo-probability [0, 1]
        anomaly_prob = float(1.0 / (1.0 + np.exp(-3.0 * anomaly_score)))

        # Profile similarity percentage -> [0, 1]
        similarity_pct = float(profile_result.get("similarity", 50.0))
        profile_prob = similarity_pct / 100.0

        # Weighted tri-layer fusion score
        final_score = (0.50 * ensemble_prob) + (0.35 * profile_prob) + (0.15 * anomaly_prob)
        final_score = max(0.0, min(1.0, final_score))

        # Decision Threshold
        if final_score >= 0.60:
            decision = "GENUINE"
        else:
            decision = "SUSPICIOUS"

        # Risk Classification
        if final_score >= 0.75:
            risk = "LOW"
        elif final_score >= 0.50:
            risk = "MEDIUM"
        else:
            risk = "HIGH"

        # Confidence percentage (distance from neutral threshold 0.5)
        confidence = round(abs(final_score - 0.5) * 200.0, 2)
        confidence = max(50.0, min(100.0, confidence))

        return {
            "decision": decision,
            "risk": risk,
            "final_score": round(final_score, 4),
            "probability": round(ensemble_prob, 4),
            "anomaly_score": round(anomaly_score, 4),
            "profile_similarity": round(similarity_pct, 2),
            "confidence_score": confidence,
            "model_contributions": ensemble_result.get("model_contributions", {}),
            "explanations": profile_result.get("explanations", [])
        }
