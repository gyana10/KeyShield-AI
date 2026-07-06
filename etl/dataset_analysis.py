import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "raw" / "DSL-StrongPasswordData.csv"

df = pd.read_csv(DATA_PATH)

print("=" * 60)
print("KEYSHIELD AI - DATASET ANALYSIS REPORT")
print("=" * 60)

print("\nUnique Users:")

print(df["subject"].nunique())

print("\nUsers:")

print(sorted(df["subject"].unique()))

print("\nSamples Per User:")

print(df["subject"].value_counts())

print("\nSessions:")

print(df["sessionIndex"].value_counts())

print("\nRepetitions:")

print(df["rep"].value_counts().sort_index())

print("\nDataset Statistics Completed.")