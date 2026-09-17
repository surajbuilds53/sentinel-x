"""End-to-end integration test verifying the complete Sentinel-X workflow pipeline."""

import numpy as np
import pandas as pd
import torch
import pytest

from sentinel_x.data.cleaner import clean_flow_dataframe
from sentinel_x.data.aggregation import aggregate_flows_to_time_windows
from sentinel_x.data.windowing import create_rolling_windows, chronological_split, scale_window_datasets
from sentinel_x.baseline.logistic_regression import BaselineLogisticRegression
from sentinel_x.models.lstm_world_model import LSTMWorldModel
from sentinel_x.models.losses import MultiTaskForecastingLoss
from sentinel_x.explainability.shap_explainer import SentinelXExplainer
from sentinel_x.evaluation.metrics import compute_risk_metrics


def test_full_pipeline_integration():
    """Verify raw flows -> clean -> aggregate -> window -> train baseline -> train LSTM -> explain."""
    # 1. Generate micro dataset
    base_time = pd.Timestamp("2026-04-01 10:00:00")
    records = []
    for i in range(120):
        records.append({
            "timestamp": base_time + pd.Timedelta(seconds=i * 2),
            "dst_port": 80 if i % 2 == 0 else 443,
            "tot_fwd_pkts": 5 + (i % 4),
            "tot_bwd_pkts": 4 + (i % 3),
            "tot_fwd_bytes": 200 + i * 15,
            "tot_bwd_bytes": 300 + i * 10,
            "flow_duration": 1000 + i * 20,
            "fwd_pkt_len_mean": 60.0,
            "bwd_pkt_len_mean": 70.0,
            "flow_iat_mean": 15.0,
            "syn_flag_cnt": 1 if i % 6 == 0 else 0,
            "rst_flag_cnt": 0,
            "ack_flag_cnt": 1,
            "fin_flag_cnt": 0,
            "protocol": 6,
            "label": "PortScan" if i > 60 else "Benign",
        })
    raw_df = pd.DataFrame(records)

    # 2. Clean
    clean_df = clean_flow_dataframe(raw_df)
    assert len(clean_df) == 120

    # 3. Temporal Aggregate
    state_df = aggregate_flows_to_time_windows(clean_df, window_seconds=4)
    assert len(state_df) >= 20

    # 4. Chronological Split
    train_df, val_df, test_df = chronological_split(state_df, 0.6, 0.2, 0.2)
    assert len(train_df) + len(val_df) + len(test_df) == len(state_df)

    # 5. Windowing
    seq_len = 5
    horizon = 3
    tr_X, tr_yr, tr_ys, tr_yst = create_rolling_windows(train_df, seq_len, horizon)
    te_X, te_yr, te_ys, te_yst = create_rolling_windows(test_df, seq_len, horizon)

    # 6. Baseline Fit & Predict
    baseline = BaselineLogisticRegression()
    baseline.fit(tr_X[:, -1, :], tr_yr[:, 0])
    base_preds = baseline.predict(te_X[:, -1, :])
    assert len(base_preds) == len(te_yr)

    # 7. LSTM Model Forward & Loss
    model = LSTMWorldModel(input_dim=16, hidden_size=32, num_layers=1)
    loss_fn = MultiTaskForecastingLoss()

    out = model(torch.from_numpy(tr_X).float(), horizon=horizon)
    assert out["risk_preds"].shape == (len(tr_X), horizon)

    loss, breakdown = loss_fn(
        out["risk_preds"][:, 0],
        out["stage_logits"][:, 0],
        out["state_preds"][:, 0],
        torch.from_numpy(tr_yr[:, 0]).float(),
        torch.from_numpy(tr_ys[:, 0]).long(),
        torch.from_numpy(tr_yst[:, 0]).float(),
    )
    assert loss.item() > 0

    # 8. SHAP Explanation
    explainer = SentinelXExplainer(model=model, background_data=tr_X[:5], device="cpu")
    expl = explainer.explain_sample(te_X[0], nsamples=15)
    assert expl["status"] == "success"
    assert "top_risk_drivers" in expl
