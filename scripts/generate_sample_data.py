#!/usr/bin/env python3
"""SAFE Synthetic Network Traffic Generator for Sentinel-X Demonstration.

Defensive Cybersecurity B.Tech Minor Project (SIH26153).
"""

from pathlib import Path
import argparse
from sentinel_x.config import PROJECT_ROOT
from sentinel_x.data.synthetic import generate_synthetic_flow_dataset


def main():
    parser = argparse.ArgumentParser(description="Generate safe synthetic demo flows for Sentinel-X")
    parser.add_argument("--flows", type=int, default=6000, help="Number of flow records to generate")
    parser.add_argument("--output", type=str, default=str(PROJECT_ROOT / "data" / "sample" / "synthetic_flows.csv"))
    args = parser.parse_args()
    
    df = generate_synthetic_flow_dataset(num_flows=args.flows, output_path=args.output)
    print(f"[+] Successfully generated {len(df)} synthetic demo flows -> {args.output}")


if __name__ == "__main__":
    main()
