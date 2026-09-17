"""Tests for dashboard components, import integrity, and data loading."""

import pytest
import numpy as np
import plotly.graph_objects as go

from dashboard.components.header import apply_custom_soc_styles
from dashboard.components.executive_view import create_risk_gauge
from dashboard.app import load_trained_model_and_data


def test_create_risk_gauge():
    fig = create_risk_gauge(0.75, title="Test Risk")
    assert isinstance(fig, go.Figure)
    assert len(fig.data) == 1
    assert fig.data[0].value == 75.0


def test_dashboard_model_and_data_loading():
    model, test_X, test_Y_risk, shap_data = load_trained_model_and_data()
    assert model is not None
    assert test_X is not None
    assert test_X.shape[-1] == 16
    assert test_X.shape[1] == 12  # Sequence length
