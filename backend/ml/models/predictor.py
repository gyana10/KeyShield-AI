import joblib
import pandas as pd

model = joblib.load(
    "backend/ml/models/isolation_forest.pkl"
)


def predict(features):

    df = pd.DataFrame([features])

    prediction = model.predict(df)[0]

    score = float(model.decision_function(df)[0])

    decision = "GENUINE"
    risk = "LOW"

    if prediction == -1:
        decision = "SUSPICIOUS"
        risk = "HIGH"

    return {

        "prediction": int(prediction),

        "decision": decision,

        "risk": risk,

        "anomaly_score": round(score, 4)

    }