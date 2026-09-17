"""Tests for data cleaning, sanitization, and loading in Sentinel-X."""

import numpy as np
import pandas as pd
import pytest

from sentinel_x.data.cleaner import (
    normalize_column_names,
    remove_repeated_headers,
    sanitize_numeric_values,
    parse_and_sort_timestamps,
    clean_flow_dataframe,
)
from sentinel_x.taxonomy.mitre_mapping import map_raw_label_to_stage, get_stage_metadata


def test_normalize_column_names():
    raw_df = pd.DataFrame({
        " Destination Port": [80],
        " Flow Duration ": [1000],
        "Total Fwd Packets": [5],
        "Label": ["BENIGN"],
    })
    cleaned = normalize_column_names(raw_df)
    assert "dst_port" in cleaned.columns
    assert "flow_duration" in cleaned.columns
    assert "tot_fwd_pkts" in cleaned.columns
    assert "label" in cleaned.columns


def test_remove_repeated_headers():
    df = pd.DataFrame({
        "dst_port": [80, "Destination Port", 443],
        "label": ["Benign", "Label", "PortScan"],
    })
    filtered = remove_repeated_headers(df, label_col="label")
    assert len(filtered) == 2
    assert "Label" not in filtered["label"].values


def test_sanitize_numeric_values():
    df = pd.DataFrame({
        "flow_duration": ["1000", np.inf, -np.inf, np.nan, "2000"],
        "tot_fwd_pkts": [1, 2, 3, 4, 5],
        "label": ["Benign", "Benign", "PortScan", "Benign", "Benign"],
    })
    sanitized = sanitize_numeric_values(df, exclude_cols=["label"])
    assert np.all(np.isfinite(sanitized["flow_duration"]))
    assert sanitized["flow_duration"].dtype == np.float32
    assert sanitized["tot_fwd_pkts"].dtype == np.float32


def test_parse_and_sort_timestamps():
    df = pd.DataFrame({
        "timestamp": ["2026-03-01 10:05:00", "2026-03-01 10:01:00", "2026-03-01 10:03:00"],
        "val": [1, 2, 3],
    })
    sorted_df = parse_and_sort_timestamps(df, time_col="timestamp")
    assert sorted_df["val"].tolist() == [2, 3, 1]


def test_mitre_mapping():
    assert map_raw_label_to_stage("BENIGN") == 0
    assert map_raw_label_to_stage("PortScan") == 1
    assert map_raw_label_to_stage("FTP-Patator") == 2
    assert map_raw_label_to_stage("Infiltration") == 3
    assert map_raw_label_to_stage("Bot") == 4
    
    meta = get_stage_metadata(1)
    assert meta["tactic_id"] == "TA0043"
    assert "Reconnaissance" in meta["name"]
