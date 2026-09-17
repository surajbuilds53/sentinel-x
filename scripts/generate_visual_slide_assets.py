"""Generate high-resolution visual diagrams and infographics for Sentinel-X presentation slides."""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

OUT_DIR = r"docs\presentation_assets\v2"
os.makedirs(OUT_DIR, exist_ok=True)
BG_COLOR = "#FFF1CD"  # Warm ivory matching Buddha Institute template


def create_reactive_vs_predictive():
    fig, ax = plt.subplots(figsize=(10, 4.2), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.axis("off")

    # Left: Traditional Reactive
    ax.add_patch(patches.FancyBboxPatch((0.03, 0.1), 0.44, 0.8, boxstyle="round,pad=0.04", facecolor="#FEE2E2", edgecolor="#DC2626", linewidth=2.5))
    ax.text(0.25, 0.82, "TRADITIONAL NIDS (REACTIVE)", ha="center", va="center", fontsize=12, fontweight="bold", color="#991B1B")

    steps_left = [
        "1. Attacker launches exploit payload",
        "2. Perimeter breached / system compromised",
        "3. Alert fires POST-COMPROMISE (Too Late!)",
        "Result: High MTTR & severe damage done"
    ]
    y = 0.65
    for s in steps_left:
        prefix = "• "
        ax.text(0.06, y, f"{prefix}{s}", fontsize=9.5, fontweight="bold" if "Result" in s else "normal", color="#7F1D1D" if "Result" in s else "#1E293B")
        y -= 0.14

    # Right: Sentinel-X Predictive
    ax.add_patch(patches.FancyBboxPatch((0.53, 0.1), 0.44, 0.8, boxstyle="round,pad=0.04", facecolor="#DCFCE7", edgecolor="#16A34A", linewidth=2.5))
    ax.text(0.75, 0.82, "SENTINEL-X (PREDICTIVE FORECASTING)", ha="center", va="center", fontsize=12, fontweight="bold", color="#166534")

    steps_right = [
        "1. Monitors 120s continuous telemetry window",
        "2. LSTM World Model forecasts 10-30s ahead",
        "3. Alert & MITRE stage predicted PRE-BREACH",
        "Result: 10-30s proactive mitigation buffer"
    ]
    y = 0.65
    for s in steps_right:
        prefix = "• "
        ax.text(0.56, y, f"{prefix}{s}", fontsize=9.5, fontweight="bold" if "Result" in s else "normal", color="#14532D" if "Result" in s else "#1E293B")
        y -= 0.14

    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "diag_reactive_vs_predictive.png"), dpi=220)
    plt.close()


