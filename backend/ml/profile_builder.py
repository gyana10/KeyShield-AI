from backend.ml.feature_adapter import build_features


def create_profile(data):
    """
    Create a user behavioral profile
    from a single enrollment sample.
    """

    features = build_features(data)

    return {
        "hold_mean": features["hold_mean"],
        "hold_std": features["hold_std"],

        "flight_mean": features["flight_mean"],
        "flight_std": features["flight_std"],

        "total_duration": features["total_duration"],

        "backspaces": features["backspaces"]
    }