from pathlib import Path
from datetime import datetime
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

        metadata = ["subject", "sessionIndex", "rep"]

        feature_columns = [
            c for c in df.columns
            if c not in metadata
        ]

        profiles = (
            df.groupby("subject")[feature_columns]
            .agg(["mean", "std", "median", "min", "max"])
        )

        profiles.columns = [
            f"{feature}_{stat}"
            for feature, stat in profiles.columns
        ]

        profiles.reset_index(inplace=True)

        profiles["samples_used"] = 250
        profiles["sessions_used"] = "1,2,3,4,5"
        profiles["profile_version"] = "v1"
        profiles["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        profiles.to_csv(self.output_path, index=False)

        print("=" * 60)
        print("Behavior Profiles Generated")
        print("=" * 60)
        print(f"Profiles : {profiles.shape}")

        return profiles