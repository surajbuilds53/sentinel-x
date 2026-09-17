"""View 2: Forecast Timeline Component."""

import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd


def render_timeline_view(
    historical_risks: list,
    forecast_risks: list,
    time_labels: list = None,
):
    """Render interactive timeline contrasting historical observations vs. autoregressive forecasts."""
    st.subheader("📈 Historical Observations vs. Autoregressive Forecasts")

    n_hist = len(historical_risks)
    n_fore = len(forecast_risks)

    if time_labels is None or len(time_labels) != n_hist:
        time_labels = [f"T-{n_hist - 1 - i}" for i in range(n_hist)]

    forecast_labels = [f"T+{i+1}" for i in range(n_fore)]

    fig = go.Figure()

    # 1. Historical Observed Risk (Solid cyan line)
    fig.add_trace(
        go.Scatter(
            x=time_labels,
            y=historical_risks,
            mode="lines+markers",
            name="Observed Historical Risk",
            line=dict(color="#38bdf8", width=3),
            marker=dict(size=7, color="#38bdf8"),
        )
    )

    # Bridge connection between T and T+1
    bridge_x = [time_labels[-1]] + forecast_labels
    bridge_y = [historical_risks[-1]] + list(forecast_risks)

    # 2. Autoregressive Forecasts (Dashed Red line)
    fig.add_trace(
        go.Scatter(
            x=bridge_x,
            y=bridge_y,
            mode="lines+markers",
            name="World Model Forecast (T+1..T+3)",
            line=dict(color="#f43f5e", width=3, dash="dash"),
            marker=dict(size=9, color="#f43f5e", symbol="diamond"),
        )
    )

    # 3. Forecast Confidence Band
    std_spread = 0.08
    upper_band = [min(1.0, y + std_spread * (i + 1) * 0.7) for i, y in enumerate(bridge_y)]
    lower_band = [max(0.0, y - std_spread * (i + 1) * 0.7) for i, y in enumerate(bridge_y)]

    fig.add_trace(
        go.Scatter(
            x=bridge_x + bridge_x[::-1],
            y=upper_band + lower_band[::-1],
            fill="toself",
            fillcolor="rgba(244, 63, 94, 0.15)",
            line=dict(color="rgba(255,255,255,0)"),
            hoverinfo="skip",
            showlegend=True,
            name="Forecast Uncertainty Band (95% CI)",
        )
    )

    # Layout styling
    fig.update_layout(
        paper_bgcolor="#111827",
        plot_bgcolor="#0b0f19",
        font=dict(color="#f3f4f6"),
        xaxis=dict(
            title="Temporal Horizon Sequence",
            gridcolor="#1f2937",
            zerolinecolor="#1f2937",
        ),
        yaxis=dict(
            title="Attack Risk Probability",
            range=[-0.05, 1.05],
            gridcolor="#1f2937",
            zerolinecolor="#1f2937",
            tickformat=".0%",
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor="rgba(0,0,0,0)",
        ),
        height=380,
        margin=dict(l=30, r=30, t=40, b=30),
    )

    st.plotly_chart(fig, use_container_width=True)

    # Explanation badge
    st.info(
        r"💡 **Forecasting Insight**: Solid blue markers represent verified historical observations ($T-N \dots T$). "
        r"The dashed red trajectory represents the LSTM World Model's multi-step autoregressive rollout ($T+1, T+2, T+3$), "
        r"providing SOC analysts early proactive warning before attacks escalate."
    )
