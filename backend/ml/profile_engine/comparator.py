import math


class Comparator:

    @staticmethod
    def compare(profile, sample):

        score = 0

        if abs(sample["hold_mean"] - profile["hold_mean"]) <= profile["hold_std"]:

            score += 25

        if abs(sample["flight_mean"] - profile["flight_mean"]) <= profile["flight_std"]:

            score += 25

        if abs(sample["duration_mean"] - profile["duration_mean"]) <= profile["duration_std"]:

            score += 25

        if abs(sample["backspace_mean"] - profile["backspace_mean"]) <= max(profile["backspace_std"], 1):

            score += 25

        return score