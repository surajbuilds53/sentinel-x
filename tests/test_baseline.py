"""Unit tests for the Logistic Regression baseline model in Sentinel-X."""

import numpy as np
import pytest
from pathlib import Path
import tempfile

from sentinel_x.baseline.logistic_regression import BaselineLogisticRegression
from sentinel_x.evaluation.metrics import compute_risk_metrics


def test_baseline_fit_and_predict():
    np.random.seed(42)
    # 100 samples, 16 features
    X = np.random.randn(100, 16).astype(np.float32)
    # Synthetic ground truth
    y = (X[:, 0] + X[:, 1] > 0.5).astype(int)
    
    model = BaselineLogisticRegression(random_state=42)
    assert not model.is_fitted
    
    model.fit(X, y)
    assert model.is_fitted
    
    preds = model.predict(X)
    probs = model.predict_proba(X)
    
    assert preds.shape == (100,)
    assert probs.shape == (100,)
    assert np.all((probs >= 0.0) & (probs <= 1.0))
    assert set(np.unique(preds)).issubset({0, 1})


def test_baseline_evaluation_metrics():
    np.random.seed(42)
    X = np.random.randn(80, 16).astype(np.float32)
    y = (X[:, 2] > 0.0).astype(int)
    
    model = BaselineLogisticRegression(random_state=42)
    model.fit(X, y)
    
    metrics = model.evaluate(X, y)
    
    assert "precision" in metrics
    assert "recall" in metrics
    assert "f1_score" in metrics
    assert "false_positive_rate" in metrics
    assert "confusion_matrix" in metrics
    assert 0.0 <= metrics["false_positive_rate"] <= 1.0
    assert 0.0 <= metrics["f1_score"] <= 1.0


def test_baseline_save_and_load(tmp_path):
    np.random.seed(42)
    X = np.random.randn(50, 16).astype(np.float32)
    y = (X[:, 0] > 0.0).astype(int)
    
    model = BaselineLogisticRegression(random_state=42)
    model.fit(X, y)
    
    m_path = tmp_path / "baseline_model.joblib"
    s_path = tmp_path / "baseline_scaler.joblib"
    
    model.save(m_path, s_path)
    assert m_path.is_file()
    assert s_path.is_file()
    
    loaded = BaselineLogisticRegression.load(m_path, s_path)
    assert loaded.is_fitted
    
    original_preds = model.predict(X)
    loaded_preds = loaded.predict(X)
    np.testing.assert_array_equal(original_preds, loaded_preds)
