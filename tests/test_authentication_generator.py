from etl.authentication_generator import AuthenticationGenerator

generator = AuthenticationGenerator()

df = generator.generate_dataset()

print()

print(df.head())

print()

print(df["label"].value_counts())