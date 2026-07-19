from backend.ml.stacking_ensemble import prepare_biometrics_dataset, StackingEnsemblePipeline


def main():
    print("=" * 60)
    print("KEYSHIELD AI - STACKING ENSEMBLE TRAINING")
    print("=" * 60)

    X, y = prepare_biometrics_dataset("data/processed/training_features.csv")
    print(f"Dataset Prepared: {X.shape[0]} samples, {X.shape[1]} features")

    pipeline = StackingEnsemblePipeline()
    metrics = pipeline.train_and_evaluate(X, y)

    print("=" * 60)
    print("STACKING ENSEMBLE TRAINING COMPLETE!")
    print("=" * 60)


if __name__ == "__main__":
    main()
