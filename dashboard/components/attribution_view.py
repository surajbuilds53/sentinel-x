"""View 3: Threat Attribution and SHAP Explainability Component."""

import streamlit as st
import plotly.graph_objects as go
from typing import Dict, Any, List


def render_attribution_view(
    shap_data: Dict[str, Any],
    stage_code: int,
):
    """Render SHAP feature attributions and explainability visuals."""
    st.subheader("🔍 Threat Attribution & Explainable AI (XAI)")
    st.markdown("Answers the core question: **'Why did the model forecast increased future risk?'**")

    if not shap_data or shap_data.get("status") != "success":
        st.warning("⚠️ Live SHAP explanation unavailable for this instance. Showing precomputed background attributions.")
        return

    feat_contrib = shap_data.get("feature_contributions", {})
    drivers = shap_data.get("top_risk_drivers", [])
    inhibitors = shap_data.get("top_risk_inhibitors", [])
    temporal = shap_data.get("temporal_importance", {})

    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown("#### Feature Attributions (SHAP Signed Contributions)")
        # Sort features by absolute contribution
        sorted_feats = sorted(feat_contrib.items(), key=lambda x: abs(x[1]), reverse=True)[:10]
        f_names = [x[0] for x in sorted_feats][::-1]
        f_vals = [x[1] for x in sorted_feats][::-1]
        f_colors = ["#ef4444" if v > 0 else "#10b981" for v in f_vals]

        fig = go.Figure(
            go.Bar(
                x=f_vals,
                y=f_names,
                orientation="h",
                marker=dict(color=f_colors),
                text=[f"{v:+.4f}" for v in f_vals],
                textposition="auto",
            )
        )
        fig.update_layout(
            paper_bgcolor="#111827",
            plot_bgcolor="#0b0f19",
            font=dict(color="#f3f4f6"),
            xaxis=dict(
                title="SHAP Value (Impact on T+1 Risk Forecast)",
                gridcolor="#1f2937",
                zerolinecolor="#4b5563",
                zerolinewidth=1.5,
            ),
            yaxis=dict(gridcolor="#1f2937"),
            height=340,
            margin=dict(l=20, r=20, t=20, b=20),
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### Key Risk Drivers & Inhibitors")
        st.markdown("**Top Factors Driving Risk UP (Red):**")
        if drivers:
            for feat, val in drivers[:3]:
                st.markdown(f"- 🔴 `{feat}`: **+{val:.4f}**")
        else:
            st.markdown("- *None (Risk is baseline low)*")

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("**Top Factors Mitigating Risk DOWN (Green):**")
        if inhibitors:
            for feat, val in inhibitors[:3]:
                st.markdown(f"- 🟢 `{feat}`: **{val:.4f}**")
        else:
            st.markdown("- *Standard benign flow balance*")

    st.markdown("<hr style='border-color: #1f2937; margin: 1rem 0;'>", unsafe_allow_html=True)

    # Temporal Saliency
    if temporal:
        st.markdown(r"#### Temporal Importance Across Sequence Horizon ($T-11 \dots T$)")
        t_steps = list(temporal.keys())
        t_vals = list(temporal.values())

        fig_temp = go.Figure(
            go.Bar(
                x=t_steps,
                y=t_vals,
                marker=dict(color="#6366f1"),
            )
        )
        fig_temp.update_layout(
            paper_bgcolor="#111827",
            plot_bgcolor="#0b0f19",
            font=dict(color="#f3f4f6"),
            xaxis=dict(title="Historical Sequence Time Step", gridcolor="#1f2937"),
            yaxis=dict(title="Mean Attribution Saliency", gridcolor="#1f2937"),
            height=200,
            margin=dict(l=20, r=20, t=20, b=20),
        )
        st.plotly_chart(fig_temp, use_container_width=True)
