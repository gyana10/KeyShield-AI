import joblib
import pandas as pd

from sklearn.ensemble import IsolationForest

# Load enrollment data
df = pd.read_csv(
    "data/intermediate/enrollment.csv"
)

print(df.shape)

# Remove metadata columns
X = df.drop(
    columns=[
        "subject",
        "sessionIndex",
        "rep"
    ]
)

print("Training Features:", X.shape)

model = IsolationForest(
    n_estimators=200,
    contamination=0.02,
    random_state=42
)

model.fit(X)

joblib.dump(
    model,
    "backend/ml/models/isolation_forest.pkl"
)

print("=" * 60)
print("Model Trained Successfully")
print("=" * 60)