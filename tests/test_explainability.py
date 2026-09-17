"""Unit tests for the SHAP explainability engine in Sentinel-X."""

import numpy as np
import torch
import pytest

from sentinel_x.models.lstm_world_model import LSTMWorldModel
from sentinel_x.explainability.shap_explainer import SentinelXExplainer


def test_shap_explainer_initialization_and_attribution():
    torch.manual_seed(42)
    np.random.seed(42)

    model = LSTMWorldModel(input_dim=16, hidden_size=32, num_layers=1)
    bg_data = np.random.randn(10, 12, 16).astype(np.float32)
    test_seq = np.random.randn(12, 16).astype(np.float32)

    explainer = SentinelXExplainer(
        model=model,
        background_data=bg_data,
        device="cpu",
    )

    assert explainer.explainer_type in ["KernelExplainer", "GradientFallback"]

    res = explainer.explain_sample(test_seq, nsamples=20)

    assert res["status"] == "success"
    assert "predicted_risk_T1" in res
    assert 0.0 <= res["predicted_risk_T1"] <= 1.0
    assert "feature_contributions" in res
    assert len(res["feature_contributions"]) == 16
    assert "top_risk_drivers" in res
    assert "temporal_importance" in res
    assert len(res["temporal_importance"]) == 12  # 12 historical time steps
