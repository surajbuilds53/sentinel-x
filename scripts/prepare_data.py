#!/usr/bin/env python3
"""Data Preparation and Preprocessing Pipeline Script for Sentinel-X.

Defensive Cybersecurity B.Tech Minor Project (SIH26153).
"""

from pathlib import Path
import argparse
import logging
import joblib
import numpy as np
import pandas as pd

from sentinel_x.config import load_config, PROJECT_ROOT, set_seed
from sentinel_x.data.loader import load_dataset
from sentinel_x.data.aggregation import aggregate_flows_to_time_windows, FEATURE_NAMES
from sentinel_x.data.windowing import (
    chronological_split,
    create_rolling_windows,
    scale_window_datasets,
)
from sentinel_x.data.synthetic import generate_synthetic_flow_dataset

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("prepare_data")


def run_data_pipeline(config_path: Path | str | None = None) -> dict:
    config = load_config(config_path)
    set_seed(config["project"]["random_seed"])
    
    raw_dir = PROJECT_ROOT / config["paths"]["raw_data_dir"]
    sample_dir = PROJECT_ROOT / config["paths"]["sample_data_dir"]
    processed_dir = PROJECT_ROOT / config["paths"]["processed_data_dir"]
    scaler_dir = PROJECT_ROOT / config["paths"]["scaler_dir"]
    
    processed_dir.mkdir(parents=True, exist_ok=True)
    scaler_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. Determine input data source
    raw_csvs = list(raw_dir.glob("*.csv"))
    if raw_csvs:
        logger.info(f"Found {len(raw_csvs)} raw dataset file(s) in {raw_dir}")
        df = load_dataset(raw_dir, clean=True)
        data_source_type = "CIC-IDS Raw Benchmark"
    else:
        sample_csv = sample_dir / "synthetic_flows.csv"
        if not sample_csv.is_file():
            logger.info(f"No raw files found. Generating sample synthetic dataset at {sample_csv}")
            generate_synthetic_flow_dataset(num_flows=6000, output_path=sample_csv)
        else:
            logger.info(f"Loading existing sample dataset from {sample_csv}")
        df = load_dataset(sample_csv, clean=True)
        data_source_type = "Synthetic Demo Dataset"
        
    logger.info(f"Cleaned flow dataset: {len(df)} records, {len(df.columns)} columns.")
    
    # 2. Temporal Aggregation into Network-State Vectors
    window_sec = config["data_pipeline"]["time_window_seconds"]
    logger.info(f"Aggregating flow records into {window_sec}s temporal network-state vectors...")
    state_df = aggregate_flows_to_time_windows(
        df,
        window_seconds=window_sec,
        time_col=config["data_pipeline"].get("timestamp_column", "timestamp").lower(),
        label_col=config["data_pipeline"].get("label_column", "label").lower(),
    )
    logger.info(f"Generated {len(state_df)} temporal network-state vectors.")
    
    # Save the unscaled state timeline for the SOC dashboard
    state_timeline_path = processed_dir / "network_state_timeline.csv"
    state_df.to_csv(state_timeline_path, index=False)
    logger.info(f"Saved state timeline -> {state_timeline_path}")
    
    # 3. Chronological Train / Val / Test Splits (NO SHUFFLE)
    splits = config["data_pipeline"]["chronological_splits"]
    train_df, val_df, test_df = chronological_split(
        state_df,
        train_ratio=splits["train_ratio"],
        val_ratio=splits["val_ratio"],
        test_ratio=splits["test_ratio"],
    )
    logger.info(f"Chronological split sizes -> Train: {len(train_df)}, Val: {len(val_df)}, Test: {len(test_df)}")
    
    # 4. Create Rolling Sequence Windows (T-N...T -> T+1, T+2, T+3)
    seq_len = config["data_pipeline"]["sequence_length"]
    horizon = config["data_pipeline"]["forecast_horizon"]
    
    train_X, train_Y_risk, train_Y_stage, train_Y_state = create_rolling_windows(
        train_df, sequence_length=seq_len, forecast_horizon=horizon
    )
    val_X, val_Y_risk, val_Y_stage, val_Y_state = create_rolling_windows(
        val_df, sequence_length=seq_len, forecast_horizon=horizon
    )
    test_X, test_Y_risk, test_Y_stage, test_Y_state = create_rolling_windows(
        test_df, sequence_length=seq_len, forecast_horizon=horizon
    )
    logger.info(f"Rolling window sample counts -> Train: {len(train_X)}, Val: {len(val_X)}, Test: {len(test_X)}")
    
    # 5. Fit Scaler STRICTLY on Train and transform all splits
    (
        s_train_X, s_val_X, s_test_X,
        s_train_Y_state, s_val_Y_state, s_test_Y_state,
        scaler
    ) = scale_window_datasets(
        train_X, val_X, test_X,
        train_Y_state, val_Y_state, test_Y_state
    )
    
    # 6. Save scaler artifact
    scaler_path = PROJECT_ROOT / config["lstm_world_model"]["training"]["scaler_save_path"]
    scaler_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(scaler, scaler_path)
    logger.info(f"Saved state scaler -> {scaler_path}")
    
    # 7. Save processed tensors / arrays
    npz_path = processed_dir / "processed_windows.npz"
    np.savez_compressed(
        npz_path,
        train_X=s_train_X,
        train_Y_risk=train_Y_risk,
        train_Y_stage=train_Y_stage,
        train_Y_state=s_train_Y_state,
        val_X=s_val_X,
        val_Y_risk=val_Y_risk,
        val_Y_stage=val_Y_stage,
        val_Y_state=s_val_Y_state,
        test_X=s_test_X,
        test_Y_risk=test_Y_risk,
        test_Y_stage=test_Y_stage,
        test_Y_state=s_test_Y_state,
        raw_test_X=test_X,
        raw_test_Y_state=test_Y_state,
    )
    logger.info(f"Saved processed window dataset -> {npz_path}")
    
    return {
        "data_source_type": data_source_type,
        "raw_flows": len(df),
        "state_vectors": len(state_df),
        "train_samples": len(s_train_X),
        "val_samples": len(s_val_X),
        "test_samples": len(s_test_X),
        "feature_dim": s_train_X.shape[-1],
        "sequence_length": seq_len,
        "forecast_horizon": horizon,
    }


def main():
    parser = argparse.ArgumentParser(description="Sentinel-X Data Pipeline Runner")
    parser.add_argument("--config", type=str, default=None, help="Path to config.yaml")
    args = parser.parse_args()
    
    summary = run_data_pipeline(args.config)
    print("\n" + "=" * 65)
    print(" SENTINEL-X | DATA PIPELINE PREPARATION SUMMARY")
    print("=" * 65)
    for k, v in summary.items():
        print(f"[*] {k:22s} : {v}")
    print("=" * 65)


if __name__ == "__main__":
    main()
