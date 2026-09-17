"""SAFE Synthetic Network Traffic Generator for Sentinel-X Demonstration.

Defensive Cybersecurity B.Tech Minor Project (SIH26153).
Generates purely synthetic statistical patterns for viva and offline SOC demonstration.
DOES NOT perform any real-world attack, exploit, or offensive network packet generation.
"""

from pathlib import Path
from typing import Optional, Union, Dict, Any, List
import numpy as np
import pandas as pd

from sentinel_x.config import set_seed


def _make_benign_flow(ts: pd.Timestamp, rng: np.random.Generator) -> Dict[str, Any]:
    proto = 6 if rng.random() > 0.25 else 17
    dst_port = int(rng.choice([80, 443, 53, 8080, 22, 8443]))
    return {
        "timestamp": ts,
        "dst_port": dst_port,
        "protocol": proto,
        "flow_duration": float(rng.uniform(500, 180000)),
        "tot_fwd_pkts": int(rng.integers(2, 20)),
        "tot_bwd_pkts": int(rng.integers(1, 25)),
        "tot_fwd_bytes": int(rng.integers(150, 6000)),
        "tot_bwd_bytes": int(rng.integers(200, 12000)),
        "fwd_pkt_len_mean": float(rng.uniform(40, 500)),
        "bwd_pkt_len_mean": float(rng.uniform(60, 1000)),
        "flow_iat_mean": float(rng.uniform(100, 12000)),
        "syn_flag_cnt": 1 if rng.random() > 0.8 else 0,
        "rst_flag_cnt": 1 if rng.random() > 0.98 else 0,
        "psh_flag_cnt": 1 if rng.random() > 0.5 else 0,
        "ack_flag_cnt": 1,
        "fin_flag_cnt": 1 if rng.random() > 0.85 else 0,
        "label": "Benign",
        "is_synthetic": True,
    }


def _make_recon_flow(ts: pd.Timestamp, rng: np.random.Generator) -> Dict[str, Any]:
    return {
        "timestamp": ts,
        "dst_port": int(rng.integers(1, 65535)),
        "protocol": 6,
        "flow_duration": float(rng.uniform(10, 600)),
        "tot_fwd_pkts": int(rng.integers(1, 3)),
        "tot_bwd_pkts": int(rng.integers(0, 1)),
        "tot_fwd_bytes": int(rng.integers(40, 120)),
        "tot_bwd_bytes": 0,
        "fwd_pkt_len_mean": float(rng.uniform(40, 64)),
        "bwd_pkt_len_mean": 0.0,
        "flow_iat_mean": float(rng.uniform(5, 50)),
        "syn_flag_cnt": 1,
        "rst_flag_cnt": 1 if rng.random() > 0.4 else 0,
        "psh_flag_cnt": 0,
        "ack_flag_cnt": 0,
        "fin_flag_cnt": 0,
        "label": "PortScan",
        "is_synthetic": True,
    }


def _make_access_flow(ts: pd.Timestamp, rng: np.random.Generator) -> Dict[str, Any]:
    return {
        "timestamp": ts,
        "dst_port": int(rng.choice([21, 22, 80, 443])),
        "protocol": 6,
        "flow_duration": float(rng.uniform(2000, 45000)),
        "tot_fwd_pkts": int(rng.integers(12, 50)),
        "tot_bwd_pkts": int(rng.integers(10, 40)),
        "tot_fwd_bytes": int(rng.integers(800, 10000)),
        "tot_bwd_bytes": int(rng.integers(600, 7000)),
        "fwd_pkt_len_mean": float(rng.uniform(100, 350)),
        "bwd_pkt_len_mean": float(rng.uniform(80, 250)),
        "flow_iat_mean": float(rng.uniform(50, 350)),
        "syn_flag_cnt": 1 if rng.random() > 0.3 else 0,
        "rst_flag_cnt": 1 if rng.random() > 0.6 else 0,
        "psh_flag_cnt": 1,
        "ack_flag_cnt": 1,
        "fin_flag_cnt": 1 if rng.random() > 0.5 else 0,
        "label": "FTP-Patator",
        "is_synthetic": True,
    }


def _make_lateral_flow(ts: pd.Timestamp, rng: np.random.Generator) -> Dict[str, Any]:
    return {
        "timestamp": ts,
        "dst_port": int(rng.choice([445, 139, 3389, 5985])),
        "protocol": 6,
        "flow_duration": float(rng.uniform(5000, 150000)),
        "tot_fwd_pkts": int(rng.integers(15, 80)),
        "tot_bwd_pkts": int(rng.integers(15, 80)),
        "tot_fwd_bytes": int(rng.integers(2000, 30000)),
        "tot_bwd_bytes": int(rng.integers(2000, 35000)),
        "fwd_pkt_len_mean": float(rng.uniform(150, 700)),
        "bwd_pkt_len_mean": float(rng.uniform(200, 800)),
        "flow_iat_mean": float(rng.uniform(150, 1500)),
        "syn_flag_cnt": 1 if rng.random() > 0.4 else 0,
        "rst_flag_cnt": 0,
        "psh_flag_cnt": 1,
        "ack_flag_cnt": 1,
        "fin_flag_cnt": 1 if rng.random() > 0.7 else 0,
        "label": "Infiltration",
        "is_synthetic": True,
    }


