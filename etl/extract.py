"""
extract.py
-----------
Extracts the raw DSL keystroke dataset.

Author: Gyana Mohanty
Project: KeyShield AI
"""

from pathlib import Path
import pandas as pd


class DataExtractor:

    def __init__(self):

        self.base_dir = Path(__file__).resolve().parent.parent

        self.dataset_path = (
            self.base_dir
            / "data"
            / "raw"
            / "DSL-StrongPasswordData.csv"
        )

    def load_dataset(self):

        if not self.dataset_path.exists():

            raise FileNotFoundError(
                f"Dataset not found:\n{self.dataset_path}"
            )

        df = pd.read_csv(self.dataset_path)

        return df