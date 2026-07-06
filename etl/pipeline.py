from etl.extract import DataExtractor
from etl.transform import DataTransformer
from etl.profile_builder import ProfileBuilder


def main():

    print("=" * 70)
    print("KEYSHIELD AI - ETL PIPELINE")
    print("=" * 70)

    # Step 1
    extractor = DataExtractor()
    df = extractor.load_dataset()

    print(f"\nDataset Loaded : {df.shape}")

    # Step 2
    transformer = DataTransformer()
    enrollment, authentication = transformer.split_dataset()

    # Step 3
    builder = ProfileBuilder()
    profiles = builder.build_profiles()

    print("\nETL Pipeline Completed Successfully!")

    print(f"Enrollment : {enrollment.shape}")

    print(f"Authentication : {authentication.shape}")

    print(f"Profiles : {profiles.shape}")


if __name__ == "__main__":
    main()