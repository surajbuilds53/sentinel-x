"""SAFE Synthetic Network Traffic Generator for Sentinel-X Demonstration.

Defensive Cybersecurity B.Tech Minor Project (SIH26153).
Generates purely synthetic statistical patterns for viva and offline SOC demonstration.
DOES NOT perform any real-world attack, exploit, or offensive network packet generation.
"""

from pathlib import Path
from typing import Optional, Union
import numpy as np
import pandas as pd

from sentinel_x.config import set_seed


def generate_synthetic_flow_dataset(
    num_flows: int = 8000,
    seed: int = 42,
    output_path: Optional[Union[Path, str]] = None,
) -> pd.DataFrame:
    """Generate synthetic network flow DataFrame with distinct statistical phases.
    
    Phases:
    1. Normal Benign Traffic (~45% of flows)
    2. Reconnaissance-like Statistical Pattern (~15% of flows)
    3. Initial Access-like Statistical Pattern (~15% of flows)
    4. Lateral Movement-like Statistical Pattern (~12% of flows)
    5. C2 Beaconing-like Statistical Pattern (~13% of flows)
    """
    set_seed(seed)
    rng = np.random.default_rng(seed)
    
    start_time = pd.Timestamp("2026-03-15 08:00:00")
    # Spacing flows to span ~2-3 hours for robust temporal time bins
    timestamps = [start_time + pd.Timedelta(seconds=float(i * 1.2 + rng.uniform(-0.3, 0.3))) for i in range(num_flows)]
    
    n_benign = int(num_flows * 0.45)
    n_recon = int(num_flows * 0.15)
    n_access = int(num_flows * 0.15)
    n_lateral = int(num_flows * 0.12)
    n_c2 = num_flows - (n_benign + n_recon + n_access + n_lateral)
    
    records = []
    
    # --- PHASE 1: Benign / Normal Activity ---
    for i in range(n_benign):
        proto = 6 if rng.random() > 0.3 else 17
        dst_port = int(rng.choice([80, 443, 53, 8080, 22]))
        records.append({
            "timestamp": timestamps[i],
            "dst_port": dst_port,
            "protocol": proto,
            "flow_duration": float(rng.uniform(500, 200000)),
            "tot_fwd_pkts": int(rng.integers(2, 25)),
            "tot_bwd_pkts": int(rng.integers(1, 30)),
            "tot_fwd_bytes": int(rng.integers(150, 8000)),
            "tot_bwd_bytes": int(rng.integers(200, 15000)),
            "fwd_pkt_len_mean": float(rng.uniform(40, 600)),
            "bwd_pkt_len_mean": float(rng.uniform(60, 1200)),
            "flow_iat_mean": float(rng.uniform(100, 15000)),
            "syn_flag_cnt": 1 if rng.random() > 0.7 else 0,
            "rst_flag_cnt": 1 if rng.random() > 0.95 else 0,
            "psh_flag_cnt": 1 if rng.random() > 0.5 else 0,
            "ack_flag_cnt": 1,
            "fin_flag_cnt": 1 if rng.random() > 0.8 else 0,
            "label": "Benign",
            "is_synthetic": True,
        })
        
    offset = n_benign
    # --- PHASE 2: Reconnaissance-like Pattern (TA0043) ---
    for i in range(n_recon):
        idx = offset + i
        records.append({
            "timestamp": timestamps[idx],
            "dst_port": int(rng.integers(1, 65535)),
            "protocol": 6,
            "flow_duration": float(rng.uniform(10, 800)),
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
        })
        
    offset += n_recon
    # --- PHASE 3: Initial Access-like Pattern (TA0001) ---
    for i in range(n_access):
        idx = offset + i
        records.append({
            "timestamp": timestamps[idx],
            "dst_port": int(rng.choice([21, 22, 80, 443])),
            "protocol": 6,
            "flow_duration": float(rng.uniform(2000, 50000)),
            "tot_fwd_pkts": int(rng.integers(10, 60)),
            "tot_bwd_pkts": int(rng.integers(8, 50)),
            "tot_fwd_bytes": int(rng.integers(800, 12000)),
            "tot_bwd_bytes": int(rng.integers(600, 8000)),
            "fwd_pkt_len_mean": float(rng.uniform(100, 400)),
            "bwd_pkt_len_mean": float(rng.uniform(80, 300)),
            "flow_iat_mean": float(rng.uniform(50, 400)),
            "syn_flag_cnt": 1 if rng.random() > 0.3 else 0,
            "rst_flag_cnt": 1 if rng.random() > 0.6 else 0,
            "psh_flag_cnt": 1,
            "ack_flag_cnt": 1,
            "fin_flag_cnt": 1 if rng.random() > 0.5 else 0,
            "label": "FTP-Patator",
            "is_synthetic": True,
        })
        
    offset += n_access
    # --- PHASE 4: Lateral Movement-like Pattern (TA0008) ---
    for i in range(n_lateral):
        idx = offset + i
        records.append({
            "timestamp": timestamps[idx],
            "dst_port": int(rng.choice([445, 139, 3389, 5985])),
            "protocol": 6,
            "flow_duration": float(rng.uniform(5000, 180000)),
            "tot_fwd_pkts": int(rng.integers(15, 100)),
            "tot_bwd_pkts": int(rng.integers(15, 100)),
            "tot_fwd_bytes": int(rng.integers(2000, 35000)),
            "tot_bwd_bytes": int(rng.integers(2000, 40000)),
            "fwd_pkt_len_mean": float(rng.uniform(150, 800)),
            "bwd_pkt_len_mean": float(rng.uniform(200, 900)),
            "flow_iat_mean": float(rng.uniform(150, 2000)),
            "syn_flag_cnt": 1 if rng.random() > 0.4 else 0,
            "rst_flag_cnt": 0,
            "psh_flag_cnt": 1,
            "ack_flag_cnt": 1,
            "fin_flag_cnt": 1 if rng.random() > 0.7 else 0,
            "label": "Infiltration",
            "is_synthetic": True,
        })
        
    offset += n_lateral
    # --- PHASE 5: Command and Control Beaconing-like Pattern (TA0011) ---
    for i in range(n_c2):
        idx = offset + i
        records.append({
            "timestamp": timestamps[idx],
            "dst_port": int(rng.choice([443, 8443, 53])),
            "protocol": 6,
            "flow_duration": float(rng.uniform(800, 4000)),
            "tot_fwd_pkts": int(rng.integers(4, 8)),
            "tot_bwd_pkts": int(rng.integers(3, 6)),
            "tot_fwd_bytes": int(rng.integers(200, 600)),
            "tot_bwd_bytes": int(rng.integers(100, 400)),
            "fwd_pkt_len_mean": float(rng.uniform(50, 90)),
            "bwd_pkt_len_mean": float(rng.uniform(40, 80)),
            "flow_iat_mean": float(rng.uniform(4800, 5200)),
            "syn_flag_cnt": 1 if rng.random() > 0.5 else 0,
            "rst_flag_cnt": 0,
            "psh_flag_cnt": 1,
            "ack_flag_cnt": 1,
            "fin_flag_cnt": 1,
            "label": "Bot",
            "is_synthetic": True,
        })
        
    df = pd.DataFrame(records).sort_values("timestamp").reset_index(drop=True)
    
    if output_path:
        out_p = Path(output_path)
        out_p.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(out_p, index=False)
        
    return df
