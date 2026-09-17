"""Comparative evaluation engine comparing Baseline Logistic Regression vs. LSTM World Model."""

from pathlib import Path
from typing import Dict, Any, Optional
import json
import pandas as pd
import numpy as np

from sentinel_x.config import PROJECT_ROOT, load_config


def generate_comparison_summary(
    baseline_metrics_path: Optional[Path | str] = None,
    lstm_metrics_path: Optional[Path | str] = None,
    output_json_path: Optional[Path | str] = None,
    output_csv_path: Optional[Path | str] = None,
) -> Dict[str, Any]:
    """Load baseline and LSTM metrics, calculate relative advantages, and save comparison tables."""
    b_path = Path(baseline_metrics_path) if baseline_metrics_path else PROJECT_ROOT / "models" / "evaluation" / "baseline_metrics.json"
    l_path = Path(lstm_metrics_path) if lstm_metrics_path else PROJECT_ROOT / "models" / "evaluation" / "lstm_metrics.json"

    if not b_path.is_file():
        raise FileNotFoundError(f"Baseline metrics not found at {b_path}. Train baseline first.")
    if not l_path.is_file():
        raise FileNotFoundError(f"LSTM metrics not found at {l_path}. Train LSTM World Model first.")

    with open(b_path, "r", encoding="utf-8") as f:
        b_data = json.load(f)
    with open(l_path, "r", encoding="utf-8") as f:
        l_data = json.load(f)

    b_risk = b_data["metrics"]
    l_multi = l_data["multistep_evaluation"]

    # Comparative table rows
    comparison_rows = [
        {
            "Model": "Baseline Logistic Regression (Static)",
            "Forecast Horizon": "Static (T)",
            "Risk Precision": round(float(b_risk["precision"]), 4),
            "Risk Recall": round(float(b_risk["recall"]), 4),
            "Risk F1-Score": round(float(b_risk["f1_score"]), 4),
            "False Positive Rate": round(float(b_risk["false_positive_rate"]), 4),
            "Stage Accuracy": None,
            "State Forecast MAE": None,
        }
    ]

    for horizon in ["T+1", "T+2", "T+3"]:
        h_data = l_multi[horizon]
        r = h_data["risk_metrics"]
        st = h_data["stage_metrics"]
        se = h_data["state_metrics"]

        comparison_rows.append({
            "Model": "LSTM World Model (Deep Recurrent)",
            "Forecast Horizon": horizon,
            "Risk Precision": round(float(r["precision"]), 4),
            "Risk Recall": round(float(r["recall"]), 4),
            "Risk F1-Score": round(float(r["f1_score"]), 4),
            "False Positive Rate": round(float(r["false_positive_rate"]), 4),
            "Stage Accuracy": round(float(st["accuracy"]), 4),
            "State Forecast MAE": round(float(se["mae"]), 4),
        })

    comp_df = pd.DataFrame(comparison_rows)

    # Relative Advantage analysis (Baseline vs LSTM T+1)
    lstm_t1 = l_multi["T+1"]
    recall_gain = float(lstm_t1["risk_metrics"]["recall"]) - float(b_risk["recall"])
    fpr_reduction = float(b_risk["false_positive_rate"]) - float(lstm_t1["risk_metrics"]["false_positive_rate"])

    analysis = {
        "summary_table": comparison_rows,
        "key_findings": {
            "recall_advantage": round(recall_gain, 4),
            "fpr_improvement": round(fpr_reduction, 4),
            "multi_stage_capability": "Supported exclusively by LSTM World Model (5-stage MITRE taxonomy)",
            "multi_step_trajectory": "Supported exclusively by LSTM World Model (T+1, T+2, T+3 autoregressive rollout)",
        },
    }

    if output_json_path:
        out_j = Path(output_json_path)
        out_j.parent.mkdir(parents=True, exist_ok=True)
        with open(out_j, "w", encoding="utf-8") as f:
            json.dump(analysis, f, indent=2)

    if output_csv_path:
        out_c = Path(output_csv_path)
        out_c.parent.mkdir(parents=True, exist_ok=True)
        comp_df.to_csv(out_c, index=False)

    return analysis
