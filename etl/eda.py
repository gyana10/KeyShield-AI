import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "raw" / "DSL-StrongPasswordData.csv"

print("=" * 60)
print("KEYSHIELD AI - DATASET ANALYSIS")
print("=" * 60)

print("\nDataset Path:")
print(DATA_PATH)

print("\nExists:", DATA_PATH.exists())

df = pd.read_csv(DATA_PATH)

print("\nDataset Loaded Successfully!")

print("\nShape:")
print(df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nFirst Five Rows:")
print(df.head())

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Rows:")
print(df.duplicated().sum())