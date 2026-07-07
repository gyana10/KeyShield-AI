import pandas as pd

from backend.ml.models.predictor import predict

df = pd.read_csv(
    "data/intermediate/authentication.csv"
)

sample = df.iloc[0]

sample = sample.drop(
    [
        "subject",
        "sessionIndex",
        "rep"
    ]
)

result = predict(sample.to_dict())

print(result)