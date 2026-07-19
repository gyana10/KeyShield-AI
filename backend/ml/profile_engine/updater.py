from datetime import datetime
import numpy as np


class ProfileUpdater:
    ALPHA = 0.1  # Exponential moving average factor

    @staticmethod
    def update_profile(profile_model, new_features, confidence_score, decision):
        """
        Adaptive profile update.
        Only updates when decision is GENUINE and confidence >= 75.0%.
        """
        if decision != "GENUINE" or confidence_score < 75.0:
            return False, profile_model.drift_score

        # Apply EMA to update profile baselines
        alpha = ProfileUpdater.ALPHA

        old_hold = profile_model.hold_mean
        new_hold = new_features["hold_mean"]
        profile_model.hold_mean = float((1 - alpha) * old_hold + alpha * new_hold)

        old_flight = profile_model.flight_mean
        new_flight = new_features["flight_mean"]
        profile_model.flight_mean = float((1 - alpha) * old_flight + alpha * new_flight)

        old_dur = profile_model.total_duration
        new_dur = new_features["total_duration"]
        profile_model.total_duration = float((1 - alpha) * old_dur + alpha * new_dur)

        old_bs = profile_model.backspaces
        new_bs = new_features["backspaces"]
        profile_model.backspaces = float((1 - alpha) * old_bs + alpha * new_bs)

        # Update last_updated timestamp
        profile_model.last_updated = datetime.utcnow()

        # Calculate behavior drift score: normalized shift between old vs new
        shift = (
            abs(new_hold - old_hold) / (profile_model.hold_std + 1e-4) +
            abs(new_flight - old_flight) / (profile_model.flight_std + 1e-4)
        ) / 2.0

        # Exponentially decay old drift score and add new shift
        drift = float(0.85 * (profile_model.drift_score or 0.0) + 0.15 * shift)
        profile_model.drift_score = round(drift, 4)

        return True, profile_model.drift_score
