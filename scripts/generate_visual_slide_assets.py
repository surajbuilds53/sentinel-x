"""Generate high-resolution visual diagrams and infographics for Sentinel-X presentation slides.
All diagrams use clean padding, explicit text wrapping, and generous spacing to prevent
any box collisions, text collisions, or label overlaps.
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

OUT_DIR = r"docs/presentation_assets/v2"
os.makedirs(OUT_DIR, exist_ok=True)
BG_COLOR = "#FFF1CD"  # Warm ivory matching Buddha Institute template


def create_reactive_vs_predictive():
    """Slide 3: Reactive NIDS vs Sentinel-X Predictive Forecasting."""
    fig, ax = plt.subplots(figsize=(10.5, 4.3), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.axis("off")

    # Left: Traditional Reactive
    ax.add_patch(patches.FancyBboxPatch(
        (0.04, 0.08), 0.43, 0.84,
        boxstyle="round,pad=0.015,rounding_size=0.03",
        facecolor="#FEE2E2", edgecolor="#DC2626", linewidth=2.5
    ))
    ax.text(0.255, 0.84, "TRADITIONAL NIDS (REACTIVE)", ha="center", va="center", fontsize=11.5, fontweight="bold", color="#991B1B")

    steps_left = [
        ("Exploit Execution", "Attacker launches payload or scan"),
        ("Perimeter Breach", "System compromised, data exposed"),
        ("Delayed Alert", "Fires POST-COMPROMISE (Too late)"),
        ("Severe Impact", "High MTTD (207 days) & alert fatigue")
    ]
    y = 0.67
    for title, sub in steps_left:
        ax.text(0.07, y, f"• {title}:", fontsize=9.5, fontweight="bold", color="#7F1D1D")
        ax.text(0.09, y - 0.05, sub, fontsize=8.5, color="#334155")
        y -= 0.13

    # Right: Sentinel-X Predictive
    ax.add_patch(patches.FancyBboxPatch(
        (0.53, 0.08), 0.43, 0.84,
        boxstyle="round,pad=0.015,rounding_size=0.03",
        facecolor="#DCFCE7", edgecolor="#16A34A", linewidth=2.5
    ))
    ax.text(0.745, 0.84, "SENTINEL-X (PREDICTIVE FORECASTING)", ha="center", va="center", fontsize=11.5, fontweight="bold", color="#166534")

    steps_right = [
        ("Telemetry Tracking", "Monitors continuous 120s flow window"),
        ("World Model Rollout", "Forecasts 10s, 20s, 30s ahead"),
        ("Pre-Breach Warning", "Predicts risk & MITRE stage early"),
        ("Proactive Shielding", "10-30s buffer to push firewall ACLs")
    ]
    y = 0.67
    for title, sub in steps_right:
        ax.text(0.56, y, f"• {title}:", fontsize=9.5, fontweight="bold", color="#14532D")
        ax.text(0.58, y - 0.05, sub, fontsize=8.5, color="#334155")
        y -= 0.13

    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "diag_reactive_vs_predictive.png"), dpi=220)
    plt.close()


def create_pipeline_flowchart():
    """Slide 4: End-to-End System Pipeline (7-stage closed loop)."""
    fig, ax = plt.subplots(figsize=(11, 4.4), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.axis("off")

    stages_row1 = [
        ("1. Traffic Telemetry", "CIC-IDS / Real Flows\nPacket Capture", 0.03, 0.56, "#DBEAFE", "#1D4ED8"),
        ("2. 10s Aggregator", "16 State Features\nContinuous Dynamics", 0.28, 0.56, "#E0E7FF", "#4338CA"),
        ("3. Leak-Free Window", "Input: T-11...T (120s)\n70/15/15 Chrono Split", 0.53, 0.56, "#EDE9FE", "#6D28D9"),
        ("4. LSTM World Model", "2-Layer Recurrent\nHidden 128, Dropout 0.3", 0.78, 0.56, "#FEF3C7", "#D97706"),
    ]

    for title, desc, x, y, fc, ec in stages_row1:
        ax.add_patch(patches.FancyBboxPatch((x, y), 0.19, 0.36, boxstyle="round,pad=0.015,rounding_size=0.02", facecolor=fc, edgecolor=ec, linewidth=2))
        ax.text(x + 0.095, y + 0.25, title, ha="center", va="center", fontsize=9.5, fontweight="bold", color="#0F172A")
        ax.text(x + 0.095, y + 0.11, desc, ha="center", va="center", fontsize=8.2, color="#334155")

    # Arrows row 1 (left to right)
    ax.annotate("", xy=(0.275, 0.74), xytext=(0.225, 0.74), arrowprops=dict(arrowstyle="->", lw=2.5, color="#1E293B"))
    ax.annotate("", xy=(0.525, 0.74), xytext=(0.475, 0.74), arrowprops=dict(arrowstyle="->", lw=2.5, color="#1E293B"))
    ax.annotate("", xy=(0.775, 0.74), xytext=(0.725, 0.74), arrowprops=dict(arrowstyle="->", lw=2.5, color="#1E293B"))

    # Turn down arrow
    ax.annotate("", xy=(0.875, 0.50), xytext=(0.875, 0.56), arrowprops=dict(arrowstyle="->", lw=2.5, color="#1E293B"))

    stages_row2 = [
        ("7. SOC Dashboard", "5 Interactive Views\nLive Local Execution", 0.03, 0.10, "#CCFBF1", "#0F766E"),
        ("6. SHAP Explainability", "Signed Risk Drivers\n& Temporal Saliency", 0.28, 0.10, "#DCFCE7", "#15803D"),
        ("5. Multi-Step Rollout", "Autoregressive Loop\nT+1 -> T+2 -> T+3", 0.53, 0.10, "#FFE4E6", "#BE123C"),
        ("3 Forecast Heads", "Risk (BCE) | Stage (CE)\nState Reconstructor (MSE)", 0.78, 0.10, "#FEE2E2", "#B91C1C"),
    ]

    for title, desc, x, y, fc, ec in stages_row2:
        ax.add_patch(patches.FancyBboxPatch((x, y), 0.19, 0.36, boxstyle="round,pad=0.015,rounding_size=0.02", facecolor=fc, edgecolor=ec, linewidth=2))
        ax.text(x + 0.095, y + 0.25, title, ha="center", va="center", fontsize=9.5, fontweight="bold", color="#0F172A")
        ax.text(x + 0.095, y + 0.11, desc, ha="center", va="center", fontsize=8.2, color="#334155")

    # Arrows row 2 (right to left)
    ax.annotate("", xy=(0.725, 0.28), xytext=(0.775, 0.28), arrowprops=dict(arrowstyle="->", lw=2.5, color="#1E293B"))
    ax.annotate("", xy=(0.475, 0.28), xytext=(0.525, 0.28), arrowprops=dict(arrowstyle="->", lw=2.5, color="#1E293B"))
    ax.annotate("", xy=(0.225, 0.28), xytext=(0.275, 0.28), arrowprops=dict(arrowstyle="->", lw=2.5, color="#1E293B"))

    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "diag_pipeline_flowchart.png"), dpi=220)
    plt.close()


def create_16_features_grid():
    """Slide 5: 16 Continuous State Features Grid (Clean 4 Quadrants)."""
    fig, ax = plt.subplots(figsize=(10.5, 4.4), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.axis("off")

    cards = [
        ("VOLUMETRIC (5 Features)",
         ["flow_count", "total_packets", "packet_rate", "total_bytes", "byte_rate"],
         "Detects volumetric floods & exfiltration",
         0.03, 0.53, "#DBEAFE", "#1D4ED8"),

        ("TIMING & DURATION (3 Features)",
         ["duration_mean", "duration_std", "iat_mean (inter-arrival time)"],
         "Detects rapid scanning & botnet beacon pacing",
         0.52, 0.53, "#FEF3C7", "#D97706"),

        ("PACKET DYNAMICS (2 Features)",
         ["fwd_pkt_len_mean", "bwd_pkt_len_mean"],
         "Detects asymmetric payloads & auth handshakes",
         0.03, 0.06, "#DCFCE7", "#15803D"),

        ("FLAGS & PROTOCOLS (6 Features)",
         ["syn_ratio, rst_ratio", "ack_ratio, fin_ratio", "tcp_ratio, udp_ratio"],
         "Detects SYN scans, closed ports & flood vectors",
         0.52, 0.06, "#FEE2E2", "#B91C1C"),
    ]

    for title, feats, note, x, y, fc, ec in cards:
        ax.add_patch(patches.FancyBboxPatch(
            (x, y), 0.45, 0.41,
            boxstyle="round,pad=0.015,rounding_size=0.025",
            facecolor=fc, edgecolor=ec, linewidth=2
        ))
        ax.text(x + 0.025, y + 0.33, title, fontsize=10.5, fontweight="bold", color=ec)

        # Draw features inside box with tight, controlled spacing
        y_f = y + 0.24
        step = 0.044 if len(feats) > 3 else 0.062
        for f in feats:
            ax.text(x + 0.025, y_f, f"•  {f}", fontsize=8.5, fontfamily="monospace", fontweight="bold", color="#1E293B")
            y_f -= step

        ax.text(x + 0.025, y + 0.035, f"↳ {note}", fontsize=7.8, fontstyle="italic", color="#475569")

    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "diag_16_features_grid.png"), dpi=220)
    plt.close()


def create_chronological_split():
    """Slide 6: Leak-Free Chronological Partitioning & Sequence Window."""
    fig, ax = plt.subplots(figsize=(10.5, 4.3), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.axis("off")

    ax.text(0.5, 0.93, "LEAK-FREE CHRONOLOGICAL PARTITIONING (NO RANDOM SHUFFLE)", ha="center", va="center", fontsize=11, fontweight="bold", color="#1E3A8A")

    # Timeline bar
    ax.add_patch(patches.Rectangle((0.05, 0.66), 0.63, 0.16, facecolor="#93C5FD", edgecolor="#1D4ED8", linewidth=1.5))
    ax.text(0.365, 0.74, "TRAINING SET (Earliest 70%)\nStandardScaler fitted solely here", ha="center", va="center", fontsize=9, fontweight="bold", color="#1E3A8A")

    ax.add_patch(patches.Rectangle((0.68, 0.66), 0.14, 0.16, facecolor="#FDE68A", edgecolor="#D97706", linewidth=1.5))
    ax.text(0.75, 0.74, "VALIDATION\n(Middle 15%)", ha="center", va="center", fontsize=8.5, fontweight="bold", color="#78350F")

    ax.add_patch(patches.Rectangle((0.82, 0.66), 0.13, 0.16, facecolor="#BBF7D0", edgecolor="#15803D", linewidth=1.5))
    ax.text(0.885, 0.74, "HELD-OUT TEST\n(Latest 15%)", ha="center", va="center", fontsize=8.5, fontweight="bold", color="#14532D")

    # Rolling sequence illustration
    ax.text(0.5, 0.52, "ROLLING SEQUENCE WINDOW STRUCTURE", ha="center", va="center", fontsize=10.5, fontweight="bold", color="#0F172A")

    # History window box
    ax.add_patch(patches.FancyBboxPatch((0.07, 0.12), 0.53, 0.32, boxstyle="round,pad=0.015,rounding_size=0.02", facecolor="#E0E7FF", edgecolor="#4338CA", linewidth=2))
    ax.text(0.335, 0.34, "HISTORICAL CONTEXT WINDOW (N = 12 steps)", ha="center", va="center", fontsize=9.5, fontweight="bold", color="#312E81")
    ax.text(0.335, 0.22, "Input Sequence: [T-11, T-10, ..., T-1, T] = 120 Seconds (2 min)\nTensor Shape: [Batch Size, 12 timesteps, 16 features]", ha="center", va="center", fontsize=8.5, color="#1E1B4B")

    # Arrow to targets
    ax.annotate("", xy=(0.67, 0.28), xytext=(0.61, 0.28), arrowprops=dict(arrowstyle="->", lw=3, color="#DC2626"))

    # Forecast targets box
    ax.add_patch(patches.FancyBboxPatch((0.68, 0.12), 0.25, 0.32, boxstyle="round,pad=0.015,rounding_size=0.02", facecolor="#FEE2E2", edgecolor="#DC2626", linewidth=2))
    ax.text(0.805, 0.34, "FORECAST TARGETS (H = 3)", ha="center", va="center", fontsize=9.5, fontweight="bold", color="#991B1B")
    ax.text(0.805, 0.22, "T+1: Next 10 seconds\nT+2: Next 20 seconds\nT+3: Next 30 seconds", ha="center", va="center", fontsize=8.5, color="#7F1D1D")

    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "diag_chronological_split.png"), dpi=220)
    plt.close()


def create_world_model_diagram():
    """Slide 7: Deep LSTM World Model Architecture with Clean Clearance."""
    fig, ax = plt.subplots(figsize=(10.5, 4.3), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.axis("off")

    # Input Box
    ax.add_patch(patches.FancyBboxPatch((0.04, 0.28), 0.20, 0.44, boxstyle="round,pad=0.015,rounding_size=0.02", facecolor="#E2E8F0", edgecolor="#475569", linewidth=2))
    ax.text(0.14, 0.55, "INPUT SEQUENCE", ha="center", va="center", fontsize=10, fontweight="bold", color="#0F172A")
    ax.text(0.14, 0.44, "[Batch, 12, 16]\n12 Timesteps\n16 Features each", ha="center", va="center", fontsize=8.5, color="#334155")

    # Arrow from Input to LSTM
    ax.annotate("", xy=(0.31, 0.50), xytext=(0.25, 0.50), arrowprops=dict(arrowstyle="->", lw=2.5, color="#1E293B"))

    # LSTM Backbone Box
    ax.add_patch(patches.FancyBboxPatch((0.32, 0.24), 0.25, 0.52, boxstyle="round,pad=0.015,rounding_size=0.02", facecolor="#DBEAFE", edgecolor="#1D4ED8", linewidth=2.2))
    ax.text(0.445, 0.63, "LSTM BACKBONE", ha="center", va="center", fontsize=10.5, fontweight="bold", color="#1E3A8A")
    ax.text(0.445, 0.48, "• 2-Layer LSTM\n• Hidden Size: 128\n• Dropout: 0.30\n• Latent State: h_T [128]", ha="center", va="center", fontsize=8.5, color="#1E293B")

    # 3 Heads on Right
    # Head 1: Risk Head
    ax.add_patch(patches.FancyBboxPatch((0.66, 0.67), 0.30, 0.26, boxstyle="round,pad=0.015,rounding_size=0.02", facecolor="#FEE2E2", edgecolor="#DC2626", linewidth=2))
    ax.text(0.81, 0.83, "Risk Prediction Head", ha="center", va="center", fontsize=9.5, fontweight="bold", color="#991B1B")
    ax.text(0.81, 0.73, "Linear(128→32) → Sigmoid\nOutput: Risk Score r ∈ [0, 1] (BCE)", ha="center", va="center", fontsize=8, color="#7F1D1D")

    # Head 2: Stage Head
    ax.add_patch(patches.FancyBboxPatch((0.66, 0.37), 0.30, 0.26, boxstyle="round,pad=0.015,rounding_size=0.02", facecolor="#FEF3C7", edgecolor="#D97706", linewidth=2))
    ax.text(0.81, 0.53, "MITRE Stage Head", ha="center", va="center", fontsize=9.5, fontweight="bold", color="#92400E")
    ax.text(0.81, 0.43, "Linear(128→64) → Softmax\nOutput: 5 Stage Classes (CCE)", ha="center", va="center", fontsize=8, color="#78350F")

    # Head 3: State Reconstructor Head
    ax.add_patch(patches.FancyBboxPatch((0.66, 0.07), 0.30, 0.26, boxstyle="round,pad=0.015,rounding_size=0.02", facecolor="#DCFCE7", edgecolor="#15803D", linewidth=2))
    ax.text(0.81, 0.23, "State Head (World Model)", ha="center", va="center", fontsize=9.5, fontweight="bold", color="#14532D")
    ax.text(0.81, 0.13, "Linear(128→64→16) (MSE)\nPredicted State s_{t+1} ∈ R^16", ha="center", va="center", fontsize=8, color="#166534")

    # Branching arrows from LSTM to heads
    ax.annotate("", xy=(0.65, 0.78), xytext=(0.58, 0.56), arrowprops=dict(arrowstyle="->", lw=2, color="#DC2626"))
    ax.annotate("", xy=(0.65, 0.50), xytext=(0.58, 0.50), arrowprops=dict(arrowstyle="->", lw=2, color="#D97706"))
    ax.annotate("", xy=(0.65, 0.22), xytext=(0.58, 0.44), arrowprops=dict(arrowstyle="->", lw=2, color="#15803D"))

    # Autoregressive feedback loop (curves cleanly below without cutting text)
    ax.annotate("Autoregressive Feedback: s_{t+1} fed back for T+2, T+3",
                xy=(0.445, 0.23), xytext=(0.66, 0.02),
                arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=-0.25", lw=2.2, color="#2563EB"),
                fontsize=8, fontweight="bold", color="#1D4ED8", ha="center")

    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "diag_world_model.png"), dpi=220)
    plt.close()


def create_rollout_loss_diagram():
    """Slide 8: Autoregressive Rollout & Multi-Task Loss Formulation."""
    fig, ax = plt.subplots(figsize=(10.5, 4.3), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.axis("off")

    # Column 1 Header
    ax.text(0.245, 0.94, "AUTOREGRESSIVE MULTI-STEP ROLLOUT", ha="center", va="center", fontsize=10.5, fontweight="bold", color="#1E3A8A")

    # 3 Steps with generous vertical clearance
    steps_left = [
        ("STEP 1: T+1 (Next 10s)", "Input: [T-11 ... T]", "Output: s_{T+1}, Risk r_{T+1}, Stage c_{T+1}", 0.67, "#DBEAFE", "#1D4ED8", "#1E3A8A"),
        ("STEP 2: T+2 (Next 20s)", "Input: [T-10 ... T, s_{T+1}]", "Output: s_{T+2}, Risk r_{T+2}, Stage c_{T+2}", 0.38, "#FEF3C7", "#D97706", "#92400E"),
        ("STEP 3: T+3 (Next 30s)", "Input: [T-9 ... s_{T+1}, s_{T+2}]", "Output: s_{T+3}, Risk r_{T+3}, Stage c_{T+3}", 0.09, "#FEE2E2", "#DC2626", "#991B1B"),
    ]

    for title, inp, out, y, fc, ec, tc in steps_left:
        ax.add_patch(patches.FancyBboxPatch((0.03, y), 0.43, 0.22, boxstyle="round,pad=0.012,rounding_size=0.02", facecolor=fc, edgecolor=ec, linewidth=2))
        ax.text(0.245, y + 0.165, title, ha="center", va="center", fontsize=9.5, fontweight="bold", color=tc)
        ax.text(0.245, y + 0.10, inp, ha="center", va="center", fontsize=8.2, color="#1E293B")
        ax.text(0.245, y + 0.045, out, ha="center", va="center", fontsize=8.0, color="#1E293B")

    # Downward connecting arrows with clear space
    ax.annotate("", xy=(0.245, 0.615), xytext=(0.245, 0.665), arrowprops=dict(arrowstyle="->", lw=2.5, color="#1D4ED8"))
    ax.annotate("", xy=(0.245, 0.325), xytext=(0.245, 0.375), arrowprops=dict(arrowstyle="->", lw=2.5, color="#D97706"))

    # Column 2 Header
    ax.text(0.735, 0.94, "WEIGHTED MULTI-TASK LOSS", ha="center", va="center", fontsize=10.5, fontweight="bold", color="#1E3A8A")

    # Formula Box
    ax.add_patch(patches.FancyBboxPatch((0.50, 0.70), 0.47, 0.19, boxstyle="round,pad=0.012,rounding_size=0.02", facecolor="#EDE9FE", edgecolor="#6D28D9", linewidth=2))
    ax.text(0.735, 0.795, r"$\mathcal{L}_{total} = 1.0 \cdot \mathcal{L}_{BCE} + 1.0 \cdot \mathcal{L}_{CE} + 0.2 \cdot \mathcal{L}_{MSE}$", ha="center", va="center", fontsize=9.2, fontweight="bold", color="#4C1D95")

    losses = [
        ("1. Risk Loss (w = 1.0): Binary Cross-Entropy", "Penalizes missed attack probability vs benign traffic", 0.49, "#FEE2E2", "#DC2626", "#991B1B"),
        ("2. Stage Loss (w = 1.0): Categorical Cross-Entropy", "Supervises progression across 5 MITRE behavioral stages", 0.28, "#FEF3C7", "#D97706", "#92400E"),
        ("3. Auxiliary State Loss (w = 0.2): Mean Squared Error", "Forces LSTM to learn real physics of 16 continuous signals", 0.07, "#DCFCE7", "#15803D", "#14532D"),
    ]
    for title, desc, y, fc, ec, tc in losses:
        ax.add_patch(patches.FancyBboxPatch((0.50, y), 0.47, 0.18, boxstyle="round,pad=0.012,rounding_size=0.02", facecolor=fc, edgecolor=ec, linewidth=1.5))
        ax.text(0.52, y + 0.115, title, fontsize=8.8, fontweight="bold", color=tc)
        ax.text(0.52, y + 0.05, desc, fontsize=7.8, color="#475569")

    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "diag_rollout_loss.png"), dpi=220)
    plt.close()


def create_mitre_chevrons():
    """Slide 9: 5-Stage MITRE ATT&CK Lifecycle Chevrons with Clean Gaps."""
    fig, ax = plt.subplots(figsize=(10.5, 4.3), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.axis("off")

    stages = [
        ("STAGE 0\nBENIGN", "Normal Baseline", "High ACK (>0.85)\nNormal durations\nSteady traffic", "#D1FAE5", "#059669"),
        ("STAGE 1\nRECON (TA0043)", "Port Scanning", "SYN ratio > 0.5\nShort durations\nSpike in flow count", "#FEF3C7", "#D97706"),
        ("STAGE 2\nINITIAL ACCESS", "Brute Force (TA0001)", "Repeated auth tries\nHigh byte rates\nSSH/FTP Patator", "#FED7AA", "#EA580C"),
        ("STAGE 3\nLATERAL MOVE", "Subnet Pivot (TA0008)", "Bursty SMB/RDP\nInternal traversal\nTraffic expansion", "#FECDD3", "#E11D48"),
        ("STAGE 4\nCOMMAND & CTRL", "C2 Beacon (TA0011)", "Periodic IAT pulses\nHeartbeat channels\nRigid time intervals", "#FEE2E2", "#DC2626"),
    ]

    x = 0.02
    w = 0.165
    step = 0.198
    for title, sub, desc, fc, ec in stages:
        ax.add_patch(patches.FancyBboxPatch((x, 0.10), w, 0.80, boxstyle="round,pad=0.012,rounding_size=0.025", facecolor=fc, edgecolor=ec, linewidth=2))
        ax.text(x + w/2, 0.77, title, ha="center", va="center", fontsize=9.2, fontweight="bold", color=ec)
        ax.text(x + w/2, 0.63, sub, ha="center", va="center", fontsize=8.8, fontweight="bold", color="#0F172A")
        ax.text(x + w/2, 0.36, desc, ha="center", va="center", fontsize=8.2, color="#334155")

        if x < 0.75:
            ax.annotate("", xy=(x + w + 0.024, 0.50), xytext=(x + w + 0.006, 0.50), arrowprops=dict(arrowstyle="->", lw=2, color="#475569"))
        x += step

    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "diag_mitre_chevrons.png"), dpi=220)
    plt.close()


def create_shap_force():
    """Slide 10: Signed SHAP Threat Attribution & Temporal Saliency."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.5, 4.3), facecolor=BG_COLOR, gridspec_kw={"width_ratios": [1.4, 1.0]})
    ax1.set_facecolor("#FFF8E7")
    ax2.set_facecolor("#FFF8E7")

    # Left: Signed feature attribution
    features = ["syn_ratio", "packet_rate", "rst_ratio", "tot_fwd_bytes", "flow_count", "iat_mean", "duration_mean", "ack_ratio"]
    vals = [0.3547, 0.2463, 0.1610, 0.1394, 0.0912, -0.0520, -0.0845, -0.1299]
    colors = ["#DC2626" if v > 0 else "#16A34A" for v in vals]

    y_pos = np.arange(len(features))
    ax1.barh(y_pos, vals, color=colors, edgecolor="#1E293B", height=0.65)
    ax1.set_yticks(y_pos)
    ax1.set_yticklabels(features, fontsize=9.5, fontweight="bold")
    ax1.tick_params(axis='y', pad=8)
    ax1.axvline(0, color="#475569", linewidth=1.5)
    ax1.set_xlabel("SHAP Impact on T+1 Forecast Risk", fontsize=9.5, fontweight="bold")
    ax1.set_title("Signed Threat Attribution (Drivers vs. Inhibitors)", fontsize=10.5, fontweight="bold", color="#1E3A8A")
    ax1.grid(axis="x", linestyle="--", alpha=0.5)
    ax1.set_xlim(-0.22, 0.44)  # Generous left margin so negative text labels never overlap feature names!

    # Annotate labels
    for i, v in enumerate(vals):
        if v >= 0:
            ax1.text(v + 0.015, i, f"{v:+.2f}", va="center", ha="left", fontsize=8.5, fontweight="bold", color="#991B1B")
        else:
            # Place negative value cleanly with sufficient distance from y-tick
            ax1.text(v - 0.012, i, f"{v:+.2f}", va="center", ha="right", fontsize=8.5, fontweight="bold", color="#166534")

    # Right: Temporal Saliency
    t_steps = [f"T-{11-i}" for i in range(12)]
    t_vals = [0.03 + 0.12 * ((i+1)/12)**2 for i in range(12)]
    ax2.bar(t_steps, t_vals, color="#4338CA", edgecolor="#1E1B4B")
    ax2.set_title("Temporal Saliency (T-11 ... T)", fontsize=10.5, fontweight="bold", color="#1E3A8A")
    ax2.set_ylabel("Attribution Weight", fontsize=9)
    ax2.set_xticks(range(len(t_steps)))
    ax2.set_xticklabels(t_steps, rotation=45, fontsize=7.5)
    ax2.grid(axis="y", linestyle="--", alpha=0.5)

    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "diag_shap_force.png"), dpi=220)
    plt.close()


