import pandas as pd
import numpy as np
import os

# ----------------------------
# Load enrollment dataset
# ----------------------------
df = pd.read_csv("data/intermediate/enrollment.csv")

# Metadata columns
metadata = ["subject", "sessionIndex", "rep"]

# Hold Time columns
hold_cols = [c for c in df.columns if c.startswith("H.")]

# Flight Time columns
flight_cols = [c for c in df.columns if c.startswith("UD.")]

print("=" * 60)
print("Dataset Loaded:", df.shape)
print("Hold Columns :", len(hold_cols))
print("Flight Columns:", len(flight_cols))
print("=" * 60)

rows = []

for _, row in df.iterrows():

    hold = row[hold_cols].astype(float).values
    flight = row[flight_cols].astype(float).values

    features = {
        "subject": row["subject"],
        "sessionIndex": row["sessionIndex"],
        "rep": row["rep"],

        "hold_mean": np.mean(hold),
        "hold_std": np.std(hold),
        "hold_min": np.min(hold),
        "hold_max": np.max(hold),

        "flight_mean": np.mean(flight),
        "flight_std": np.std(flight),
        "flight_min": np.min(flight),
        "flight_max": np.max(flight),

        "total_duration": np.sum(hold) + np.sum(flight),

        # DSL dataset doesn't record backspaces
        "backspaces": 0
    }

    rows.append(features)

feature_df = pd.DataFrame(rows)

os.makedirs("data/processed", exist_ok=True)

feature_df.to_csv(
    "data/processed/training_features.csv",
    index=False
)

print("=" * 60)
print("Training Feature Dataset Created Successfully")
print(feature_df.shape)
print("=" * 60)

print(feature_df.head())