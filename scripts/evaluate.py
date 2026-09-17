#!/usr/bin/env python3
"""Comprehensive Evaluation and Model Comparison Script for Sentinel-X.

Defensive Cybersecurity B.Tech Minor Project (SIH26153).
Compares Baseline Logistic Regression vs. LSTM World Model and generates SHAP explanations.
"""

from pathlib import Path
import argparse
import json
import logging
import numpy as np
import pandas as pd
import torch

from sentinel_x.config import load_config, PROJECT_ROOT, get_device
from sentinel_x.models.lstm_world_model import LSTMWorldModel
from sentinel_x.evaluation.comparison import generate_comparison_summary
from sentinel_x.explainability.shap_explainer import SentinelXExplainer
from sentinel_x.data.aggregation import FEATURE_NAMES

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("evaluate")


def run_evaluation(config_path: Path | str | None = None) -> dict:
    config = load_config(config_path)
    eval_dir = PROJECT_ROOT / config["paths"]["evaluation_dir"]
    eval_dir.mkdir(parents=True, exist_ok=True)

    # 1. Generate Model Comparison Tables
    logger.info("Generating comparative evaluation summary (Baseline vs LSTM)...")
    comp_json = eval_dir / "model_comparison.json"
    comp_csv = eval_dir / "model_comparison.csv"

    comparison = generate_comparison_summary(
        output_json_path=comp_json,
        output_csv_path=comp_csv,
    )
    logger.info(f"Saved comparison tables -> {comp_json} and {comp_csv}")

    # 2. Compute SHAP Feature Attribution & Explainability
    proc_path = PROJECT_ROOT / config["paths"]["processed_data_dir"] / "processed_windows.npz"
    ckpt_path = PROJECT_ROOT / config["lstm_world_model"]["training"]["best_model_path"]

    if proc_path.is_file() and ckpt_path.is_file():
        logger.info(f"Loading checkpoint {ckpt_path} to compute SHAP attributions...")
        data = np.load(proc_path)
        train_X = data["train_X"]
        test_X = data["test_X"]

        device = config["environment"].get("device", "auto")
        model = LSTMWorldModel(
            input_dim=config["lstm_world_model"].get("input_dim", 16),
            hidden_size=config["lstm_world_model"].get("hidden_size", 128),
            num_layers=config["lstm_world_model"].get("num_layers", 2),
            num_stages=config["lstm_world_model"].get("stage_classes", 5),
        )

        checkpoint = torch.load(ckpt_path, map_location=get_device(device))
        model.load_state_dict(checkpoint["model_state_dict"])

        explainer = SentinelXExplainer(
            model=model,
            background_data=train_X[:30],
            feature_names=FEATURE_NAMES,
            device=get_device(device),
        )

        shap_out = eval_dir / "shap_summary.json"
        shap_summary = explainer.save_summary_report(
            test_sequences=test_X,
            output_path=shap_out,
            num_instances=5,
        )
        logger.info("SHAP explainability computation completed successfully.")
    else:
        shap_summary = None

    return {
        "comparison": comparison,
        "shap_summary": shap_summary,
    }


def main():
    parser = argparse.ArgumentParser(description="Evaluate and compare Sentinel-X models")
    parser.add_argument("--config", type=str, default=None, help="Path to config.yaml")
    args = parser.parse_args()

    results = run_evaluation(args.config)
    comp = results["comparison"]

    print("\n" + "=" * 80)
    print(" SENTINEL-X | MODEL COMPARISON: BASELINE vs. LSTM WORLD MODEL")
    print("=" * 80)
    df = pd.DataFrame(comp["summary_table"])
    print(df.to_string(index=False))
    print("-" * 80)
    print("Key Architectural Findings:")
    for k, v in comp["key_findings"].items():
        print(f"  * {k:24s} : {v}")
    print("=" * 80)


if __name__ == "__main__":
    main()
