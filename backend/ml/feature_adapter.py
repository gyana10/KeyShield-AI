import numpy as np


def build_features(data):
    """
    Convert raw frontend keystroke data into the
    statistical features expected by the ML model.

    Frontend timings are in milliseconds.
    Training data is in seconds.
    """

    # Convert milliseconds -> seconds
    hold = np.array(
        data["holdTimes"],
        dtype=float
    ) / 1000.0

    flight = np.array(
        data["flightTimes"],
        dtype=float
    ) / 1000.0

    total_duration = float(data["totalDuration"]) / 1000.0

    return {
        "hold_mean": float(np.mean(hold)),
        "hold_std": float(np.std(hold)),
        "hold_min": float(np.min(hold)),
        "hold_max": float(np.max(hold)),

        "flight_mean": float(np.mean(flight)),
        "flight_std": float(np.std(flight)),
        "flight_min": float(np.min(flight)),
        "flight_max": float(np.max(flight)),

        "total_duration": total_duration,

        "backspaces": int(data["backspaces"])
    }