"""
transform.py
-------------
Splits the DSL dataset into Enrollment and Authentication datasets.
"""

from pathlib import Path
import pandas as pd

from etl.extract import DataExtractor


class DataTransformer:

    def __init__(self):

        self.extractor = DataExtractor()

        self.base_dir = Path(__file__).resolve().parent.parent

        self.output_dir = self.base_dir / "data" / "intermediate"

    def split_dataset(self):

        df = self.extractor.load_dataset()

        enrollment_df = df[df["sessionIndex"].isin([1, 2, 3, 4, 5])]

        authentication_df = df[df["sessionIndex"].isin([6, 7, 8])]

        enrollment_path = self.output_dir / "enrollment.csv"

        authentication_path = self.output_dir / "authentication.csv"

        enrollment_df.to_csv(enrollment_path, index=False)

        authentication_df.to_csv(authentication_path, index=False)

        print("=" * 50)
        print("Dataset Split Completed")
        print("=" * 50)

        print(f"\nEnrollment Shape : {enrollment_df.shape}")

        print(f"Authentication Shape : {authentication_df.shape}")

        return enrollment_df, authentication_df