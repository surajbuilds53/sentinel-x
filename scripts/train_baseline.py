#!/usr/bin/env python3
"""Training and Evaluation Script for Static Logistic Regression Baseline.

Defensive Cybersecurity B.Tech Minor Project (SIH26153).
"""

from pathlib import Path
import argparse
import json
import logging
import numpy as np

from sentinel_x.config import load_config, PROJECT_ROOT, set_seed
from sentinel_x.baseline.logistic_regression import BaselineLogisticRegression
from sentinel_x.data.aggregation import FEATURE_NAMES

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("train_baseline")


def train_and_evaluate_baseline(config_path: Path | str | None = None) -> dict:
    config = load_config(config_path)
    set_seed(config["project"]["random_seed"])
    
    proc_data_path = PROJECT_ROOT / config["paths"]["processed_data_dir"] / "processed_windows.npz"
    if not proc_data_path.is_file():
        raise FileNotFoundError(
            f"Processed data file not found at {proc_data_path}. "
            f"Please run 'python scripts/prepare_data.py' first."
        )
        
    logger.info(f"Loading processed window dataset from {proc_data_path}...")
    data = np.load(proc_data_path)
    
    # Baseline uses the static state at time T (the latest observation: slice -1)
    # to forecast risk at T+1 (horizon index 0)
    train_X = data["train_X"][:, -1, :]
    train_y = data["train_Y_risk"][:, 0]
    
    val_X = data["val_X"][:, -1, :]
    val_y = data["val_Y_risk"][:, 0]
    
    test_X = data["test_X"][:, -1, :]
    test_y = data["test_Y_risk"][:, 0]
    
    logger.info(f"Static dataset shapes -> Train: {train_X.shape}, Val: {val_X.shape}, Test: {test_X.shape}")
    logger.info(f"Attack class balance -> Train: {np.mean(train_y):.2%}, Test: {np.mean(test_y):.2%}")
    
    # Initialize baseline model
    b_cfg = config["baseline"]
    baseline = BaselineLogisticRegression(
        C=float(b_cfg.get("C", 1.0)),
        max_iter=int(b_cfg.get("max_iter", 1000)),
        solver=b_cfg.get("solver", "lbfgs"),
        random_state=config["project"]["random_seed"],
    )
    
    # Train
    logger.info("Training StandardScaler -> LogisticRegression pipeline...")
    baseline.fit(train_X, train_y)
    
    # Evaluate
    logger.info("Evaluating baseline on unseen test set...")
    metrics = baseline.evaluate(test_X, test_y)
    
    # Feature coefficients
    importances = baseline.get_feature_importances(FEATURE_NAMES)
    top_features = sorted(importances.items(), key=lambda x: abs(x[1]), reverse=True)[:5]
    
    # Save artifacts
    model_save_path = PROJECT_ROOT / b_cfg["model_save_path"]
    scaler_save_path = PROJECT_ROOT / b_cfg["scaler_save_path"]
    metrics_save_path = PROJECT_ROOT / b_cfg["metrics_save_path"]
    
    metrics_save_path.parent.mkdir(parents=True, exist_ok=True)
    baseline.save(model_save_path, scaler_save_path)
    logger.info(f"Saved model checkpoint -> {model_save_path}")
    logger.info(f"Saved scaler artifact   -> {scaler_save_path}")
    
    # Save full metrics report as JSON
    report = {
        "model": "Logistic Regression Baseline (Static)",
        "features_used": FEATURE_NAMES,
        "metrics": metrics,
        "top_features": dict(top_features),
        "test_samples": int(len(test_y)),
    }
    with open(metrics_save_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    logger.info(f"Saved baseline metrics  -> {metrics_save_path}")
    
    return report


def main():
    parser = argparse.ArgumentParser(description="Train static Logistic Regression baseline for Sentinel-X")
    parser.add_argument("--config", type=str, default=None, help="Path to config.yaml")
    args = parser.parse_args()
    
    report = train_and_evaluate_baseline(args.config)
    m = report["metrics"]
    
    print("\n" + "=" * 65)
    print(" SENTINEL-X | LOGISTIC REGRESSION BASELINE EVALUATION")
    print("=" * 65)
    print(f"[*] Precision           : {m['precision']:.4f}")
    print(f"[*] Recall              : {m['recall']:.4f}")
    print(f"[*] F1-Score            : {m['f1_score']:.4f}")
    print(f"[*] False Positive Rate : {m['false_positive_rate']:.4f}")
    print(f"[*] Accuracy            : {m['accuracy']:.4f}")
    if m.get("roc_auc") is not None:
        print(f"[*] ROC-AUC             : {m['roc_auc']:.4f}")
    print(f"[*] Confusion Matrix    : TN={m['true_negatives']}, FP={m['false_positives']}, FN={m['false_negatives']}, TP={m['true_positives']}")
    print("-" * 65)
    print("Top Influential Static Features (Coefficients):")
    for feat, coef in report["top_features"].items():
        print(f"    - {feat:18s} : {coef:+.4f}")
    print("=" * 65)


if __name__ == "__main__":
    main()