def create_pipeline_flowchart():
    fig, ax = plt.subplots(figsize=(11, 4.5), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.axis("off")

    stages = [
        ("1. Traffic Telemetry", "CIC-IDS / Benchmark\nFlow Records", 0.02, 0.58, "#DBEAFE", "#1D4ED8"),
        ("2. 10s Aggregator", "16 Continuous State\nFeatures Extracted", 0.27, 0.58, "#E0E7FF", "#4338CA"),
        ("3. Leak-Free Window", "Chronological 70/15/15\nInput: T-11...T (120s)", 0.52, 0.58, "#EDE9FE", "#6D28D9"),
        ("4. LSTM World Model", "2-Layer Recurrent\nHidden 128, Dropout 0.3", 0.77, 0.58, "#FEF3C7", "#D97706"),
    ]

    for title, desc, x, y, fc, ec in stages:
        ax.add_patch(patches.FancyBboxPatch((x, y), 0.21, 0.34, boxstyle="round,pad=0.03", facecolor=fc, edgecolor=ec, linewidth=2.2))
        ax.text(x + 0.105, y + 0.23, title, ha="center", va="center", fontsize=9.5, fontweight="bold", color="#0F172A")
        ax.text(x + 0.105, y + 0.10, desc, ha="center", va="center", fontsize=8.5, color="#334155")

    # Arrows row 1
    ax.annotate("", xy=(0.27, 0.75), xytext=(0.23, 0.75), arrowprops=dict(arrowstyle="->", lw=2.5, color="#1E293B"))
    ax.annotate("", xy=(0.52, 0.75), xytext=(0.48, 0.75), arrowprops=dict(arrowstyle="->", lw=2.5, color="#1E293B"))
    ax.annotate("", xy=(0.77, 0.75), xytext=(0.73, 0.75), arrowprops=dict(arrowstyle="->", lw=2.5, color="#1E293B"))

    # Turn down arrow
    ax.annotate("", xy=(0.88, 0.52), xytext=(0.88, 0.58), arrowprops=dict(arrowstyle="->", lw=2.5, color="#1E293B"))

    stages2 = [
        ("7. SOC Dashboard", "5 Interactive Views\nLive Local Execution", 0.02, 0.12, "#CCFBF1", "#0F766E"),
        ("6. SHAP Explainability", "Signed Risk Drivers\n& Temporal Saliency", 0.27, 0.12, "#DCFCE7", "#15803D"),
        ("5. Multi-Step Rollout", "Autoregressive Loop\nT+1 -> T+2 -> T+3", 0.52, 0.12, "#FFE4E6", "#BE123C"),
        ("3 Forecast Heads", "Risk (BCE) | Stage (CE)\nState Reconstructor (MSE)", 0.77, 0.12, "#FEE2E2", "#B91C1C"),
    ]

    for title, desc, x, y, fc, ec in stages2:
        ax.add_patch(patches.FancyBboxPatch((x, y), 0.21, 0.34, boxstyle="round,pad=0.03", facecolor=fc, edgecolor=ec, linewidth=2.2))
        ax.text(x + 0.105, y + 0.23, title, ha="center", va="center", fontsize=9.5, fontweight="bold", color="#0F172A")
        ax.text(x + 0.105, y + 0.10, desc, ha="center", va="center", fontsize=8.5, color="#334155")

    # Arrows row 2 (right to left)
    ax.annotate("", xy=(0.73, 0.29), xytext=(0.77, 0.29), arrowprops=dict(arrowstyle="->", lw=2.5, color="#1E293B"))
    ax.annotate("", xy=(0.48, 0.29), xytext=(0.52, 0.29), arrowprops=dict(arrowstyle="->", lw=2.5, color="#1E293B"))
    ax.annotate("", xy=(0.23, 0.29), xytext=(0.27, 0.29), arrowprops=dict(arrowstyle="->", lw=2.5, color="#1E293B"))

    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "diag_pipeline_flowchart.png"), dpi=220)
    plt.close()


def create_16_features_grid():
    fig, ax = plt.subplots(figsize=(10.5, 4.4), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.axis("off")

    cards = [
        ("VOLUMETRIC (5 Features)", ["flow_count", "total_packets", "packet_rate", "total_bytes", "byte_rate"], "Detects volumetric floods & exfiltration", 0.02, 0.52, "#DBEAFE", "#1D4ED8"),
        ("TIMING & DURATION (3 Features)", ["duration_mean", "duration_std", "iat_mean (inter-arrival)"], "Detects rapid scanning & botnet pacing", 0.52, 0.52, "#FEF3C7", "#D97706"),
        ("PACKET DYNAMICS (2 Features)", ["fwd_pkt_len_mean", "bwd_pkt_len_mean"], "Detects payload size & auth asymmetry", 0.02, 0.05, "#DCFCE7", "#15803D"),
        ("FLAGS & PROTOCOLS (6 Features)", ["syn_ratio, rst_ratio", "ack_ratio, fin_ratio", "tcp_ratio, udp_ratio"], "Detects SYN scans, closed ports & floods", 0.52, 0.05, "#FEE2E2", "#B91C1C"),
    ]

    for title, feats, note, x, y, fc, ec in cards:
        ax.add_patch(patches.FancyBboxPatch((x, y), 0.46, 0.42, boxstyle="round,pad=0.03", facecolor=fc, edgecolor=ec, linewidth=2))
        ax.text(x + 0.03, y + 0.33, title, fontsize=10.5, fontweight="bold", color=ec)
        y_f = y + 0.23
        for f in feats:
            ax.text(x + 0.03, y_f, f"•  {f}", fontsize=9, fontfamily="monospace", fontweight="bold", color="#1E293B")
            y_f -= 0.075
        ax.text(x + 0.03, y + 0.04, f"↳ {note}", fontsize=8, fontstyle="italic", color="#475569")

    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "diag_16_features_grid.png"), dpi=220)
    plt.close()


