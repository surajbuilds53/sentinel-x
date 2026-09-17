"""View 4: Model Performance & Comparative Benchmark Component."""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import json
from pathlib import Path

from sentinel_x.config import PROJECT_ROOT


def render_performance_view():
    """Render comprehensive model comparison and multi-step metrics."""
    st.subheader("📊 Model Performance: Baseline vs. Deep LSTM World Model")

    comp_path = PROJECT_ROOT / "models" / "evaluation" / "model_comparison.json"
    if not comp_path.is_file():
        st.warning("⚠️ Comparative evaluation report not found. Run 'python scripts/evaluate.py' to generate it.")
        return

    with open(comp_path, "r", encoding="utf-8") as f:
        comp_data = json.load(f)

    summary_table = comp_data.get("summary_table", [])
    df = pd.DataFrame(summary_table)

    st.markdown("#### Comparative Benchmark Summary")
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2 = st.columns([1, 1])

    with c1:
        st.markdown(r"#### Multi-Step Risk Metrics Across Horizon ($T+1 \dots T+3$)")
        horizons = ["T+1", "T+2", "T+3"]
        lstm_rows = [r for r in summary_table if r["Model"].startswith("LSTM")]

        precisions = [r["Risk Precision"] for r in lstm_rows]
        recalls = [r["Risk Recall"] for r in lstm_rows]
        f1_scores = [r["Risk F1-Score"] for r in lstm_rows]

        fig = go.Figure()
        fig.add_trace(go.Bar(x=horizons, y=precisions, name="Precision", marker_color="#38bdf8"))
        fig.add_trace(go.Bar(x=horizons, y=recalls, name="Recall", marker_color="#34d399"))
        fig.add_trace(go.Bar(x=horizons, y=f1_scores, name="F1-Score", marker_color="#818cf8"))

        fig.update_layout(
            barmode="group",
            paper_bgcolor="#111827",
            plot_bgcolor="#0b0f19",
            font=dict(color="#f3f4f6"),
            yaxis=dict(range=[0.8, 1.05], gridcolor="#1f2937", tickformat=".0%"),
            xaxis=dict(gridcolor="#1f2937"),
            height=300,
            margin=dict(l=20, r=20, t=20, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        )
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.markdown(r"#### Forecast Degradation Curves ($T+1 \dots T+3$)")
        stage_accs = [r["Stage Accuracy"] * 100 for r in lstm_rows]
        state_maes = [r["State Forecast MAE"] for r in lstm_rows]

        fig2 = go.Figure()
        fig2.add_trace(
            go.Scatter(
                x=horizons,
                y=stage_accs,
                name="Stage Accuracy (%)",
                line=dict(color="#f59e0b", width=3),
                marker=dict(size=8),
            )
        )
        fig2.add_trace(
            go.Scatter(
                x=horizons,
                y=state_maes,
                name="State Forecast MAE",
                yaxis="y2",
                line=dict(color="#ec4899", width=3, dash="dash"),
                marker=dict(size=8),
            )
        )

        fig2.update_layout(
            paper_bgcolor="#111827",
            plot_bgcolor="#0b0f19",
            font=dict(color="#f3f4f6"),
            xaxis=dict(gridcolor="#1f2937"),
            yaxis=dict(title="Stage Accuracy (%)", gridcolor="#1f2937", range=[50, 100]),
            yaxis2=dict(
                title="State MAE",
                overlaying="y",
                side="right",
                gridcolor="#1f2937",
                range=[0.5, 1.5],
            ),
            height=300,
            margin=dict(l=20, r=20, t=20, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        )
        st.plotly_chart(fig2, use_container_width=True)
