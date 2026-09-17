"""Tests for temporal aggregation, rolling windows, and chronological splitting."""

import numpy as np
import pandas as pd
import pytest

from sentinel_x.data.aggregation import aggregate_flows_to_time_windows, FEATURE_NAMES
from sentinel_x.data.windowing import (
    create_rolling_windows,
    chronological_split,
    scale_window_datasets,
)


@pytest.fixture
def dummy_flow_df():
    base_time = pd.Timestamp("2026-03-01 12:00:00")
    records = []
    for i in range(100):
        records.append({
            "timestamp": base_time + pd.Timedelta(seconds=i),
            "dst_port": 80 if i % 2 == 0 else 443,
            "tot_fwd_pkts": 5 + (i % 3),
            "tot_bwd_pkts": 4 + (i % 2),
            "tot_fwd_bytes": 100 + i * 10,
            "tot_bwd_bytes": 200 + i * 5,
            "flow_duration": 1000 + i * 50,
            "fwd_pkt_len_mean": 50.0,
            "bwd_pkt_len_mean": 60.0,
            "flow_iat_mean": 10.0,
            "syn_flag_cnt": 1 if i % 10 == 0 else 0,
            "rst_flag_cnt": 0,
            "ack_flag_cnt": 1,
            "fin_flag_cnt": 0,
            "protocol": 6,
            "label": "PortScan" if 40 <= i < 60 else "Benign",
        })
    return pd.DataFrame(records)


def test_temporal_aggregation(dummy_flow_df):
    state_df = aggregate_flows_to_time_windows(dummy_flow_df, window_seconds=10)
    assert len(state_df) > 0
    for feat in FEATURE_NAMES:
        assert feat in state_df.columns
    assert "risk" in state_df.columns
    assert "stage" in state_df.columns
    assert state_df["risk"].max() == 1.0


def test_chronological_split(dummy_flow_df):
    state_df = aggregate_flows_to_time_windows(dummy_flow_df, window_seconds=2)
    train_df, val_df, test_df = chronological_split(state_df, 0.7, 0.15, 0.15)
    
    assert len(train_df) + len(val_df) + len(test_df) == len(state_df)
    # Check strictly chronological ordering (no time overlap)
    assert train_df["window_time"].max() < val_df["window_time"].min()
    assert val_df["window_time"].max() < test_df["window_time"].min()


def test_rolling_windows(dummy_flow_df):
    state_df = aggregate_flows_to_time_windows(dummy_flow_df, window_seconds=2)
    seq_len = 5
    horizon = 3
    X, Y_risk, Y_stage, Y_state = create_rolling_windows(
        state_df, sequence_length=seq_len, forecast_horizon=horizon
    )
    
    expected_samples = len(state_df) - (seq_len + horizon) + 1
    assert X.shape == (expected_samples, seq_len, len(FEATURE_NAMES))
    assert Y_risk.shape == (expected_samples, horizon)
    assert Y_stage.shape == (expected_samples, horizon)
    assert Y_state.shape == (expected_samples, horizon, len(FEATURE_NAMES))


def test_scaler_no_leakage(dummy_flow_df):
    state_df = aggregate_flows_to_time_windows(dummy_flow_df, window_seconds=2)
    train_df, val_df, test_df = chronological_split(state_df, 0.6, 0.2, 0.2)
    
    X_tr, _, _, Y_tr = create_rolling_windows(train_df, 3, 2)
    X_va, _, _, Y_va = create_rolling_windows(val_df, 3, 2)
    X_te, _, _, Y_te = create_rolling_windows(test_df, 3, 2)
    
    s_X_tr, s_X_va, s_X_te, s_Y_tr, s_Y_va, s_Y_te, scaler = scale_window_datasets(
        X_tr, X_va, X_te, Y_tr, Y_va, Y_te
    )
    
    # Train mean should be close to 0
    flat_train = s_X_tr.reshape(-1, s_X_tr.shape[-1])
    assert np.allclose(flat_train.mean(axis=0), 0.0, atol=1e-1)
