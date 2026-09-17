"""Unit tests for evaluation metrics and model comparison in Sentinel-X."""

import numpy as np
import pytest
from sentinel_x.evaluation.metrics import (
    compute_risk_metrics,
    compute_stage_metrics,
    compute_state_metrics,
)
from sentinel_x.evaluation.comparison import generate_comparison_summary


def test_compute_risk_metrics():
    y_true = np.array([0, 0, 1, 1, 1, 0, 1])
    y_probs = np.array([0.1, 0.2, 0.8, 0.9, 0.6, 0.3, 0.7])

    metrics = compute_risk_metrics(y_true, y_probs, y_probs=y_probs, threshold=0.5)

    assert metrics["accuracy"] == 1.0
    assert metrics["precision"] == 1.0
    assert metrics["recall"] == 1.0
    assert metrics["f1_score"] == 1.0
    assert metrics["false_positive_rate"] == 0.0
    assert metrics["true_positives"] == 4
    assert metrics["true_negatives"] == 3


def test_compute_stage_metrics():
    y_true = np.array([0, 1, 2, 3, 4, 0, 1])
    y_pred = np.array([0, 1, 2, 3, 4, 0, 2])  # 1 mistake on last sample

    metrics = compute_stage_metrics(y_true, y_pred, labels=[0, 1, 2, 3, 4])

    assert metrics["accuracy"] == pytest.approx(6 / 7, abs=1e-3)
    assert 0.0 <= metrics["macro_f1"] <= 1.0
    assert len(metrics["confusion_matrix"]) == 5


def test_compute_state_metrics():
    y_true = np.array([[1.0, 2.0], [3.0, 4.0]])
    y_pred = np.array([[1.1, 1.9], [3.2, 3.8]])

    metrics = compute_state_metrics(y_true, y_pred)

    assert metrics["mae"] == pytest.approx(0.15, abs=1e-2)
    assert metrics["rmse"] > 0.0


def test_model_comparison_generation():
    comparison = generate_comparison_summary()
    assert "summary_table" in comparison
    assert len(comparison["summary_table"]) == 4  # Baseline + T+1, T+2, T+3
    assert "key_findings" in comparison
