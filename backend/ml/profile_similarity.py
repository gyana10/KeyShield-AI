def calculate_similarity(profile, features):

    scores = []

    explanations = []

    comparisons = {
        "hold_mean": "Average key hold time",
        "hold_std": "Hold time consistency",
        "flight_mean": "Average transition speed",
        "flight_std": "Transition consistency",
        "total_duration": "Overall typing speed",
        "backspaces": "Correction behavior"
    }

    for feature in comparisons:

        profile_value = getattr(profile, feature)

        current_value = features[feature]

        if profile_value == 0:
            similarity = 100
        else:
            difference = abs(
                current_value - profile_value
            ) / abs(profile_value)

            similarity = max(
                0,
                100 - (difference * 100)
            )

        scores.append(similarity)

        explanations.append({
            "feature": feature,
            "description": comparisons[feature],
            "expected": round(profile_value, 4),
            "current": round(current_value, 4),
            "similarity": round(similarity, 2)
        })

    overall_similarity = sum(scores) / len(scores)

    return {
        "similarity": round(
            overall_similarity,
            2
        ),
        "explanations": explanations
    }