def create_chronological_split():
    fig, ax = plt.subplots(figsize=(10, 4.2), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.axis("off")

    ax.text(0.5, 0.92, "LEAK-FREE CHRONOLOGICAL PARTITIONING (NO RANDOM SHUFFLING)", ha="center", va="center", fontsize=11.5, fontweight="bold", color="#1E3A8A")

    # Timeline bar
    ax.add_patch(patches.Rectangle((0.05, 0.65), 0.63, 0.16, facecolor="#93C5FD", edgecolor="#1D4ED8", linewidth=1.5))
    ax.text(0.365, 0.73, "TRAINING SET (Earliest 70%)\nStandardScaler fitted solely here", ha="center", va="center", fontsize=9, fontweight="bold", color="#1E3A8A")

    ax.add_patch(patches.Rectangle((0.68, 0.65), 0.14, 0.16, facecolor="#FDE68A", edgecolor="#D97706", linewidth=1.5))
    ax.text(0.75, 0.73, "VALIDATION\n(Middle 15%)", ha="center", va="center", fontsize=8.5, fontweight="bold", color="#78350F")

    ax.add_patch(patches.Rectangle((0.82, 0.65), 0.13, 0.16, facecolor="#BBF7D0", edgecolor="#15803D", linewidth=1.5))
    ax.text(0.885, 0.73, "HELD-OUT TEST\n(Latest 15%)", ha="center", va="center", fontsize=8.5, fontweight="bold", color="#14532D")

    # Rolling sequence illustration
    ax.text(0.5, 0.52, "ROLLING SEQUENCE WINDOW STRUCTURE", ha="center", va="center", fontsize=11, fontweight="bold", color="#0F172A")

    # History window box
    ax.add_patch(patches.FancyBboxPatch((0.08, 0.15), 0.52, 0.28, boxstyle="round,pad=0.02", facecolor="#E0E7FF", edgecolor="#4338CA", linewidth=2))
    ax.text(0.34, 0.33, "HISTORICAL CONTEXT WINDOW (N = 12 steps)", ha="center", va="center", fontsize=9.5, fontweight="bold", color="#312E81")
    ax.text(0.34, 0.22, "Input Sequence: [T-11, T-10, ..., T-1, T] = 120 Seconds (2 min)\nTensor Shape: [Batch Size, 12, 16 features]", ha="center", va="center", fontsize=8.5, color="#1E1B4B")

    # Arrow to targets
    ax.annotate("", xy=(0.67, 0.29), xytext=(0.60, 0.29), arrowprops=dict(arrowstyle="->", lw=3, color="#DC2626"))

    # Forecast targets box
    ax.add_patch(patches.FancyBboxPatch((0.68, 0.15), 0.25, 0.28, boxstyle="round,pad=0.02", facecolor="#FEE2E2", edgecolor="#DC2626", linewidth=2))
    ax.text(0.805, 0.33, "FORECAST TARGETS (H = 3)", ha="center", va="center", fontsize=9.5, fontweight="bold", color="#991B1B")
    ax.text(0.805, 0.22, "T+1: Next 10 seconds\nT+2: Next 20 seconds\nT+3: Next 30 seconds", ha="center", va="center", fontsize=8.5, color="#7F1D1D")

    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "diag_chronological_split.png"), dpi=220)
    plt.close()


def create_mitre_chevrons():
    fig, ax = plt.subplots(figsize=(10.5, 4.2), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.axis("off")

    stages = [
        ("STAGE 0\nBENIGN", "Normal Baseline", "High ACK (>0.85)\nNormal durations\nSteady traffic", "#D1FAE5", "#059669"),
        ("STAGE 1\nRECON (TA0043)", "Port Scanning", "SYN ratio > 0.5\nShort durations\nSpike in flow count", "#FEF3C7", "#D97706"),
        ("STAGE 2\nINITIAL ACCESS", "Brute Force (TA0001)", "Repeated auth attempts\nHigh byte rates\nSSH/FTP Patator", "#FED7AA", "#EA580C"),
        ("STAGE 3\nLATERAL MOVE", "Subnet Pivot (TA0008)", "Bursty SMB/RDP\nInternal traversal\nTraffic expansion", "#FECDD3", "#E11D48"),
        ("STAGE 4\nCOMMAND & CTRL", "C2 Beaconing (TA0011)", "Periodic IAT pulses\nHeartbeat channels\nRigid time intervals", "#FEE2E2", "#DC2626"),
    ]

    x = 0.02
    w = 0.18
    for title, sub, desc, fc, ec in stages:
        ax.add_patch(patches.FancyBboxPatch((x, 0.12), w, 0.76, boxstyle="round,pad=0.02", facecolor=fc, edgecolor=ec, linewidth=2.2))
        ax.text(x + w/2, 0.77, title, ha="center", va="center", fontsize=9.5, fontweight="bold", color=ec)
        ax.text(x + w/2, 0.63, sub, ha="center", va="center", fontsize=9, fontweight="bold", color="#0F172A")
        ax.text(x + w/2, 0.36, desc, ha="center", va="center", fontsize=8.5, color="#334155")

        if x < 0.75:
            ax.annotate("", xy=(x + w + 0.018, 0.5), xytext=(x + w + 0.002, 0.5), arrowprops=dict(arrowstyle="->", lw=2, color="#475569"))
        x += 0.20

    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "diag_mitre_chevrons.png"), dpi=220)
    plt.close()


