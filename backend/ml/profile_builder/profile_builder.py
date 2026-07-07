import json


def build_profile(enrollments):

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

        "avg_hold_time":

            sum(hold) / len(hold),

        "avg_flight_time":

            sum(flight) / len(flight),

        "avg_duration":

            sum(duration) / len(duration),

        "avg_backspaces":

            sum(backspace) / len(backspace)

    }

    return profile