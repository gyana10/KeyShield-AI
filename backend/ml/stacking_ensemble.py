import os
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold, train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    roc_curve
)
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier


FEATURE_NAMES = [
    "hold_mean",
    "hold_std",
    "hold_min",
    "hold_max",
    "flight_mean",
    "flight_std",
    "flight_min",
    "flight_max",
    "total_duration",
    "backspaces"
]


def calculate_eer(y_true, y_scores):
    """
    Calculate Equal Error Rate (EER) where FAR == FRR.
    """
    fpr, tpr, thresholds = roc_curve(y_true, y_scores, pos_label=1)
    fnr = 1 - tpr
    eer_threshold_idx = np.nanargmin(np.absolute(fnr - fpr))
    eer = (fpr[eer_threshold_idx] + fnr[eer_threshold_idx]) / 2.0
    return float(eer)


def compute_metrics(y_true, y_pred, y_prob):
    """
    Compute comprehensive evaluation metrics.
    """
    acc = float(accuracy_score(y_true, y_pred))
    prec = float(precision_score(y_true, y_pred, zero_division=0))
    rec = float(recall_score(y_true, y_pred, zero_division=0))
    f1 = float(f1_score(y_true, y_pred, zero_division=0))
    try:
        auc = float(roc_auc_score(y_true, y_prob))
        eer = calculate_eer(y_true, y_prob)
    except Exception:
        auc = 0.5
        eer = 0.5

    return {
        "accuracy": round(acc, 4),
        "precision": round(prec, 4),
        "recall": round(rec, 4),
        "f1_score": round(f1, 4),
        "roc_auc": round(auc, 4),
        "eer": round(eer, 4)
    }


def prepare_biometrics_dataset(csv_path="data/processed/training_features.csv"):
    """
    Construct a universal biometric pairwise difference dataset.
    For each subject, genuine pairs (y=1) use subject's own samples.
    Impostor pairs (y=0) compare subject's profile with samples from other subjects.
    """
    df = pd.read_csv(csv_path)
    subjects = df["subject"].unique()

    X_list = []
    y_list = []

    for subj in subjects:
        subj_df = df[df["subject"] == subj][FEATURE_NAMES]
        if len(subj_df) < 5:
            continue

        subj_mean = subj_df.mean().values
        subj_std = subj_df.std().values + 1e-5

        # Genuine samples (y=1)
        for _, row in subj_df.iterrows():
            sample = row.values
            diff = np.abs(sample - subj_mean) / subj_std
            X_list.append(diff)
            y_list.append(1)

        # Impostor samples (y=0) from other subjects
        other_df = df[df["subject"] != subj][FEATURE_NAMES].sample(
            n=min(len(subj_df), 50), random_state=42
        )
        for _, row in other_df.iterrows():
            sample = row.values
            diff = np.abs(sample - subj_mean) / subj_std
            X_list.append(diff)
            y_list.append(0)

    X = np.array(X_list)
    y = np.array(y_list)

    return X, y


