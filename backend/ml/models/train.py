import joblib
import pandas as pd

from sklearn.ensemble import IsolationForest

print("=" * 60)
print("Loading Statistical Feature Dataset")
print("=" * 60)

df = pd.read_csv(
    "data/processed/training_features.csv"
)

print(df.shape)

# Remove metadata
X = df.drop(
    columns=[
        "subject",
        "sessionIndex",
        "rep"
    ]
)

print("Training Shape:", X.shape)

model = IsolationForest(

    n_estimators=300,

    contamination=0.02,

    random_state=42

)

model.fit(X)

joblib.dump(

    model,

    "backend/ml/models/isolation_forest.pkl"

)

print("=" * 60)
print("NEW MODEL TRAINED SUCCESSFULLY")
print("=" * 60)