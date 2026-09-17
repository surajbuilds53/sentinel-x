"""Static Logistic Regression baseline model using scikit-learn."""

from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple
import joblib
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

from sentinel_x.evaluation.metrics import compute_risk_metrics


class BaselineLogisticRegression:
    """Static network risk baseline using StandardScaler -> LogisticRegression.
    
    Serves as the static benchmark to evaluate the predictive advantage
    of temporal deep sequence modeling (LSTM World Model).
    """

    def __init__(
        self,
        C: float = 1.0,
        max_iter: int = 1000,
        solver: str = "lbfgs",
        random_state: int = 42,
        **kwargs,
    ):
        self.scaler = StandardScaler()
        self.model = LogisticRegression(
            C=C,
            max_iter=max_iter,
            solver=solver,
            random_state=random_state,
        )
        self.is_fitted = False

    def fit(self, X: np.ndarray, y: np.ndarray) -> "BaselineLogisticRegression":
        """Fit scaler and logistic regression on training data.
        
        Args:
            X: 2D feature matrix of shape (num_samples, num_features).
            y: Binary target array of shape (num_samples,).
        """
        X = np.asarray(X, dtype=np.float32)
        y = np.asarray(y, dtype=np.int64).ravel()
        
        if X.ndim != 2:
            raise ValueError(f"Expected 2D array for static baseline, got ndim={X.ndim}")
            
        scaled_X = self.scaler.fit_transform(X)
        self.model.fit(scaled_X, y)
        self.is_fitted = True
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict binary risk (0 or 1)."""
        if not self.is_fitted:
            raise RuntimeError("Model must be fitted before predicting.")
        X = np.asarray(X, dtype=np.float32)
        scaled_X = self.scaler.transform(X)
        return self.model.predict(scaled_X)

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """Predict continuous risk probability in [0, 1]."""
        if not self.is_fitted:
            raise RuntimeError("Model must be fitted before predicting.")
        X = np.asarray(X, dtype=np.float32)
        scaled_X = self.scaler.transform(X)
        probs = self.model.predict_proba(scaled_X)
        # Return probability of class 1 (attack risk)
        return probs[:, 1] if probs.shape[1] > 1 else probs[:, 0]

    def evaluate(self, X: np.ndarray, y: np.ndarray, threshold: float = 0.5) -> Dict[str, Any]:
        """Evaluate baseline and return Precision, Recall, F1, FPR, Confusion Matrix."""
        y_true = np.asarray(y, dtype=np.int64).ravel()
        y_probs = self.predict_proba(X)
        y_pred = (y_probs >= threshold).astype(int)
        metrics = compute_risk_metrics(y_true, y_pred, y_probs=y_probs, threshold=threshold)
        return metrics

    def get_feature_importances(self, feature_names: List[str]) -> Dict[str, float]:
        """Get logistic regression feature coefficients."""
        if not self.is_fitted:
            raise RuntimeError("Model must be fitted before retrieving feature importances.")
        coefs = self.model.coef_[0]
        return {feat: float(coef) for feat, coef in zip(feature_names, coefs)}

    def save(self, model_path: Path | str, scaler_path: Path | str) -> None:
        """Save model and scaler artifacts to disk."""
        m_path = Path(model_path)
        s_path = Path(scaler_path)
        m_path.parent.mkdir(parents=True, exist_ok=True)
        s_path.parent.mkdir(parents=True, exist_ok=True)
        
        joblib.dump(self.model, m_path)
        joblib.dump(self.scaler, s_path)

    @classmethod
    def load(cls, model_path: Path | str, scaler_path: Path | str) -> "BaselineLogisticRegression":
        """Load saved model and scaler artifacts."""
        instance = cls()
        instance.model = joblib.load(model_path)
        instance.scaler = joblib.load(scaler_path)
        instance.is_fitted = True
        return instance
