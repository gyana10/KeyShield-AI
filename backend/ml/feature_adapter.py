import numpy as np


def build_features(data):

    hold = np.array(data["holdTimes"], dtype=float)
    flight = np.array(data["flightTimes"], dtype=float)

    return {

        "hold_mean": float(np.mean(hold)),
        "hold_std": float(np.std(hold)),
        "hold_min": float(np.min(hold)),
        "hold_max": float(np.max(hold)),

        "flight_mean": float(np.mean(flight)),
        "flight_std": float(np.std(flight)),
        "flight_min": float(np.min(flight)),
        "flight_max": float(np.max(flight)),

        "total_duration": float(data["totalDuration"]),

        "backspaces": int(data["backspaces"])

    }