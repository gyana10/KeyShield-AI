import pandas as pd

from backend.ml.models.predictor import predict

df = pd.read_csv(
    "data/processed/training_features.csv"
)

sample = df.iloc[0]

sample = sample.drop(

    [
        "subject",
        "sessionIndex",
        "rep"
    ]

)

print(

    predict(

        sample.to_dict()

    )

)