def _make_c2_flow(ts: pd.Timestamp, rng: np.random.Generator) -> Dict[str, Any]:
    return {
        "timestamp": ts,
        "dst_port": int(rng.choice([443, 8443, 53])),
        "protocol": 6,
        "flow_duration": float(rng.uniform(800, 3500)),
        "tot_fwd_pkts": int(rng.integers(4, 7)),
        "tot_bwd_pkts": int(rng.integers(3, 6)),
        "tot_fwd_bytes": int(rng.integers(200, 500)),
        "tot_bwd_bytes": int(rng.integers(100, 350)),
        "fwd_pkt_len_mean": float(rng.uniform(50, 85)),
        "bwd_pkt_len_mean": float(rng.uniform(40, 75)),
        "flow_iat_mean": float(rng.uniform(4900, 5100)),
        "syn_flag_cnt": 1 if rng.random() > 0.5 else 0,
        "rst_flag_cnt": 0,
        "psh_flag_cnt": 1,
        "ack_flag_cnt": 1,
        "fin_flag_cnt": 1,
        "label": "Bot",
        "is_synthetic": True,
    }


def generate_synthetic_flow_dataset(
    num_flows: int = 10000,
    seed: int = 42,
    output_path: Optional[Union[Path, str]] = None,
) -> pd.DataFrame:
    """Generate realistic synthetic network flow dataset with episodic attack campaigns.
    
    Structure:
    - 60% persistent background benign traffic spanning the full timeline.
    - Periodic attack campaign episodes (Recon, Initial Access, Lateral Movement, C2)
      interleaved across 3 distinct campaign waves so train, val, and test splits
      contain realistic distributions of benign and attack behavioral transitions.
    """
    set_seed(seed)
    rng = np.random.default_rng(seed)

    start_time = pd.Timestamp("2026-03-15 08:00:00")
    total_duration_sec = 7200.0  # 2 hours

    records: List[Dict[str, Any]] = []

    # Campaign definitions with normalized time intervals [start_ratio, end_ratio]
    campaigns = [
        # Wave 1 (occurs in train split: 0.0 - 0.70)
        {"type": "recon", "start": 0.10, "end": 0.20, "flows": int(num_flows * 0.08)},
        {"type": "access", "start": 0.30, "end": 0.45, "flows": int(num_flows * 0.08)},
        {"type": "lateral", "start": 0.52, "end": 0.65, "flows": int(num_flows * 0.06)},
        
        # Wave 2 (occurs across train/val boundary: 0.65 - 0.85)
        {"type": "c2", "start": 0.68, "end": 0.78, "flows": int(num_flows * 0.05)},
        {"type": "recon", "start": 0.75, "end": 0.83, "flows": int(num_flows * 0.05)},
        
        # Wave 3 (occurs in test split: 0.85 - 1.00)
        {"type": "access", "start": 0.85, "end": 0.92, "flows": int(num_flows * 0.05)},
        {"type": "lateral", "start": 0.90, "end": 0.97, "flows": int(num_flows * 0.05)},
        {"type": "c2", "start": 0.94, "end": 0.99, "flows": int(num_flows * 0.05)},
    ]

    # 1. Background Benign traffic (evenly distributed across full session)
    n_campaign_flows = sum(c["flows"] for c in campaigns)
    n_benign = max(1000, num_flows - n_campaign_flows)

    benign_times = start_time + pd.to_timedelta(
        np.sort(rng.uniform(0, total_duration_sec, size=n_benign)), unit="s"
    )
    for ts in benign_times:
        records.append(_make_benign_flow(ts, rng))

    # 2. Add campaign flows
    makers = {
        "recon": _make_recon_flow,
        "access": _make_access_flow,
        "lateral": _make_lateral_flow,
        "c2": _make_c2_flow,
    }

    for camp in campaigns:
        maker = makers[camp["type"]]
        s_sec = camp["start"] * total_duration_sec
        e_sec = camp["end"] * total_duration_sec
        c_times = start_time + pd.to_timedelta(
            np.sort(rng.uniform(s_sec, e_sec, size=camp["flows"])), unit="s"
        )
        for ts in c_times:
            records.append(maker(ts, rng))

    df = pd.DataFrame(records).sort_values("timestamp").reset_index(drop=True)

    if output_path:
        out_p = Path(output_path)
        out_p.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(out_p, index=False)

    return df
