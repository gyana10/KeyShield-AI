import math


def euclidean(profile, sample):

    return math.sqrt(

        (profile["avg_hold_time"] - sample["avg_hold_time"]) ** 2 +

        (profile["avg_flight_time"] - sample["avg_flight_time"]) ** 2 +

        (profile["avg_duration"] - sample["avg_duration"]) ** 2 +

        (profile["avg_backspaces"] - sample["avg_backspaces"]) ** 2

    )


def similarity(distance):

    return max(

        0,

        100 - distance / 20

    )