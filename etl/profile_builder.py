from pathlib import Path
from datetime import datetime
import pandas as pd


class ProfileBuilder:

    def __init__(self):
        self.base_dir = Path(__file__).resolve().parent.parent

        self.input_path = (
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

        df = pd.read_csv(self.input_path)

        metadata = ["subject", "sessionIndex", "rep"]

        features = [c for c in df.columns if c not in metadata]

        profiles = (
            df.groupby("subject")[features]
            .agg(["mean", "std", "min", "max", "median"])
        )

        profiles.columns = [
            f"{feature}_{stat}"
            for feature, stat in profiles.columns
        ]

        profiles.reset_index(inplace=True)

        # ---------- Metadata ----------

        sample_count = df.groupby("subject").size()

        profiles["samples_used"] = profiles["subject"].map(sample_count)

        profiles["sessions_used"] = "1,2,3,4,5"

        profiles["profile_version"] = "v1"

        profiles["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        profiles.to_csv(self.output_path, index=False)

        print("=" * 60)
        print("Behavior Profiles Generated Successfully")
        print("=" * 60)
        print(f"Profiles : {profiles.shape}")

        return profiles