class StackingEnsemblePipeline:
    def __init__(self, models_dir="backend/ml/models"):
        self.models_dir = models_dir
        os.makedirs(self.models_dir, exist_ok=True)

        self.scaler = StandardScaler()
        self.iso_forest = IsolationForest(n_estimators=200, contamination=0.1, random_state=42)
        self.rf = RandomForestClassifier(n_estimators=150, max_depth=8, random_state=42)
        self.xgb = XGBClassifier(n_estimators=150, max_depth=6, learning_rate=0.08, random_state=42, eval_metric="logloss")
        self.lgb = LGBMClassifier(n_estimators=150, max_depth=6, learning_rate=0.08, random_state=42, verbose=-1)
        self.meta_learner = LogisticRegression(C=1.0, random_state=42)

    def _convert_if_score_to_prob(self, scores):
        """
        Convert Isolation Forest decision function scores to pseudo-probabilities [0, 1].
        Higher decision function score => more genuine => higher probability.
        """
        # Sigmoidal normalization centered at 0
        return 1.0 / (1.0 + np.exp(-3.0 * scores))

    def train_and_evaluate(self, X, y):
        print("=" * 60)
        print("Training Stacking Ensemble with 5-Fold OOF Cross Validation...")
        print("=" * 60)

        # 1. Train / Test Split (80% train, 20% test)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )

        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)

        # 2. Out-of-Fold (OOF) matrix setup (4 base models)
        oof_preds = np.zeros((len(X_train_scaled), 4))
        skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

        for fold, (train_idx, val_idx) in enumerate(skf.split(X_train_scaled, y_train)):
            X_tr, y_tr = X_train_scaled[train_idx], y_train[train_idx]
            X_va, y_va = X_train_scaled[val_idx], y_train[val_idx]

            # Fit fold models
            if_fold = IsolationForest(n_estimators=200, contamination=0.1, random_state=42)
            rf_fold = RandomForestClassifier(n_estimators=150, max_depth=8, random_state=42)
            xgb_fold = XGBClassifier(n_estimators=150, max_depth=6, learning_rate=0.08, random_state=42, eval_metric="logloss")
            lgb_fold = LGBMClassifier(n_estimators=150, max_depth=6, learning_rate=0.08, random_state=42, verbose=-1)

            if_fold.fit(X_tr)
            rf_fold.fit(X_tr, y_tr)
            xgb_fold.fit(X_tr, y_tr)
            lgb_fold.fit(X_tr, y_tr)

            # Predict on validation fold
            if_val_scores = if_fold.decision_function(X_va)
            if_val_prob = self._convert_if_score_to_prob(if_val_scores)
            rf_val_prob = rf_fold.predict_proba(X_va)[:, 1]
            xgb_val_prob = xgb_fold.predict_proba(X_va)[:, 1]
            lgb_val_prob = lgb_fold.predict_proba(X_va)[:, 1]

            oof_preds[val_idx, 0] = if_val_prob
            oof_preds[val_idx, 1] = rf_val_prob
            oof_preds[val_idx, 2] = xgb_val_prob
            oof_preds[val_idx, 3] = lgb_val_prob

        # 3. Train Meta Learner on OOF predictions
        print("Training Meta Learner (Logistic Regression)...")
        self.meta_learner.fit(oof_preds, y_train)

        # 4. Refit base models on full training set
        print("Refitting Base Models on Full Training Set...")
        self.iso_forest.fit(X_train_scaled)
        self.rf.fit(X_train_scaled, y_train)
        self.xgb.fit(X_train_scaled, y_train)
        self.lgb.fit(X_train_scaled, y_train)

        # 5. Evaluate Base Models and Meta Learner on Test set
        print("Evaluating Models on Held-Out Test Set...")
        if_test_score = self.iso_forest.decision_function(X_test_scaled)
        if_test_prob = self._convert_if_score_to_prob(if_test_score)
        if_test_pred = (if_test_prob >= 0.5).astype(int)

        rf_test_prob = self.rf.predict_proba(X_test_scaled)[:, 1]
        rf_test_pred = (rf_test_prob >= 0.5).astype(int)

        xgb_test_prob = self.xgb.predict_proba(X_test_scaled)[:, 1]
        xgb_test_pred = (xgb_test_prob >= 0.5).astype(int)

        lgb_test_prob = self.lgb.predict_proba(X_test_scaled)[:, 1]
        lgb_test_pred = (lgb_test_prob >= 0.5).astype(int)

        test_meta_input = np.column_stack([if_test_prob, rf_test_prob, xgb_test_prob, lgb_test_prob])
        stacking_prob = self.meta_learner.predict_proba(test_meta_input)[:, 1]
        stacking_pred = (stacking_prob >= 0.5).astype(int)

        # Compute metrics
        metrics = {
            "Isolation Forest": compute_metrics(y_test, if_test_pred, if_test_prob),
            "Random Forest": compute_metrics(y_test, rf_test_pred, rf_test_prob),
            "XGBoost": compute_metrics(y_test, xgb_test_pred, xgb_test_prob),
            "LightGBM": compute_metrics(y_test, lgb_test_pred, lgb_test_prob),
            "Stacking Ensemble": compute_metrics(y_test, stacking_pred, stacking_prob)
        }

        # Format metrics array for frontend GET /model-info comparison chart
        metrics_list = []
        for name, m in metrics.items():
            metrics_list.append({
                "model_name": name,
                **m
            })

        print("\nModel Comparison Results:")
        print(pd.DataFrame(metrics_list))

        # 6. Save models and metrics
        joblib.dump(self.scaler, os.path.join(self.models_dir, "scaler.pkl"))
        joblib.dump(self.iso_forest, os.path.join(self.models_dir, "isolation_forest.pkl"))
        joblib.dump(self.rf, os.path.join(self.models_dir, "random_forest.pkl"))
        joblib.dump(self.xgb, os.path.join(self.models_dir, "xgboost.pkl"))
        joblib.dump(self.lgb, os.path.join(self.models_dir, "lightgbm.pkl"))
        joblib.dump(self.meta_learner, os.path.join(self.models_dir, "meta_learner.pkl"))

        metrics_payload = {
            "architecture": "Stacking Ensemble (Isolation Forest + RF + XGBoost + LightGBM -> Logistic Regression)",
            "base_models": ["Isolation Forest", "Random Forest", "XGBoost", "LightGBM"],
            "meta_learner": "Logistic Regression",
            "features": FEATURE_NAMES,
            "metrics": metrics_list
        }

        with open(os.path.join(self.models_dir, "model_metrics.json"), "w") as f:
            json.dump(metrics_payload, f, indent=4)

        print("\nAll models and metrics saved successfully to:", self.models_dir)
        return metrics_payload


if __name__ == "__main__":
    X, y = prepare_biometrics_dataset()
    pipeline = StackingEnsemblePipeline()
    pipeline.train_and_evaluate(X, y)
