#!/usr/bin/env python3
"""Environment and Dependency Verification Script for Sentinel-X.

Defensive Cybersecurity B.Tech Minor Project (SIH26153).
"""

import sys
import platform
from pathlib import Path

REQUIRED_PACKAGES = [
    ("yaml", "PyYAML"),
    ("numpy", "numpy"),
    ("pandas", "pandas"),
    ("sklearn", "scikit-learn"),
    ("torch", "torch"),
    ("shap", "shap"),
    ("streamlit", "streamlit"),
    ("plotly", "plotly"),
    ("pytest", "pytest"),
]

REQUIRED_DIRS = [
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


def check_python() -> bool:
    print("=" * 65)
    print(" SENTINEL-X | ENVIRONMENT AUDIT (PHASE 0)")
    print("=" * 65)
    py_ver = sys.version.split()[0]
    print(f"[*] Operating System : {platform.system()} {platform.release()} ({platform.machine()})")
    print(f"[*] Python Version   : {py_ver} ({sys.executable})")
    
    if sys.version_info >= (3, 11):
        print("    [+] Python version meets requirements (>= 3.11).")
        return True
    else:
        print("    [-] Python version is below 3.11. Recommend 3.12 or 3.13.")
        return False


def check_gpu() -> None:
    print("\n" + "-" * 65)
    print(" HARDWARE ACCELERATION & COMPUTE DEVICE")
    print("-" * 65)
    try:
        import torch
        cuda_avail = torch.cuda.is_available()
        print(f"[*] PyTorch Version : {torch.__version__}")
        print(f"[*] CUDA Available  : {cuda_avail}")
        if cuda_avail:
            device_count = torch.cuda.device_count()
            current_dev = torch.cuda.current_device()
            dev_name = torch.cuda.get_device_name(current_dev)
            vram_gb = torch.cuda.get_device_properties(current_dev).total_memory / (1024 ** 3)
            print(f"[*] GPU Device ({current_dev + 1}/{device_count}) : {dev_name}")
            print(f"[*] Total VRAM      : {vram_gb:.2f} GB")
            print("    [+] NVIDIA GPU acceleration enabled.")
        else:
            print("    [!] CUDA not active or PyTorch CPU-only build.")
            print("    [*] Fallback: Model will execute on CPU (fully supported).")
    except ImportError:
        print("    [-] PyTorch is not yet installed in this environment.")


def check_packages() -> bool:
    print("\n" + "-" * 65)
    print(" REQUIRED DEPENDENCIES STATUS")
    print("-" * 65)
    all_ok = True
    for mod_name, pkg_name in REQUIRED_PACKAGES:
        try:
            mod = __import__(mod_name)
            ver = getattr(mod, "__version__", "installed")
            print(f"    [+] {pkg_name:16s} : {ver}")
        except ImportError as e:
            print(f"    [-] {pkg_name:16s} : MISSING ({e})")
            all_ok = False
    return all_ok


def check_directories() -> bool:
    print("\n" + "-" * 65)
    print(" PROJECT STRUCTURE VERIFICATION")
    print("-" * 65)
    root = Path(__file__).resolve().parent.parent
    all_ok = True
    for d in REQUIRED_DIRS:
        target = root / d
        if target.is_dir():
            print(f"    [+] Directory exists: {d}")
        else:
            print(f"    [-] Directory missing: {d}")
            all_ok = False
            
    config_file = root / "config.yaml"
    if config_file.is_file():
        print(f"    [+] Config file exists: config.yaml")
    else:
        print(f"    [-] Config file missing: config.yaml")
        all_ok = False
        
    return all_ok


def main():
    py_ok = check_python()
    check_gpu()
    pkgs_ok = check_packages()
    dirs_ok = check_directories()
    
    print("\n" + "=" * 65)
    if py_ok and pkgs_ok and dirs_ok:
        print(" [SUCCESS] Phase 0 & Phase 1 Environment Audit Passed!")
    else:
        print(" [NOTE] Some packages or directories require setup before training.")
    print("=" * 65)


if __name__ == "__main__":
    main()
