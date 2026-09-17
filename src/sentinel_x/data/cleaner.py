"""Data cleaning, validation, and sanitization for network traffic flow datasets.

Supports CIC-IDS-2017, CIC-IDS-2018, and Sentinel-X synthetic network flow formats.
"""

import logging
from typing import List, Optional, Tuple
import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

# Standard column mapping to normalize different versions of CIC-IDS
COLUMN_ALIASES = {
    "destination port": "dst_port",
    "dst port": "dst_port",
    "flow duration": "flow_duration",
    "total fwd packets": "tot_fwd_pkts",
    "total backward packets": "tot_bwd_pkts",
    "tot fwd pkts": "tot_fwd_pkts",
    "tot bwd pkts": "tot_bwd_pkts",
    "total length of fwd packets": "tot_fwd_bytes",
    "total length of bwd packets": "tot_bwd_bytes",
    "totlen fwd pkts": "tot_fwd_bytes",
    "totlen bwd pkts": "tot_bwd_bytes",
    "fwd packet length mean": "fwd_pkt_len_mean",
    "bwd packet length mean": "bwd_pkt_len_mean",
    "flow packets/s": "flow_pkts_s",
    "flow bytes/s": "flow_bytes_s",
    "flow iat mean": "flow_iat_mean",
    "flow iat std": "flow_iat_std",
    "fwd iat mean": "fwd_iat_mean",
    "bwd iat mean": "bwd_iat_mean",
    "fin flag count": "fin_flag_cnt",
    "syn flag count": "syn_flag_cnt",
    "rst flag count": "rst_flag_cnt",
    "psh flag count": "psh_flag_cnt",
    "ack flag count": "ack_flag_cnt",
    "urg flag count": "urg_flag_cnt",
    "protocol": "protocol",
    "timestamp": "timestamp",
    "label": "label",
}


def normalize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Strip whitespace, lowercase, and map common column variations."""
    df = df.copy()
    cleaned_cols = []
    for col in df.columns:
        norm = str(col).strip().lower()
        norm = COLUMN_ALIASES.get(norm, norm.replace(" ", "_").replace("/", "_").replace(".", "_"))
        cleaned_cols.append(norm)
    df.columns = cleaned_cols
    return df


def remove_repeated_headers(df: pd.DataFrame, label_col: str = "label") -> pd.DataFrame:
    """Detect and remove repeated CSV headers embedded within rows."""
    if label_col in df.columns:
        # Check if the label column contains the string 'label' (case-insensitive)
        is_header_row = df[label_col].astype(str).str.strip().str.lower() == label_col.lower()
        header_count = is_header_row.sum()
        if header_count > 0:
            logger.info(f"Removing {header_count} repeated header rows.")
            df = df[~is_header_row]
    return df


def sanitize_numeric_values(df: pd.DataFrame, exclude_cols: Optional[List[str]] = None) -> pd.DataFrame:
    """Replace +/- infinity with NaNs, coerce numeric types, and fill missing values."""
    df = df.copy()
    exclude = set(exclude_cols or ["label", "timestamp", "src_ip", "dst_ip"])
    
    numeric_cols = [col for col in df.columns if col not in exclude]
    
    for col in numeric_cols:
        # Coerce to numeric (bad strings become NaN)
        df[col] = pd.to_numeric(df[col], errors="coerce")
        # Replace inf and -inf with NaN
        df[col] = df[col].replace([np.inf, -np.inf], np.nan)
        # Fill NaN with median or 0
        median_val = df[col].median()
        fill_val = median_val if pd.notna(median_val) else 0.0
        df[col] = df[col].fillna(fill_val).astype(np.float32)
        
    return df


def parse_and_sort_timestamps(df: pd.DataFrame, time_col: str = "timestamp") -> pd.DataFrame:
    """Parse timestamps and ensure chronological order without shuffling."""
    df = df.copy()
    if time_col in df.columns:
        df[time_col] = pd.to_datetime(df[time_col], errors="coerce")
        # If timestamps could not be parsed, create synthetic sequence index
        if df[time_col].isna().all():
            logger.warning(f"Column '{time_col}' could not be parsed as datetime; creating linear timestamp sequence.")
            base_time = pd.Timestamp("2026-01-01 00:00:00")
            df[time_col] = [base_time + pd.Timedelta(seconds=i) for i in range(len(df))]
        else:
            # Fill individual NaNs by forward-fill
            df[time_col] = df[time_col].ffill().bfill()
            
        # Chronological sort
        df = df.sort_values(by=time_col).reset_index(drop=True)
    else:
        # Generate simulated chronological timestamps
        base_time = pd.Timestamp("2026-01-01 00:00:00")
        df[time_col] = [base_time + pd.Timedelta(seconds=i) for i in range(len(df))]
        
    return df


def clean_flow_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Master cleaning pipeline for raw flow dataframe.
    
    Performs:
    1. Column name normalization
    2. Repeated header removal
    3. Missing / infinite value sanitization
    4. Chronological sorting
    """
    if df.empty:
        raise ValueError("Cannot clean an empty DataFrame.")
        
    # 1. Normalize column names
    df = normalize_column_names(df)
    
    # 2. Repeated headers
    label_col = "label" if "label" in df.columns else None
    if label_col:
        df = remove_repeated_headers(df, label_col=label_col)
        
    # 3. Numeric sanitization
    df = sanitize_numeric_values(df, exclude_cols=["label", "timestamp", "src_ip", "dst_ip"])
    
    # 4. Chronological ordering
    df = parse_and_sort_timestamps(df, time_col="timestamp")
    
    # 5. Clean labels
    if "label" in df.columns:
        df["label"] = df["label"].astype(str).str.strip()
    else:
        df["label"] = "Benign"
        
    return df.reset_index(drop=True)