def create_future_pillars():
    """Slide 13: 3 Distinct Architectural Pillars with Crisp Spacing & Structured Bullets."""
    fig, ax = plt.subplots(figsize=(10.5, 4.3), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.axis("off")

    pillars = [
        ("PILLAR 01",
         "AUTOMATED SDN\nORCHESTRATION",
         [
             "Direct API linkage to OpenFlow / Ryu",
             "Pushes automated firewall ACL rules",
             "Pre-emptively drops malicious IPs",
             "Sub-second autonomous containment"
         ],
         "#DBEAFE", "#1D4ED8", "#1E3A8A"),

        ("PILLAR 02",
         "TEMPORAL GRAPH\nNETWORKS (T-GNN)",
         [
             "Models host-to-host lateral topology",
             "Captures subnet pivot escalation",
             "Graph embeddings + LSTM temporal",
             "Prevents multi-hop ransomware"
         ],
         "#EDE9FE", "#6D28D9", "#4C1D95"),

        ("PILLAR 03",
         "EDGE ROUTER\nQUANTIZATION",
         [
             "ONNX & TensorRT INT8 quantization",
             "Inference latency dropped to < 5 ms",
             "Deployable inside edge gateways",
             "Zero cloud dependency / green AI"
         ],
         "#DCFCE7", "#15803D", "#14532D"),
    ]

    col_x = [0.03, 0.36, 0.69]
    card_w = 0.28
    card_h = 0.86
    y_start = 0.07

    for idx, (badge, title, bullets, fc, ec, text_c) in enumerate(pillars):
        x = col_x[idx]

        # Main Pillar Card
        ax.add_patch(patches.FancyBboxPatch(
            (x, y_start), card_w, card_h,
            boxstyle="round,pad=0.012,rounding_size=0.025",
            facecolor=fc, edgecolor=ec, linewidth=2.2
        ))

        # Badge Pill
        ax.add_patch(patches.FancyBboxPatch(
            (x + 0.04, y_start + card_h - 0.09), card_w - 0.08, 0.065,
            boxstyle="round,pad=0.008,rounding_size=0.015",
            facecolor=ec, edgecolor=ec, linewidth=1
        ))
        ax.text(x + card_w/2, y_start + card_h - 0.057, badge, ha="center", va="center", fontsize=8.5, fontweight="bold", color="#FFFFFF")

        # Pillar Title
        ax.text(x + card_w/2, y_start + card_h - 0.19, title, ha="center", va="center", fontsize=10.2, fontweight="bold", color=text_c)

        # Subtle divider
        ax.plot([x + 0.03, x + card_w - 0.03], [y_start + card_h - 0.27, y_start + card_h - 0.27], color=ec, linewidth=1, linestyle="--", alpha=0.6)

        # Bullets
        y_b = y_start + card_h - 0.35
        for b in bullets:
            ax.text(x + 0.02, y_b, "✓", fontsize=8.5, fontweight="bold", color=ec)
            ax.text(x + 0.045, y_b, b, fontsize=8.2, fontweight="normal", color="#1E293B")
            y_b -= 0.115

    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "diag_future_pillars.png"), dpi=220)
    plt.close()


if __name__ == "__main__":
    create_reactive_vs_predictive()
    create_pipeline_flowchart()
    create_16_features_grid()
    create_chronological_split()
    create_world_model_diagram()
    create_rollout_loss_diagram()
    create_mitre_chevrons()
    create_shap_force()
    create_future_pillars()
    print("All v2 visual slide assets generated with precision spacing!")
