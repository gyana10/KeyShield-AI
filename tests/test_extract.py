from etl.extract import DataExtractor

extractor = DataExtractor()

df = extractor.load_dataset()

print(df.head())

print()

print(df.shape)