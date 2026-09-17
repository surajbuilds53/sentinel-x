"""Unit tests for the LSTM World Model and multi-task forecasting heads in Sentinel-X."""

import torch
import pytest
from sentinel_x.models.lstm_world_model import LSTMWorldModel
from sentinel_x.models.forecasting_heads import RiskHead, StageHead, NetworkStateHead
from sentinel_x.models.losses import MultiTaskForecastingLoss


def test_forecasting_heads_shapes():
    batch_size = 8
    hidden_size = 128
    latent = torch.randn(batch_size, hidden_size)

    risk_head = RiskHead(hidden_size=hidden_size)
    stage_head = StageHead(hidden_size=hidden_size, num_classes=5)
    state_head = NetworkStateHead(hidden_size=hidden_size, state_dim=16)

    pred_risk = risk_head(latent)
    stage_logits = stage_head(latent)
    pred_state = state_head(latent)

    assert pred_risk.shape == (batch_size, 1)
    assert torch.all((pred_risk >= 0.0) & (pred_risk <= 1.0))
    assert stage_logits.shape == (batch_size, 5)
    assert pred_state.shape == (batch_size, 16)


def test_lstm_world_model_multistep_forward():
    batch_size = 4
    seq_len = 12
    input_dim = 16
    horizon = 3

    model = LSTMWorldModel(
        input_dim=input_dim,
        hidden_size=64,
        num_layers=2,
        dropout=0.2,
        num_stages=5,
    )

    dummy_seq = torch.randn(batch_size, seq_len, input_dim)
    outputs = model(dummy_seq, horizon=horizon)

    assert "risk_preds" in outputs
    assert "stage_logits" in outputs
    assert "state_preds" in outputs

    assert outputs["risk_preds"].shape == (batch_size, horizon)
    assert outputs["stage_logits"].shape == (batch_size, horizon, 5)
    assert outputs["state_preds"].shape == (batch_size, horizon, input_dim)


def test_lstm_world_model_inference():
    batch_size = 3
    seq_len = 10
    input_dim = 16
    horizon = 3

    model = LSTMWorldModel(input_dim=input_dim, hidden_size=64, num_layers=2)
    dummy_seq = torch.randn(batch_size, seq_len, input_dim)

    preds = model.forecast_inference(dummy_seq, horizon=horizon)

    assert preds["risk_probabilities"].shape == (batch_size, horizon)
    assert preds["stage_probabilities"].shape == (batch_size, horizon, 5)
    assert preds["predicted_stages"].shape == (batch_size, horizon)
    assert preds["predicted_states"].shape == (batch_size, horizon, input_dim)

    # Check softmax validity
    probs_sum = preds["stage_probabilities"].sum(dim=-1)
    assert torch.allclose(probs_sum, torch.ones_like(probs_sum), atol=1e-4)


def test_multitask_loss():
    batch_size = 4
    num_classes = 5
    state_dim = 16

    loss_fn = MultiTaskForecastingLoss(risk_weight=1.0, stage_weight=1.0, state_weight=0.5)

    pred_risk = torch.rand(batch_size, 1)
    pred_stage_logits = torch.randn(batch_size, num_classes)
    pred_state = torch.randn(batch_size, state_dim)

    target_risk = torch.randint(0, 2, (batch_size, 1)).float()
    target_stage = torch.randint(0, num_classes, (batch_size,)).long()
    target_state = torch.randn(batch_size, state_dim)

    loss, breakdown = loss_fn(
        pred_risk, pred_stage_logits, pred_state, target_risk, target_stage, target_state
    )

    assert loss.item() > 0.0
    assert "risk_loss" in breakdown
    assert "stage_loss" in breakdown
    assert "state_loss" in breakdown
    assert "total_loss" in breakdown
