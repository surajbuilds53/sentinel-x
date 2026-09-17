"""View 5: Data Pipeline and System Status Component."""

import streamlit as st
import platform
import torch
from pathlib import Path
from datetime import datetime

from sentinel_x.config import PROJECT_ROOT, load_config


def render_system_view(demo_mode: bool = True):
    """Render system diagnostics, dataset metadata, and environment specifications."""
    st.subheader("🖥️ Data Pipeline & System Status")

    config = load_config()

    # Hardware Info
    cuda_avail = torch.cuda.is_available()
    gpu_name = torch.cuda.get_device_name(0) if cuda_avail else "Not Available (CPU Execution)"
    total_ram = f"{torch.cuda.get_device_properties(0).total_memory / (1024**3):.2f} GB" if cuda_avail else "Host RAM"

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            f"""
            <div class="metric-box">
                <div class="metric-title">COMPUTE DEVICE</div>
                <div class="metric-value" style="color: {'#34d399' if cuda_avail else '#38bdf8'}; font-size: 1.3rem;">
                    {'NVIDIA CUDA' if cuda_avail else 'INTEL/AMD CPU'}
                </div>
                <div style="font-size: 0.75rem; color: #9ca3af;">{gpu_name}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c2:
        dataset_name = "Synthetic Demo Stream (6,000 flows)" if demo_mode else "CIC-IDS-2017/2018 Benchmark"
        st.markdown(
            f"""
            <div class="metric-box">
                <div class="metric-title">ACTIVE DATASET</div>
                <div class="metric-value" style="color: #f59e0b; font-size: 1.3rem;">
                    {'DEMO MODE' if demo_mode else 'LIVE BENCHMARK'}
                </div>
                <div style="font-size: 0.75rem; color: #9ca3af;">{dataset_name}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            f"""
            <div class="metric-box">
                <div class="metric-title">PROJECT VERSION</div>
                <div class="metric-value" style="color: #a78bfa; font-size: 1.3rem;">
                    v1.0.0 (SIH26153)
                </div>
                <div style="font-size: 0.75rem; color: #9ca3af;">Python {platform.python_version()} &bull; PyTorch {torch.__version__}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("#### Model Checkpoint Artifacts")
    b_path = PROJECT_ROOT / "models" / "checkpoints" / "baseline_logistic_regression.joblib"
    l_path = PROJECT_ROOT / "models" / "checkpoints" / "best_lstm_world_model.pt"
    s_path = PROJECT_ROOT / "models" / "scalers" / "lstm_state_scaler.joblib"

    artifacts = [
        {
            "Artifact": "LSTM World Model Checkpoint",
            "Path": str(l_path.relative_to(PROJECT_ROOT)),
            "Status": "✅ READY" if l_path.is_file() else "❌ MISSING",
            "Size": f"{l_path.stat().st_size / 1024:.1f} KB" if l_path.is_file() else "-",
        },
        {
            "Artifact": "Baseline Logistic Regression",
            "Path": str(b_path.relative_to(PROJECT_ROOT)),
            "Status": "✅ READY" if b_path.is_file() else "❌ MISSING",
            "Size": f"{b_path.stat().st_size / 1024:.1f} KB" if b_path.is_file() else "-",
        },
        {
            "Artifact": "StandardScaler Object",
            "Path": str(s_path.relative_to(PROJECT_ROOT)),
            "Status": "✅ READY" if s_path.is_file() else "❌ MISSING",
            "Size": f"{s_path.stat().st_size / 1024:.1f} KB" if s_path.is_file() else "-",
        },
    ]
    st.table(artifacts)
