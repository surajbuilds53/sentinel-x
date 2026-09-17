"""Rolling temporal window creation and leak-free chronological dataset splitting."""

from typing import Tuple, Dict, Any, Optional
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
import joblib

from sentinel_x.data.aggregation import FEATURE_NAMES


def create_rolling_windows(
    state_df: pd.DataFrame,
    sequence_length: int = 12,
    forecast_horizon: int = 3,
    feature_cols: Optional[list] = None,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Create rolling sequence windows for autoregressive multi-step forecasting.
    
    Given temporal network state sequence:
    Input X: [T - sequence_length + 1, ..., T]
    Target Y_risk:  [T+1, ..., T+forecast_horizon]
    Target Y_stage: [T+1, ..., T+forecast_horizon]
    Target Y_state: [T+1, ..., T+forecast_horizon]
    
    Args:
        state_df: DataFrame of aggregated temporal network-state vectors.
        sequence_length: Number of historical time-steps (N).
        forecast_horizon: Number of future forecast time-steps (H).
        feature_cols: List of column names representing the state vector.
        
    Returns:
        Tuple of (X, Y_risk, Y_stage, Y_state):
        - X: shape (num_samples, sequence_length, feature_dim)
        - Y_risk: shape (num_samples, forecast_horizon)
        - Y_stage: shape (num_samples, forecast_horizon)
        - Y_state: shape (num_samples, forecast_horizon, feature_dim)
    """
    if feature_cols is None:
        feature_cols = FEATURE_NAMES
        
    features = state_df[feature_cols].values.astype(np.float32)
    risks = state_df["risk"].values.astype(np.float32)
    stages = state_df["stage"].values.astype(np.int64)
    
    total_len = len(state_df)
    window_total = sequence_length + forecast_horizon
    
    if total_len < window_total:
        raise ValueError(
            f"Insufficient data points ({total_len}) for sequence_length={sequence_length} "
            f"and forecast_horizon={forecast_horizon}. Minimum required is {window_total}."
        )
        
    num_samples = total_len - window_total + 1
    
    X = np.zeros((num_samples, sequence_length, len(feature_cols)), dtype=np.float32)
    Y_risk = np.zeros((num_samples, forecast_horizon), dtype=np.float32)
    Y_stage = np.zeros((num_samples, forecast_horizon), dtype=np.int64)
    Y_state = np.zeros((num_samples, forecast_horizon, len(feature_cols)), dtype=np.float32)
    
    for i in range(num_samples):
        # Input history [i : i + sequence_length]
        X[i] = features[i : i + sequence_length]
        
        # Future targets [i + sequence_length : i + sequence_length + forecast_horizon]
        future_start = i + sequence_length
        future_end = future_start + forecast_horizon
        
        Y_risk[i] = risks[future_start : future_end]
        Y_stage[i] = stages[future_start : future_end]
        Y_state[i] = features[future_start : future_end]
        
    return X, Y_risk, Y_stage, Y_state


def chronological_split(
    state_df: pd.DataFrame,
    train_ratio: float = 0.70,
    val_ratio: float = 0.15,
    test_ratio: float = 0.15,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Chronologically split state DataFrame without shuffling to prevent temporal data leakage.
    
    Args:
        state_df: DataFrame sorted chronologically.
        train_ratio: Fraction for training split.
        val_ratio: Fraction for validation split.
        test_ratio: Fraction for testing split.
        
    Returns:
        (train_df, val_df, test_df)
    """
    total_len = len(state_df)
    train_end = int(total_len * train_ratio)
    val_end = int(total_len * (train_ratio + val_ratio))
    
    train_df = state_df.iloc[:train_end].copy().reset_index(drop=True)
    val_df = state_df.iloc[train_end:val_end].copy().reset_index(drop=True)
    test_df = state_df.iloc[val_end:].copy().reset_index(drop=True)
    
    return train_df, val_df, test_df


def scale_window_datasets(
    train_X: np.ndarray,
    val_X: np.ndarray,
    test_X: np.ndarray,
    train_Y_state: np.ndarray,
    val_Y_state: np.ndarray,
    test_Y_state: np.ndarray,
    scaler: Optional[StandardScaler] = None,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, StandardScaler]:
    """Fit StandardScaler ONLY on training features and apply transform to val and test.
    
    Strictly prevents future information leakage into training distributions.
    """
    if scaler is None:
        scaler = StandardScaler()
        # Flatten training temporal features to fit (N_samples * seq_len, num_features)
        flat_train = train_X.reshape(-1, train_X.shape[-1])
        scaler.fit(flat_train)
        
    def transform_3d(arr: np.ndarray) -> np.ndarray:
        s0, s1, s2 = arr.shape
        flat = arr.reshape(-1, s2)
        scaled_flat = scaler.transform(flat)
        return scaled_flat.reshape(s0, s1, s2).astype(np.float32)
        
    scaled_train_X = transform_3d(train_X)
    scaled_val_X = transform_3d(val_X)
    scaled_test_X = transform_3d(test_X)
    
    scaled_train_Y_state = transform_3d(train_Y_state)
    scaled_val_Y_state = transform_3d(val_Y_state)
    scaled_test_Y_state = transform_3d(test_Y_state)
    
    return (
        scaled_train_X,
        scaled_val_X,
        scaled_test_X,
        scaled_train_Y_state,
        scaled_val_Y_state,
        scaled_test_Y_state,
        scaler,
    )
