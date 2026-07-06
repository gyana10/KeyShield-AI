from etl.transform import DataTransformer

transformer = DataTransformer()

enrollment, authentication = transformer.split_dataset()

print()

print(enrollment.head())

print()

print(authentication.head())