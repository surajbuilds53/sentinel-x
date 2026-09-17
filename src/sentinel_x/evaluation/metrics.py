"""Standard evaluation metrics for binary risk, multi-class stage, and continuous state prediction."""

from typing import Dict, Any, List, Union, Optional
import numpy as np
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    mean_absolute_error,
    mean_squared_error,
    roc_auc_score,
)


def compute_risk_metrics(
    y_true: Union[np.ndarray, List[float]],
    y_pred: Union[np.ndarray, List[float]],
    y_probs: Union[np.ndarray, List[float], None] = None,
    threshold: float = 0.5,
) -> Dict[str, Any]:
    """Compute binary risk forecasting metrics: Precision, Recall, F1, FPR, Confusion Matrix.
    
    Args:
        y_true: Ground truth binary labels (0 or 1).
        y_pred: Predicted binary labels (0 or 1), or probabilities if y_probs is None.
        y_probs: Optional continuous probabilities in [0, 1].
        threshold: Decision threshold for probability classification.
        
    Returns:
        Dict of computed evaluation metrics.
    """
    y_true = np.asarray(y_true, dtype=int).ravel()
    
    if y_probs is not None:
        y_probs = np.asarray(y_probs, dtype=float).ravel()
        y_pred = (y_probs >= threshold).astype(int)
    elif np.issubdtype(np.asarray(y_pred).dtype, np.floating):
        y_probs = np.asarray(y_pred, dtype=float).ravel()
        y_pred = (y_probs >= threshold).astype(int)
    else:
        y_pred = np.asarray(y_pred, dtype=int).ravel()
        
    cm = confusion_matrix(y_true, y_pred, labels=[0, 1])
    tn, fp, fn, tp = cm.ravel()
    
    fpr = float(fp / (fp + tn)) if (fp + tn) > 0 else 0.0
    precision = float(precision_score(y_true, y_pred, zero_division=0))
    recall = float(recall_score(y_true, y_pred, zero_division=0))
    f1 = float(f1_score(y_true, y_pred, zero_division=0))
    accuracy = float(accuracy_score(y_true, y_pred))
    
    roc_auc = None
    if y_probs is not None and len(np.unique(y_true)) > 1:
        try:
            roc_auc = float(roc_auc_score(y_true, y_probs))
        except Exception:
            roc_auc = None
            
    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1_score": f1,
        "false_positive_rate": fpr,
        "true_positives": int(tp),
        "false_positives": int(fp),
        "true_negatives": int(tn),
        "false_negatives": int(fn),
        "confusion_matrix": cm.tolist(),
        "roc_auc": roc_auc,
    }


def compute_stage_metrics(
    y_true: Union[np.ndarray, List[int]],
    y_pred: Union[np.ndarray, List[int]],
    labels: Optional[List[int]] = None,
) -> Dict[str, Any]:
    """Compute multi-class attack stage prediction metrics."""
    y_true = np.asarray(y_true, dtype=int).ravel()
    y_pred = np.asarray(y_pred, dtype=int).ravel()
    
    if labels is None:
        labels = [0, 1, 2, 3, 4]
        
    cm = confusion_matrix(y_true, y_pred, labels=labels)
    acc = float(accuracy_score(y_true, y_pred))
    macro_f1 = float(f1_score(y_true, y_pred, average="macro", zero_division=0))
    
    return {
        "accuracy": acc,
        "macro_f1": macro_f1,
        "confusion_matrix": cm.tolist(),
    }


def compute_state_metrics(
    y_true: np.ndarray,
    y_pred: np.ndarray,
) -> Dict[str, float]:
    """Compute future continuous network-state prediction error (MAE, RMSE)."""
    mae = float(mean_absolute_error(y_true.reshape(-1), y_pred.reshape(-1)))
    rmse = float(np.sqrt(mean_squared_error(y_true.reshape(-1), y_pred.reshape(-1))))
    return {
        "mae": mae,
        "rmse": rmse,
    }
