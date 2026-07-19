import json
import numpy as np


class ProfileBuilder:
    @staticmethod
    def build_from_enrollments(enrollments):
        """
        Build user behavioral profile baseline from multiple Enrollment records.
        """
        all_holds = []
        all_flights = []
        durations = []
        backspaces = []

        for e in enrollments:
            h_times = json.loads(e.hold_times) if isinstance(e.hold_times, str) else e.hold_times
            f_times = json.loads(e.flight_times) if isinstance(e.flight_times, str) else e.flight_times

            # Timings in frontend are ms -> convert to seconds
            all_holds.extend([float(h) / 1000.0 if h > 1.0 else float(h) for h in h_times])
            all_flights.extend([float(f) / 1000.0 if abs(f) > 1.0 else float(f) for f in f_times])
            durations.append(float(e.total_duration) / 1000.0 if e.total_duration > 5.0 else float(e.total_duration))
            backspaces.append(float(e.backspaces))

        hold_mean = float(np.mean(all_holds)) if all_holds else 0.1
        hold_std = max(float(np.std(all_holds)), 0.01) if all_holds else 0.02

        flight_mean = float(np.mean(all_flights)) if all_flights else 0.2
        flight_std = max(float(np.std(all_flights)), 0.01) if all_flights else 0.05

        total_duration = float(np.mean(durations)) if durations else 3.0
        avg_backspaces = float(np.mean(backspaces)) if backspaces else 0.0

        return {
            "hold_mean": round(hold_mean, 4),
            "hold_std": round(hold_std, 4),
            "flight_mean": round(flight_mean, 4),
            "flight_std": round(flight_std, 4),
            "total_duration": round(total_duration, 4),
            "backspaces": round(avg_backspaces, 2)
        }