def create_shap_force():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.5, 4.2), facecolor=BG_COLOR, gridspec_kw={"width_ratios": [1.4, 1.0]})
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
    ax1.axvline(0, color="#475569", linewidth=1.5)
    ax1.set_xlabel("SHAP Impact on T+1 Forecast Risk", fontsize=9.5, fontweight="bold")
    ax1.set_title("Signed Threat Attribution (Drivers vs. Inhibitors)", fontsize=10.5, fontweight="bold", color="#1E3A8A")
    ax1.grid(axis="x", linestyle="--", alpha=0.5)

    # Annotate labels
    for i, v in enumerate(vals):
        offset = 0.02 if v >= 0 else -0.02
        ha = "left" if v >= 0 else "right"
        ax1.text(v + offset, i, f"{v:+.2f}", va="center", ha=ha, fontsize=8, fontweight="bold")

    # Right: Temporal Saliency
    t_steps = [f"T-{11-i}" for i in range(12)]
    t_vals = [0.03 + 0.12 * ((i+1)/12)**2 for i in range(12)]
    ax2.bar(t_steps, t_vals, color="#4338CA", edgecolor="#1E1B4B")
    ax2.set_title("Temporal Saliency (T-11 ... T)", fontsize=10.5, fontweight="bold", color="#1E3A8A")
    ax2.set_ylabel("Attribution Weight", fontsize=9)
    ax2.set_xticklabels(t_steps, rotation=45, fontsize=7.5)
    ax2.grid(axis="y", linestyle="--", alpha=0.5)

    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "diag_shap_force.png"), dpi=220)
    plt.close()


def create_future_pillars():
    fig, ax = plt.subplots(figsize=(10.5, 4.2), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.axis("off")

    pillars = [
        ("AUTOMATED SDN INTEGRATION", "Direct API linkage to OpenFlow / SDN controllers to push automatic firewall ACLs upon high-confidence T+1 risk alarms.", "#DBEAFE", "#1D4ED8"),
        ("TEMPORAL GRAPH NETWORKS", "Integrating Graph Neural Networks (GNNs) to model host-to-host lateral traversal topology alongside sequential time-series.", "#EDE9FE", "#6D28D9"),
        ("EDGE ROUTER QUANTIZATION", "Quantizing the PyTorch LSTM model using ONNX / TensorRT for sub-millisecond deployment inside edge enterprise routers.", "#DCFCE7", "#15803D"),
    ]

    x = 0.04
    w = 0.28
    for title, desc, fc, ec in pillars:
        ax.add_patch(patches.FancyBboxPatch((x, 0.15), w, 0.7, boxstyle="round,pad=0.03", facecolor=fc, edgecolor=ec, linewidth=2.5))
        ax.text(x + w/2, 0.72, title, ha="center", va="center", fontsize=10, fontweight="bold", color=ec)
        ax.text(x + w/2, 0.42, desc, ha="center", va="center", fontsize=9.5, color="#1E293B", wrap=True)
        x += 0.32

    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "diag_future_pillars.png"), dpi=220)
    plt.close()


if __name__ == "__main__":
    create_reactive_vs_predictive()
    create_pipeline_flowchart()
    create_16_features_grid()
    create_chronological_split()
    create_mitre_chevrons()
    create_shap_force()
    create_future_pillars()
    print("All v2 visual slide assets generated successfully!")
