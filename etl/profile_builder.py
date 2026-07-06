"""
profile_builder.py
------------------
Builds behavioral profiles from enrollment data.
"""

from pathlib import Path
import pandas as pd


class ProfileBuilder:

    def __init__(self):

        self.base_dir = Path(__file__).resolve().parent.parent

        self.enrollment_path = (
            self.base_dir /
            "data" /
            "intermediate" /
            "enrollment.csv"
        )

        self.output_path = (
            self.base_dir /
            "data" /
            "profiles" /
            "user_profiles.csv"
        )

    def build_profiles(self):

        df = pd.read_csv(self.enrollment_path)

        # Metadata columns
        metadata = ["subject", "sessionIndex", "rep"]

        # Timing Features
        feature_cols = [
            col for col in df.columns
            if col not in metadata
        ]

        profiles = (
            df.groupby("subject")[feature_cols]
            .agg(["mean", "std", "min", "max", "median"])
        )

        profiles.columns = [
            f"{feature}_{stat}"
            for feature, stat in profiles.columns
        ]

        profiles.reset_index(inplace=True)

        profiles.to_csv(self.output_path, index=False)

        print("=" * 60)
        print("Behavior Profiles Created Successfully")
        print("=" * 60)

        print()

        print("Profiles Shape:", profiles.shape)

        return profiles