import joblib
import pandas as pd

model = joblib.load(
    "backend/ml/models/isolation_forest.pkl"
)


def predict(sample):

    df = pd.DataFrame([sample])

    prediction = model.predict(df)[0]

    score = model.decision_function(df)[0]

    return {
        "prediction": int(prediction),
        "score": float(score)
    }