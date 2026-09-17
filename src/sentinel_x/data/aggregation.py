"""Temporal aggregation module converting network flows into chronological network-state vectors."""

from typing import List, Tuple
import numpy as np
import pandas as pd

from sentinel_x.taxonomy.mitre_mapping import map_raw_label_to_stage

FEATURE_NAMES: List[str] = [
    "flow_count",
    "total_packets",
    "packet_rate",
    "total_bytes",
    "byte_rate",
    "duration_mean",
    "duration_std",
    "fwd_pkt_len_mean",
    "bwd_pkt_len_mean",
    "iat_mean",
    "syn_ratio",
    "rst_ratio",
    "ack_ratio",
    "fin_ratio",
    "tcp_ratio",
    "udp_ratio",
]


def aggregate_flows_to_time_windows(
    df: pd.DataFrame,
    window_seconds: int = 10,
    time_col: str = "timestamp",
    label_col: str = "label",
) -> pd.DataFrame:
    """Aggregate chronological flow records into regular fixed-interval network-state vectors.
    
    Args:
        df: Cleaned network flow DataFrame sorted by timestamp.
        window_seconds: Duration of each temporal aggregation window in seconds.
        time_col: Name of the timestamp column.
        label_col: Name of the label column.
        
    Returns:
        pd.DataFrame where each row is a chronological network-state vector with targets.
    """
    if df.empty:
        raise ValueError("DataFrame is empty; cannot perform aggregation.")
        
    df = df.copy()
    if not pd.api.types.is_datetime64_any_dtype(df[time_col]):
        df[time_col] = pd.to_datetime(df[time_col])
        
    df = df.sort_values(by=time_col).reset_index(drop=True)
    
    # Floor timestamps to window boundary
    freq_str = f"{int(window_seconds)}s"
    df["window_time"] = df[time_col].dt.floor(freq_str)
    
    grouped = df.groupby("window_time")
    records = []
    
    for window_time, group in grouped:
        n_flows = len(group)
        if n_flows == 0:
            continue
            
        # Helper for column retrieval
        def get_col(candidates: List[str], default: float = 0.0) -> pd.Series:
            for c in candidates:
                if c in group.columns:
                    return group[c].astype(float)
            return pd.Series([default] * n_flows, index=group.index)
            
        # Extract base metrics
        fwd_pkts = get_col(["tot_fwd_pkts", "total_fwd_packets", "fwd_packets"])
        bwd_pkts = get_col(["tot_bwd_pkts", "total_backward_packets", "bwd_packets"])
        total_pkts = fwd_pkts + bwd_pkts
        
        fwd_bytes = get_col(["tot_fwd_bytes", "total_length_of_fwd_packets", "fwd_bytes"])
        bwd_bytes = get_col(["tot_bwd_bytes", "total_length_of_bwd_packets", "bwd_bytes"])
        total_bytes = fwd_bytes + bwd_bytes
        
        duration = get_col(["flow_duration", "duration"])
        fwd_len = get_col(["fwd_pkt_len_mean", "fwd_packet_length_mean", "fwd_len_mean"])
        bwd_len = get_col(["bwd_pkt_len_mean", "bwd_packet_length_mean", "bwd_len_mean"])
        iat = get_col(["flow_iat_mean", "iat_mean", "flow_iat"])
        
        # Flags
        syn = get_col(["syn_flag_cnt", "syn_flags", "syn"]).gt(0).sum()
        rst = get_col(["rst_flag_cnt", "rst_flags", "rst"]).gt(0).sum()
        ack = get_col(["ack_flag_cnt", "ack_flags", "ack"]).gt(0).sum()
        fin = get_col(["fin_flag_cnt", "fin_flags", "fin"]).gt(0).sum()
        
        # Protocol
        protocol = get_col(["protocol"])
        tcp_count = (protocol == 6).sum()
        udp_count = (protocol == 17).sum()
        
        # Computed aggregated metrics
        pkt_sum = float(total_pkts.sum())
        byte_sum = float(total_bytes.sum())
        
        # Labels and stage determination
        labels = group[label_col].astype(str).tolist() if label_col in group.columns else ["Benign"]
        stages = [map_raw_label_to_stage(lbl) for lbl in labels]
        
        # Risk: 0 if all flows are benign, 1 if any malicious flow present
        max_stage = max(stages) if stages else 0
        risk = 1.0 if max_stage > 0 else 0.0
        
        # Dominant non-benign stage, or benign if none
        active_stages = [s for s in stages if s > 0]
        chosen_stage = max(set(active_stages), key=active_stages.count) if active_stages else 0
        
        records.append({
            "window_time": window_time,
            "flow_count": float(n_flows),
            "total_packets": pkt_sum,
            "packet_rate": float(pkt_sum / max(1.0, window_seconds)),
            "total_bytes": byte_sum,
            "byte_rate": float(byte_sum / max(1.0, window_seconds)),
            "duration_mean": float(duration.mean()),
            "duration_std": float(duration.std(ddof=0)),
            "fwd_pkt_len_mean": float(fwd_len.mean()),
            "bwd_pkt_len_mean": float(bwd_len.mean()),
            "iat_mean": float(iat.mean()),
            "syn_ratio": float(syn / n_flows),
            "rst_ratio": float(rst / n_flows),
            "ack_ratio": float(ack / n_flows),
            "fin_ratio": float(fin / n_flows),
            "tcp_ratio": float(tcp_count / n_flows),
            "udp_ratio": float(udp_count / n_flows),
            "risk": risk,
            "stage": chosen_stage,
        })
        
    state_df = pd.DataFrame(records).sort_values("window_time").reset_index(drop=True)
    return state_df
