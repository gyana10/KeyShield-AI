import json
import numpy as np


class ProfileBuilder:

    @staticmethod
    def build(enrollments):

        hold = []
        flight = []
        duration = []
        backspace = []

        for e in enrollments:

            hold.extend(json.loads(e.hold_times))
            flight.extend(json.loads(e.flight_times))

            duration.append(e.total_duration)
            backspace.append(e.backspaces)

        profile = {

            "hold_mean": float(np.mean(hold)),
            "hold_std": float(np.std(hold)),

            "flight_mean": float(np.mean(flight)),
            "flight_std": float(np.std(flight)),

            "duration_mean": float(np.mean(duration)),
            "duration_std": float(np.std(duration)),

            "backspace_mean": float(np.mean(backspace)),
            "backspace_std": float(np.std(backspace))

        }

        return profile