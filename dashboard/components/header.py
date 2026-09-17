"""Dashboard Header and Style Component for Sentinel-X."""

import streamlit as st
from datetime import datetime


def apply_custom_soc_styles():
    """Apply clean, restrained CSS styles suitable for an academic B.Tech project."""
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #0b0f19;
            color: #e2e8f0;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        }
        .header-container {
            border-bottom: 1px solid #1e293b;
            padding-bottom: 1rem;
            margin-bottom: 1.5rem;
        }
        .project-title {
            font-size: 1.6rem;
            font-weight: 700;
            color: #38bdf8;
            margin: 0;
            letter-spacing: -0.01em;
        }
        .project-subtitle {
            font-size: 0.9rem;
            color: #94a3b8;
            margin-top: 0.25rem;
        }
        .mode-badge-demo {
            display: inline-block;
            background: #451a03;
            color: #f59e0b;
            border: 1px solid #78350f;
            padding: 3px 10px;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: 600;
            letter-spacing: 0.05em;
            text-transform: uppercase;
        }
        .mode-badge-model {
            display: inline-block;
            background: #064e3b;
            color: #34d399;
            border: 1px solid #065f46;
            padding: 3px 10px;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: 600;
            letter-spacing: 0.05em;
            text-transform: uppercase;
        }
        .stat-card {
            background: #111827;
            border: 1px solid #1f2937;
            border-radius: 6px;
            padding: 0.85rem 1rem;
            text-align: left;
        }
        .stat-label {
            font-size: 0.75rem;
            color: #94a3b8;
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }
        .stat-value {
            font-size: 1.5rem;
            font-weight: 600;
            color: #f8fafc;
            margin-top: 0.2rem;
        }
        .disclaimer-note {
            font-size: 0.75rem;
            color: #64748b;
            margin-top: 0.5rem;
            font-style: italic;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header(demo_mode: bool = True, scenario_name: str = ""):
    """Render top header bar with mode badges and system status."""
    apply_custom_soc_styles()
    
    col_left, col_right = st.columns([3, 1])
    
    with col_left:
        st.markdown(
            f"""
            <div class="header-container">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span class="project-title">Sentinel-X</span>
                    <span class="{'mode-badge-demo' if demo_mode else 'mode-badge-model'}">
                        {'Demo Mode — Synthetic Traffic' if demo_mode else 'Model Mode — Test Dataset'}
                    </span>
                </div>
                <div class="project-subtitle">
                    AI-Based Network Attack Forecasting from Network Traffic Data &bull; SIH26153 B.Tech Minor Project
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
    with col_right:
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        st.markdown(
            f"""
            <div style="text-align: right; color: #64748b; font-size: 0.8rem; padding-top: 0.25rem;">
                <div>Execution: <strong style="color: #94a3b8;">Local / Offline</strong></div>
                <div>System Clock: <span style="color: #cbd5e1;">{now_str}</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
