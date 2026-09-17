"""SHAP-based explainability module for Sentinel-X attack risk forecasting."""

from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
import logging
import json
import numpy as np
import torch
import shap

from sentinel_x.data.aggregation import FEATURE_NAMES

logger = logging.getLogger(__name__)


class SentinelXExplainer:
    """Computes genuine feature attributions for risk forecasts using SHAP.
    
    Explains: 'Why did the model predict increased future risk?'
    Attributes predictive influence across both feature dimensions and temporal time-steps.
    """

    def __init__(
        self,
        model: torch.nn.Module,
        background_data: np.ndarray,
        feature_names: Optional[List[str]] = None,
        device: str = "cpu",
    ):
        """Args:
            model: Trained LSTMWorldModel.
            background_data: Representative background sequences (num_samples, seq_len, num_features).
            feature_names: Names of the 16 network-state features.
            device: Compute device.
        """
        self.model = model
        self.device = torch.device(device)
        self.model.to(self.device)
        self.model.eval()
        self.feature_names = feature_names or FEATURE_NAMES

        # Ensure 3D background data
        self.background_data = np.asarray(background_data, dtype=np.float32)
        if self.background_data.ndim != 3:
            raise ValueError(f"Expected 3D background data, got ndim={self.background_data.ndim}")

        self.num_samples, self.seq_len, self.num_features = self.background_data.shape
        self.explainer_type = "KernelExplainer"
        self._init_explainer()

    def _predict_risk_t1_flat(self, flat_inputs: np.ndarray) -> np.ndarray:
        """Prediction wrapper for flattened 2D arrays (samples, seq_len * num_features)."""
        num_items = flat_inputs.shape[0]
        reshaped = flat_inputs.reshape(num_items, self.seq_len, self.num_features)
        tensor_in = torch.from_numpy(reshaped).float().to(self.device)

        with torch.no_grad():
            # Risk at T+1 is index 0 of risk_preds
            preds = self.model(tensor_in, horizon=1)["risk_preds"][:, 0]
            return preds.cpu().numpy()

    def _init_explainer(self) -> None:
        """Initialize SHAP KernelExplainer with summary background distribution."""
        try:
            # Flatten background for kernel explainer
            flat_bg = self.background_data.reshape(self.num_samples, -1)
            # Use k-means or median sampling if background is large
            if len(flat_bg) > 20:
                bg_summary = shap.kmeans(flat_bg, min(10, len(flat_bg)))
            else:
                bg_summary = flat_bg

            self.explainer = shap.KernelExplainer(self._predict_risk_t1_flat, bg_summary)
            logger.info("Successfully initialized SHAP KernelExplainer.")
        except Exception as e:
            logger.warning(f"Failed to initialize KernelExplainer ({e}). Using gradient fallback.")
            self.explainer_type = "GradientFallback"
            self.explainer = None

    def explain_sample(
        self,
        sequence_window: np.ndarray,
        nsamples: int = 50,
    ) -> Dict[str, Any]:
        """Compute SHAP attributions for a single sequence window (seq_len, num_features).
        
        Args:
            sequence_window: Shape (seq_len, num_features) or (1, seq_len, num_features).
            nsamples: Number of Monte Carlo evaluations for KernelExplainer.
            
        Returns:
            Dict containing:
            - base_value: Expected baseline risk
            - predicted_risk: Model predicted risk at T+1
            - feature_contributions: Signed contribution per feature
            - top_risk_drivers: Features driving risk UP
            - top_risk_inhibitors: Features pulling risk DOWN
            - temporal_importance: Importance across time-steps T-N..T
        """
        seq = np.asarray(sequence_window, dtype=np.float32)
        if seq.ndim == 2:
            seq = np.expand_dims(seq, axis=0)

        flat_seq = seq.reshape(1, -1)
        pred_risk = float(self._predict_risk_t1_flat(flat_seq)[0])

        if self.explainer is not None:
            try:
                shap_vals = self.explainer.shap_values(flat_seq, nsamples=nsamples)
                if isinstance(shap_vals, list):
                    shap_vals = shap_vals[0]
                shap_vals = np.asarray(shap_vals).reshape(self.seq_len, self.num_features)
                base_val = float(getattr(self.explainer, "expected_value", 0.5))
            except Exception as e:
                logger.warning(f"KernelExplainer evaluation failed ({e}); invoking gradient attribution.")
                shap_vals, base_val = self._gradient_attribution(seq)
        else:
            shap_vals, base_val = self._gradient_attribution(seq)

        # 1. Feature-level attribution (mean across time)
        mean_feat_shap = shap_vals.mean(axis=0)
        feat_contrib = {feat: float(mean_feat_shap[i]) for i, feat in enumerate(self.feature_names)}

        # 2. Rank drivers (positive contribution -> increases risk)
        positive_drivers = sorted(
            [(k, v) for k, v in feat_contrib.items() if v > 0],
            key=lambda x: x[1],
            reverse=True,
        )
        negative_drivers = sorted(
            [(k, v) for k, v in feat_contrib.items() if v < 0],
            key=lambda x: x[1],
        )

        # 3. Temporal importance (mean magnitude across features per time step)
        temporal_mag = np.abs(shap_vals).mean(axis=1)
        temporal_dict = {
            f"T-{self.seq_len - 1 - t}": float(temporal_mag[t])
            for t in range(self.seq_len)
        }

        return {
            "status": "success",
            "explainer_type": self.explainer_type,
            "base_risk": base_val,
            "predicted_risk_T1": pred_risk,
            "feature_contributions": feat_contrib,
            "top_risk_drivers": positive_drivers[:5],
            "top_risk_inhibitors": negative_drivers[:5],
            "temporal_importance": temporal_dict,
        }

    def _gradient_attribution(self, seq_3d: np.ndarray) -> Tuple[np.ndarray, float]:
        """Deterministic gradient-based saliency fallback."""
        tensor_in = torch.from_numpy(seq_3d).float().to(self.device).requires_grad_(True)
        pred = self.model(tensor_in, horizon=1)["risk_preds"][:, 0]
        pred.backward()

        grad = tensor_in.grad.cpu().numpy()[0]  # (seq_len, num_features)
        # Saliency = input * gradient
        attributions = (seq_3d[0] * grad).astype(np.float32)
        base_val = 0.5
        return attributions, base_val

    def save_summary_report(
        self,
        test_sequences: np.ndarray,
        output_path: Optional[Path | str] = None,
        num_instances: int = 5,
    ) -> Dict[str, Any]:
        """Generate and serialize SHAP explanations for a sample of test instances."""
        out_p = Path(output_path) if output_path else PROJECT_ROOT / "models" / "evaluation" / "shap_summary.json"
        out_p.parent.mkdir(parents=True, exist_ok=True)

        explanations = []
        n_eval = min(num_instances, len(test_sequences))
        logger.info(f"Generating SHAP explanations for {n_eval} representative test sequences...")

        for i in range(n_eval):
            expl = self.explain_sample(test_sequences[i], nsamples=30)
            explanations.append({
                "sample_index": int(i),
                "predicted_risk": expl["predicted_risk_T1"],
                "top_drivers": expl["top_risk_drivers"],
                "feature_contributions": expl["feature_contributions"],
            })

        summary = {
            "explainer_type": self.explainer_type,
            "num_evaluated_samples": n_eval,
            "features_analyzed": self.feature_names,
            "samples": explanations,
        }

        with open(out_p, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2)

        logger.info(f"Saved SHAP summary report -> {out_p}")
        return summary
