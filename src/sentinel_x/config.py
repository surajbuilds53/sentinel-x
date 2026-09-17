"""Configuration manager and seed management for Sentinel-X."""

from pathlib import Path
from typing import Any, Dict
import random
import numpy as np
import yaml

# Root directory of the project
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_CONFIG_PATH = PROJECT_ROOT / "config.yaml"


def load_config(config_path: str | Path | None = None) -> Dict[str, Any]:
    """Load and parse the project configuration YAML file.
    
    Args:
        config_path: Optional path to config.yaml. Defaults to project root config.yaml.
        
    Returns:
        Dict containing configuration parameters.
    """
    path = Path(config_path) if config_path else DEFAULT_CONFIG_PATH
    if not path.is_file():
        raise FileNotFoundError(f"Configuration file not found at: {path}")
        
    with open(path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
        
    return config


def set_seed(seed: int = 42) -> None:
    """Set deterministic random seeds across Python, NumPy, and PyTorch.
    
    Args:
        seed: Random seed integer.
    """
    random.seed(seed)
    np.random.seed(seed)
    
    try:
        import torch
        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)
            torch.backends.cudnn.deterministic = True
            torch.backends.cudnn.benchmark = False
    except ImportError:
        pass


def get_device(requested: str = "auto") -> str:
    """Resolve the computing device ('cuda' or 'cpu').
    
    Args:
        requested: 'auto', 'cuda', or 'cpu'.
        
    Returns:
        String representing available device ('cuda' or 'cpu').
    """
    if requested == "cpu":
        return "cpu"
        
    try:
        import torch
        if requested == "cuda" and torch.cuda.is_available():
            return "cuda"
        if requested == "auto":
            return "cuda" if torch.cuda.is_available() else "cpu"
    except ImportError:
        return "cpu"
        
    return "cpu"
