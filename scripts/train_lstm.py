#!/usr/bin/env python3
"""Training and Multi-Step Evaluation Script for Sentinel-X LSTM World Model.

Defensive Cybersecurity B.Tech Minor Project (SIH26153).
"""

from pathlib import Path
import argparse
import json
import logging
import numpy as np
import torch
from torch.utils.data import TensorDataset, DataLoader

from sentinel_x.config import load_config, PROJECT_ROOT, set_seed, get_device
from sentinel_x.models.lstm_world_model import LSTMWorldModel
from sentinel_x.models.losses import MultiTaskForecastingLoss
from sentinel_x.training.trainer import WorldModelTrainer
from sentinel_x.evaluation.metrics import (
    compute_risk_metrics,
    compute_stage_metrics,
    compute_state_metrics,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("train_lstm")


def evaluate_multistep_performance(
    model: LSTMWorldModel,
    test_X: np.ndarray,
    test_Y_risk: np.ndarray,
    test_Y_stage: np.ndarray,
    test_Y_state: np.ndarray,
    horizon: int = 3,
    device: str = "cpu",
) -> dict:
    """Evaluate performance across individual forecast horizons (T+1, T+2, T+3)."""
    dev = torch.device(get_device(device))
    model.eval()
    model.to(dev)

    with torch.no_grad():
        x_tensor = torch.from_numpy(test_X).float().to(dev)
        outputs = model.forecast_inference(x_tensor, horizon=horizon)

        pred_risks = outputs["risk_probabilities"].cpu().numpy()
        pred_stages = outputs["predicted_stages"].cpu().numpy()
        pred_states = outputs["predicted_states"].cpu().numpy()

    horizon_results = {}
    for h in range(horizon):
        step_name = f"T+{h+1}"
        r_metrics = compute_risk_metrics(
            y_true=test_Y_risk[:, h],
            y_pred=pred_risks[:, h],
            y_probs=pred_risks[:, h],
            threshold=0.5,
        )
        st_metrics = compute_stage_metrics(
            y_true=test_Y_stage[:, h],
            y_pred=pred_stages[:, h],
            labels=[0, 1, 2, 3, 4],
        )
        se_metrics = compute_state_metrics(
            y_true=test_Y_state[:, h, :],
            y_pred=pred_states[:, h, :],
        )

        horizon_results[step_name] = {
            "risk_metrics": r_metrics,
            "stage_metrics": st_metrics,
            "state_metrics": se_metrics,
        }

    return horizon_results


def train_and_evaluate_lstm(config_path: Path | str | None = None) -> dict:
    config = load_config(config_path)
    set_seed(config["project"]["random_seed"])
    device = config["environment"].get("device", "auto")

    proc_data_path = PROJECT_ROOT / config["paths"]["processed_data_dir"] / "processed_windows.npz"
    if not proc_data_path.is_file():
        raise FileNotFoundError(
            f"Processed data file not found at {proc_data_path}. "
            f"Please run 'python scripts/prepare_data.py' first."
        )

    logger.info(f"Loading processed window dataset from {proc_data_path}...")
    data = np.load(proc_data_path)

    train_X = data["train_X"]
    train_Y_risk = data["train_Y_risk"]
    train_Y_stage = data["train_Y_stage"]
    train_Y_state = data["train_Y_state"]

    val_X = data["val_X"]
    val_Y_risk = data["val_Y_risk"]
    val_Y_stage = data["val_Y_stage"]
    val_Y_state = data["val_Y_state"]

    test_X = data["test_X"]
    test_Y_risk = data["test_Y_risk"]
    test_Y_stage = data["test_Y_stage"]
    test_Y_state = data["test_Y_state"]

    logger.info(f"Train shapes: X={train_X.shape}, Y_risk={train_Y_risk.shape}")
    logger.info(f"Val shapes:   X={val_X.shape}, Y_risk={val_Y_risk.shape}")
    logger.info(f"Test shapes:  X={test_X.shape}, Y_risk={test_Y_risk.shape}")

    # Convert to DataLoaders
    batch_size = config["lstm_world_model"]["training"].get("batch_size", 32)

    train_ds = TensorDataset(
        torch.from_numpy(train_X).float(),
        torch.from_numpy(train_Y_risk).float(),
        torch.from_numpy(train_Y_stage).long(),
        torch.from_numpy(train_Y_state).float(),
    )
    val_ds = TensorDataset(
        torch.from_numpy(val_X).float(),
        torch.from_numpy(val_Y_risk).float(),
        torch.from_numpy(val_Y_stage).long(),
        torch.from_numpy(val_Y_state).float(),
    )

    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=batch_size, shuffle=False)

    # Instantiate Model
    m_cfg = config["lstm_world_model"]
    model = LSTMWorldModel(
        input_dim=m_cfg.get("input_dim", 16),
        hidden_size=m_cfg.get("hidden_size", 128),
        num_layers=m_cfg.get("num_layers", 2),
        dropout=m_cfg.get("dropout", 0.3),
        num_stages=m_cfg.get("stage_classes", 5),
    )

    # Loss Function
    w = m_cfg.get("loss_weights", {})
    loss_fn = MultiTaskForecastingLoss(
        risk_weight=w.get("risk_loss_weight", 1.0),
        stage_weight=w.get("stage_loss_weight", 1.0),
        state_weight=w.get("state_loss_weight", 0.5),
    )

    # Trainer
    t_cfg = m_cfg["training"]
    trainer = WorldModelTrainer(
        model=model,
        loss_fn=loss_fn,
        learning_rate=float(t_cfg.get("learning_rate", 0.001)),
        weight_decay=float(t_cfg.get("weight_decay", 1e-4)),
        device=device,
    )

    best_model_path = PROJECT_ROOT / t_cfg.get("best_model_path", "models/checkpoints/best_lstm_world_model.pt")
    fit_summary = trainer.fit(
        train_loader=train_loader,
        val_loader=val_loader,
        epochs=t_cfg.get("epochs", 20),
        horizon=config["data_pipeline"]["forecast_horizon"],
        patience=t_cfg.get("early_stopping_patience", 5),
        checkpoint_path=best_model_path,
    )

    # Multi-Step Test Evaluation
    logger.info("Evaluating multi-step forecasting on test set (T+1, T+2, T+3)...")
    eval_results = evaluate_multistep_performance(
        model=model,
        test_X=test_X,
        test_Y_risk=test_Y_risk,
        test_Y_stage=test_Y_stage,
        test_Y_state=test_Y_state,
        horizon=config["data_pipeline"]["forecast_horizon"],
        device=device,
    )

    # Save metrics JSON
    metrics_path = PROJECT_ROOT / t_cfg.get("metrics_save_path", "models/evaluation/lstm_metrics.json")
    metrics_path.parent.mkdir(parents=True, exist_ok=True)
    full_report = {
        "model": "LSTM World Model (Deep Recurrent Multi-Task)",
        "training_summary": fit_summary,
        "multistep_evaluation": eval_results,
    }
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(full_report, f, indent=2)
    logger.info(f"Saved LSTM metrics report -> {metrics_path}")

    return full_report


def main():
    parser = argparse.ArgumentParser(description="Train Sentinel-X LSTM World Model")
    parser.add_argument("--config", type=str, default=None, help="Path to config.yaml")
    args = parser.parse_args()

    report = train_and_evaluate_lstm(args.config)
    ms = report["multistep_evaluation"]

    print("\n" + "=" * 70)
    print(" SENTINEL-X | LSTM WORLD MODEL MULTI-STEP FORECASTING EVALUATION")
    print("=" * 70)
    print(f"{'Horizon':<8} | {'Risk Prec':<10} | {'Risk Rec':<10} | {'Risk F1':<10} | {'Stage Acc':<10} | {'State MAE':<10}")
    print("-" * 70)
    for step in ["T+1", "T+2", "T+3"]:
        s = ms[step]
        r = s["risk_metrics"]
        st = s["stage_metrics"]
        se = s["state_metrics"]
        print(f"{step:<8} | {r['precision']:<10.4f} | {r['recall']:<10.4f} | {r['f1_score']:<10.4f} | {st['accuracy']:<10.4f} | {se['mae']:<10.4f}")
    print("=" * 70)


if __name__ == "__main__":
    main()
