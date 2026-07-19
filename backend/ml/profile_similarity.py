import numpy as np


def calculate_similarity(profile, features):
    """
    Calculate similarity percentage (0-100%) between current keystroke sample and user profile.
    Uses continuous Gaussian/Z-score based decay curve:
    similarity_i = exp(-0.5 * z_score_i^2) * 100
    """
    scores = []
    explanations = []

    comparisons = [
        ("hold_mean", "Average Key Hold Time", getattr(profile, "hold_mean", 0.1), getattr(profile, "hold_std", 0.02)),
        ("hold_std", "Hold Time Consistency", getattr(profile, "hold_std", 0.02), max(getattr(profile, "hold_std", 0.02) * 0.5, 0.005)),
        ("flight_mean", "Average Transition Speed", getattr(profile, "flight_mean", 0.2), getattr(profile, "flight_std", 0.05)),
        ("flight_std", "Transition Consistency", getattr(profile, "flight_std", 0.05), max(getattr(profile, "flight_std", 0.05) * 0.5, 0.01)),
        ("total_duration", "Overall Typing Speed", getattr(profile, "total_duration", 3.0), max(getattr(profile, "total_duration", 3.0) * 0.2, 0.2)),
        ("backspaces", "Correction Behavior", getattr(profile, "backspaces", 0.0), 1.0)
    ]

    for feat_name, desc, prof_val, prof_std in comparisons:
        curr_val = float(features.get(feat_name, 0.0))
        std = float(prof_std) if float(prof_std) > 0 else 0.01

        # Z-score distance
        z_score = abs(curr_val - float(prof_val)) / std

        # Gaussian similarity curve
        sim = float(np.exp(-0.5 * (z_score ** 2)) * 100.0)
        sim = max(0.0, min(100.0, sim))

        scores.append(sim)
        explanations.append({
            "feature": feat_name,
            "description": desc,
            "expected": round(float(prof_val), 4),
            "current": round(curr_val, 4),
            "similarity": round(sim, 2)
        })

    overall_similarity = float(np.mean(scores))

    return {
        "similarity": round(overall_similarity, 2),
        "explanations": explanations
    }