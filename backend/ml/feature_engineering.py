import math
import numpy as np

# 17 Statistical Feature Names
FEATURE_NAMES = [
    "hold_mean", "hold_std", "hold_min", "hold_max", "hold_median",
    "flight_mean", "flight_std", "flight_min", "flight_max", "flight_median",
    "typing_duration", "backspaces", "typing_speed", "pause_count",
    "rhythm_score", "keystroke_variance", "transition_variance"
]


def extract_keystroke_features(raw_events: list) -> dict:
    """
    Extracts 17 statistical features from raw keydown/keyup timing events.
    raw_events: list of dicts [{"key": str, "type": "keydown"|"keyup", "time": float}]
    """
    if not raw_events or len(raw_events) < 2:
        # Fallback default zero-feature vector
        return {feat: 0.0 for feat in FEATURE_NAMES}

    # Sort events by timestamp
    events = sorted(raw_events, key=lambda x: x.get("time", 0))
    start_time = events[0].get("time", 0)
    end_time = events[-1].get("time", 0)
    typing_duration = max(0.1, (end_time - start_time) / 1000.0) # in seconds

    holds = []
    flights = []
    backspaces = 0
    keydown_times = {}

    prev_keyup_time = None

    for ev in events:
        key = ev.get("key")
        ev_type = ev.get("type")
        t = ev.get("time", 0)

        if key == "Backspace" and ev_type == "keydown":
            backspaces += 1

        if ev_type == "keydown":
            keydown_times[key] = t
            if prev_keyup_time is not None:
                flight = t - prev_keyup_time
                if 0 <= flight <= 2000: # filter extreme outliers > 2s
                    flights.append(flight)
        elif ev_type == "keyup":
            if key in keydown_times:
                hold = t - keydown_times[key]
                if 0 <= hold <= 2000: # filter extreme outliers
                    holds.append(hold)
                del keydown_times[key]
            prev_keyup_time = t

    # Statistical Aggregations for Holds
    if holds:
        hold_mean = float(np.mean(holds))
        hold_std = float(np.std(holds)) if len(holds) > 1 else 0.0
        hold_min = float(np.min(holds))
        hold_max = float(np.max(holds))
        hold_median = float(np.median(holds))
        keystroke_var = float(np.var(holds))
    else:
        hold_mean = hold_std = hold_min = hold_max = hold_median = keystroke_var = 110.0

    # Statistical Aggregations for Flights
    if flights:
        flight_mean = float(np.mean(flights))
        flight_std = float(np.std(flights)) if len(flights) > 1 else 0.0
        flight_min = float(np.min(flights))
        flight_max = float(np.max(flights))
        flight_median = float(np.median(flights))
        transition_var = float(np.var(flights))
        pause_count = sum(1 for f in flights if f > 300)
    else:
        flight_mean = flight_std = flight_min = flight_max = flight_median = transition_var = 140.0
        pause_count = 0

    total_keys = len([e for e in events if e.get("type") == "keydown"])
    typing_speed = (total_keys / typing_duration) * 60.0 # keys per minute

    # Rhythm score based on timing stability (lower variance = higher rhythm stability)
    rhythm_score = float(max(0.0, 100.0 - (hold_std + flight_std) / 2.0))

    return {
        "hold_mean": round(hold_mean, 2),
        "hold_std": round(hold_std, 2),
        "hold_min": round(hold_min, 2),
        "hold_max": round(hold_max, 2),
        "hold_median": round(hold_median, 2),
        "flight_mean": round(flight_mean, 2),
        "flight_std": round(flight_std, 2),
        "flight_min": round(flight_min, 2),
        "flight_max": round(flight_max, 2),
        "flight_median": round(flight_median, 2),
        "typing_duration": round(typing_duration, 2),
        "backspaces": float(backspaces),
        "typing_speed": round(typing_speed, 2),
        "pause_count": float(pause_count),
        "rhythm_score": round(rhythm_score, 2),
        "keystroke_variance": round(keystroke_var, 2),
        "transition_variance": round(transition_var, 2)
    }


def create_behavioral_profile(five_sample_feature_dicts: list) -> dict:
    """
    Creates ONE user behavioral profile from 5 enrollment sample feature vectors.
    Calculates mean, median, std, min, max for each of the 17 features.
    """
    profile = {}
    for feat in FEATURE_NAMES:
        values = [s[feat] for s in five_sample_feature_dicts if feat in s]
        if not values:
            values = [0.0]

        profile[feat] = {
            "mean": round(float(np.mean(values)), 2),
            "median": round(float(np.median(values)), 2),
            "std": round(float(np.std(values)) if len(values) > 1 else 1.0, 2),
            "min": round(float(np.min(values)), 2),
            "max": round(float(np.max(values)), 2)
        }
    return profile


def calculate_profile_similarity(verification_features: dict, behavioral_profile: dict) -> dict:
    """
    Compares verification feature vector against stored behavioral profile (Stage 1).
    Returns feature-by-feature breakdown and overall similarity score.
    """
    feature_similarities = {}
    sim_scores = []

    for feat in FEATURE_NAMES:
        curr = verification_features.get(feat, 0.0)
        prof_stat = behavioral_profile.get(feat, {"mean": curr, "std": 1.0})
        exp_mean = prof_stat.get("mean", curr)
        exp_std = max(1.0, prof_stat.get("std", 1.0))

        diff = abs(curr - exp_mean)
        # Z-score based similarity: 0 diff = 100%, 3 std diff = 0%
        z_score = diff / exp_std
        similarity_pct = max(0.0, min(100.0, 100.0 * (1.0 - (z_score / 3.0))))

        feature_similarities[feat] = {
            "expected": exp_mean,
            "current": curr,
            "difference": round(diff, 2),
            "similarity": round(similarity_pct, 1)
        }
        sim_scores.append(similarity_pct)

    overall_similarity = float(np.mean(sim_scores)) if sim_scores else 95.0
    return {
        "overall_similarity": round(overall_similarity, 1),
        "feature_breakdown": feature_similarities
    }


def update_profile_ema(current_profile: dict, verification_features: dict, alpha: float = 0.1) -> dict:
    """
    Updates stored profile using Exponential Moving Average (EMA) when authenticated as genuine.
    """
    updated_profile = {}
    for feat in FEATURE_NAMES:
        curr_val = verification_features.get(feat, 0.0)
        prof_stat = current_profile.get(feat, {"mean": curr_val, "median": curr_val, "std": 1.0, "min": curr_val, "max": curr_val})

        old_mean = prof_stat.get("mean", curr_val)
        new_mean = (1 - alpha) * old_mean + alpha * curr_val

        updated_profile[feat] = {
            "mean": round(float(new_mean), 2),
            "median": prof_stat.get("median", new_mean),
            "std": prof_stat.get("std", 1.0),
            "min": round(min(prof_stat.get("min", curr_val), curr_val), 2),
            "max": round(max(prof_stat.get("max", curr_val), curr_val), 2)
        }
    return updated_profile
