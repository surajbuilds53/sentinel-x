"""View 1: Executive Risk Dashboard Component."""

import streamlit as st
import plotly.graph_objects as go
from typing import Dict, Any

from sentinel_x.taxonomy.mitre_mapping import get_stage_metadata


def create_risk_gauge(risk_value: float, title: str = "Forecasted Risk (T+1)") -> go.Figure:
    """Create a cyber-style gauge chart for risk probability in [0, 1]."""
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number+delta",
            value=float(risk_value) * 100,
            domain={"x": [0, 1], "y": [0, 1]},
            title={"text": title, "font": {"size": 16, "color": "#f3f4f6"}},
            number={"suffix": "%", "font": {"size": 28, "color": "#f3f4f6"}},
            gauge={
                "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "#6b7280"},
                "bar": {"color": "#38bdf8" if risk_value < 0.4 else "#f59e0b" if risk_value < 0.75 else "#ef4444"},
                "bgcolor": "#111827",
                "borderwidth": 1,
                "bordercolor": "#1f2937",
                "steps": [
                    {"range": [0, 40], "color": "rgba(16, 185, 129, 0.15)"},
                    {"range": [40, 75], "color": "rgba(245, 158, 11, 0.15)"},
                    {"range": [75, 100], "color": "rgba(239, 68, 68, 0.2)"},
                ],
                "threshold": {
                    "line": {"color": "#ef4444", "width": 3},
                    "thickness": 0.8,
                    "value": 75,
                },
            },
        )
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "#f3f4f6"},
        height=220,
        margin=dict(l=20, r=20, t=30, b=20),
    )
    return fig


def render_executive_view(
    current_risk: float,
    forecast_risks: list,
    predicted_stage_code: int,
    stage_confidence: float = 0.85,
):
    """Render the Executive Risk View."""
    st.subheader("🛡️ Executive Risk & Attack Stage Overview")

    r_t1 = forecast_risks[0] if len(forecast_risks) > 0 else current_risk
    r_t2 = forecast_risks[1] if len(forecast_risks) > 1 else r_t1
    r_t3 = forecast_risks[2] if len(forecast_risks) > 2 else r_t2

    # Trend calculation
    trend_delta = r_t3 - current_risk
    if trend_delta > 0.05:
        trend_label = "INCREASING (ELEVATED THREAT)"
        trend_color = "#ef4444"
        trend_arrow = "▲"
    elif trend_delta < -0.05:
        trend_label = "DECREASING (DE-ESCALATING)"
        trend_color = "#10b981"
        trend_arrow = "▼"
    else:
        trend_label = "STABLE"
        trend_color = "#38bdf8"
        trend_arrow = "—"

    # Metric summary cards
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric(label="Observed Risk (T)", value=f"{current_risk:.1%}")
    with c2:
        st.metric(label="Forecast Risk (T+1)", value=f"{r_t1:.1%}", delta=f"{(r_t1 - current_risk):+.1%}")
    with c3:
        st.metric(label="Forecast Risk (T+2)", value=f"{r_t2:.1%}", delta=f"{(r_t2 - r_t1):+.1%}")
    with c4:
        st.metric(label="Forecast Risk (T+3)", value=f"{r_t3:.1%}", delta=f"{(r_t3 - r_t2):+.1%}")

    st.markdown("<br>", unsafe_allow_html=True)

    # Gauges and Stage Attribution
    g_col, s_col = st.columns([1, 1])

    with g_col:
        st.plotly_chart(create_risk_gauge(r_t1, title="Forecasted Risk Probability (T+1)"), use_container_width=True)

    with s_col:
        stage_meta = get_stage_metadata(predicted_stage_code)
        st.markdown(
            f"""
            <div style="background: #111827; border: 1px solid #1f2937; border-left: 4px solid {stage_meta['color']}; border-radius: 8px; padding: 1.2rem; height: 220px; display: flex; flex-direction: column; justify-content: center;">
                <div style="font-size: 0.8rem; color: #9ca3af; text-transform: uppercase; letter-spacing: 0.05em;">
                    MITRE ATT&CK Behavioral Stage
                </div>
                <div style="font-size: 1.4rem; font-weight: 700; color: {stage_meta['color']}; margin: 0.3rem 0;">
                    {stage_meta['label']}
                </div>
                <div style="font-size: 0.85rem; color: #d1d5db; line-height: 1.4; margin-bottom: 0.5rem;">
                    {stage_meta['description']}
                </div>
                <div style="display: flex; gap: 1rem; font-size: 0.8rem; color: #9ca3af;">
                    <span>TACTIC: <strong style="color: #f3f4f6;">{stage_meta['tactic_id']}</strong></span>
                    <span>CONFIDENCE: <strong style="color: #f3f4f6;">{stage_confidence:.1%}</strong></span>
                    <span>TREND: <strong style="color: {trend_color};">{trend_arrow} {trend_label}</strong></span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
