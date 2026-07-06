from pathlib import Path
import pandas as pd
import random


class AuthenticationGenerator:

    def __init__(self):

        self.base_dir = Path(__file__).resolve().parent.parent

        self.auth_path = (
            self.base_dir /
            "data" /
            "intermediate" /
            "authentication.csv"
        )

        self.output_path = (
            self.base_dir /
            "data" /
            "processed" /
            "authentication_dataset.csv"
        )

    def generate_dataset(self):

        df = pd.read_csv(self.auth_path)

        authentication_records = []

        users = sorted(df["subject"].unique())

        random.seed(42)

        for _, row in df.iterrows():

            actual_user = row["subject"]

            # ---------- Genuine ----------
            genuine = row.copy()

            genuine["claimed_user"] = actual_user

            genuine["actual_user"] = actual_user

            genuine["label"] = 1

            authentication_records.append(genuine)

            # ---------- Impostor ----------

            impostor = row.copy()

            fake_user = random.choice(
                [u for u in users if u != actual_user]
            )

            impostor["claimed_user"] = fake_user

            impostor["actual_user"] = actual_user

            impostor["label"] = 0

            authentication_records.append(impostor)

        authentication_df = pd.DataFrame(authentication_records)

        authentication_df.to_csv(self.output_path, index=False)

        print("=" * 60)
        print("Authentication Dataset Created")
        print("=" * 60)

        print(authentication_df.shape)

        return authentication_df