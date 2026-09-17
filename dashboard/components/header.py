"""SOC Dashboard Header and Styling Component."""

import streamlit as st
from datetime import datetime


def apply_custom_soc_styles():
    """Inject SOC dark theme styles with neon accents."""
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #0b0f19;
            color: #f3f4f6;
        }
        .soc-header {
            background: linear-gradient(90deg, #111827 0%, #1e293b 100%);
            border: 1px solid #1e293b;
            border-radius: 10px;
            padding: 1.2rem 1.5rem;
            margin-bottom: 1.5rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .metric-box {
            background: #111827;
            border: 1px solid #1f2937;
            border-radius: 8px;
            padding: 1rem;
            text-align: center;
        }
        .metric-title {
            font-size: 0.8rem;
            color: #9ca3af;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        .metric-value {
            font-size: 1.8rem;
            font-weight: 700;
            margin: 0.25rem 0;
        }
        .badge-synthetic {
            background: rgba(245, 158, 11, 0.15);
            color: #fbbf24;
            padding: 3px 8px;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: 600;
            border: 1px solid rgba(245, 158, 11, 0.3);
        }
        .badge-live {
            background: rgba(16, 185, 129, 0.15);
            color: #34d399;
            padding: 3px 8px;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: 600;
            border: 1px solid rgba(16, 185, 129, 0.3);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header(demo_mode: bool = True):
    apply_custom_soc_styles()
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(
            f"""
            <div style="display: flex; align-items: center; gap: 12px;">
                <h1 style="margin: 0; font-size: 1.8rem; background: linear-gradient(135deg, #38bdf8, #818cf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                    SENTINEL-X SOC
                </h1>
                <span class="{'badge-synthetic' if demo_mode else 'badge-live'}">
                    {'DEMO / SYNTHETIC DATA' if demo_mode else 'LIVE CIC-IDS DATA'}
                </span>
            </div>
            <p style="margin: 4px 0 0 0; color: #9ca3af; font-size: 0.85rem;">
                Defensive Network Attack Forecasting System &bull; SIH26153 B.Tech Minor Project
            </p>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.markdown(
            f"""
            <div style="text-align: right; color: #6b7280; font-size: 0.8rem; margin-top: 8px;">
                <div>STATUS: <span style="color: #10b981; font-weight: 600;">ACTIVE DEFENSE</span></div>
                <div>LOCAL TIME: {now_str}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown("<hr style='border-color: #1f2937; margin: 1rem 0 1.5rem 0;'>", unsafe_allow_html=True)
