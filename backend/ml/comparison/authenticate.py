from backend.ml.comparison.distance import (
    euclidean,
    similarity
)


def authenticate(profile, sample):

    distance = euclidean(

        profile,

        sample

    )

    score = similarity(

        distance

    )

    if score >= 85:

        decision = "GENUINE"

    elif score >= 70:

        decision = "SUSPICIOUS"

    else:

        decision = "IMPOSTER"

    return {

        "distance": round(distance, 2),

        "similarity": round(score, 2),

        "decision": decision

    }