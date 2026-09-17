"""Tests for configuration loading and system reproducibility in Sentinel-X."""

from pathlib import Path
import pytest
import numpy as np
import random
from sentinel_x.config import load_config, set_seed, get_device, PROJECT_ROOT


def test_project_root_exists():
    assert PROJECT_ROOT.is_dir()
    assert (PROJECT_ROOT / "config.yaml").is_file()


def test_load_config():
    config = load_config()
    assert isinstance(config, dict)
    assert "project" in config
    assert config["project"]["name"] == "Sentinel-X"
    assert "lstm_world_model" in config
    assert config["lstm_world_model"]["hidden_size"] == 128
    assert config["lstm_world_model"]["num_layers"] == 2
    assert "taxonomy" in config
    assert len(config["taxonomy"]["stages"]) == 5


def test_set_seed():
    set_seed(42)
    val1 = random.random()
    np_val1 = np.random.rand()
    
    set_seed(42)
    val2 = random.random()
    np_val2 = np.random.rand()
    
    assert val1 == val2
    assert np_val1 == np_val2


def test_get_device():
    dev = get_device("cpu")
    assert dev == "cpu"
    auto_dev = get_device("auto")
    assert auto_dev in ["cuda", "cpu"]


def test_directory_structure():
    expected = [
        "data/raw",
        "data/processed",
        "data/sample",
        "models/checkpoints",
        "models/scalers",
        "models/evaluation",
        "src/sentinel_x",
        "dashboard",
        "scripts",
        "tests",
    ]
    for d in expected:
        p = PROJECT_ROOT / d
        assert p.is_dir(), f"Expected directory {d} does not exist"
