"""Conservative MITRE ATT&CK behavioral stage taxonomy and mapping helpers.

Defensive Cybersecurity B.Tech Minor Project (SIH26153).
Maps observed network behavior to conservative stages rather than claiming exact certainty.
"""

from typing import Dict, Any, Optional

STAGE_TAXONOMY: Dict[int, Dict[str, str]] = {
    0: {
        "name": "Benign",
        "tactic_id": "BENIGN",
        "label": "Benign / Normal Operations",
        "description": "Normal, expected network baseline activity without anomalous or malicious indicators.",
        "risk_level": "LOW",
        "color": "#10b981",  # Emerald green
    },
    1: {
        "name": "Reconnaissance",
        "tactic_id": "TA0043",
        "label": "Predicted Behavioral Stage: Reconnaissance (TA0043)",
        "description": "Adversary attempting to gather network topology, active hosts, and open ports (e.g. port scanning, sweeping).",
        "risk_level": "MEDIUM",
        "color": "#f59e0b",  # Amber
    },
    2: {
        "name": "Initial Access",
        "tactic_id": "TA0001",
        "label": "Predicted Behavioral Stage: Initial Access (TA0001)",
        "description": "Adversary attempting to penetrate network perimeters or authenticate unauthorized accounts (e.g. brute force, exploit attempts).",
        "risk_level": "HIGH",
        "color": "#f97316",  # Orange
    },
    3: {
        "name": "Lateral Movement",
        "tactic_id": "TA0008",
        "label": "Predicted Behavioral Stage: Lateral Movement (TA0008)",
        "description": "Adversary attempting to extend access and pivot across internal network segments or hosts.",
        "risk_level": "CRITICAL",
        "color": "#ef4444",  # Red
    },
    4: {
        "name": "Command and Control",
        "tactic_id": "TA0011",
        "label": "Predicted Behavioral Stage: Command and Control (TA0011)",
        "description": "Adversary maintaining persistent outbound beaconing or communication channels with remote infrastructure.",
        "risk_level": "CRITICAL",
        "color": "#8b5cf6",  # Purple
    },
}

# Mapping benchmark dataset labels (CIC-IDS-2017 & 2018) to conservative stages
RAW_LABEL_MAPPING: Dict[str, int] = {
    # 0: Benign
    "benign": 0,
    "normal": 0,
    
    # 1: Reconnaissance (TA0043)
    "portscan": 1,
    "port scan": 1,
    "probe": 1,
    "ipsweep": 1,
    "nmap": 1,
    
    # 2: Initial Access (TA0001)
    "ftp-patator": 2,
    "ssh-patator": 2,
    "web attack": 2,
    "web attack – brute force": 2,
    "web attack – xss": 2,
    "web attack – sql injection": 2,
    "brute force": 2,
    "heartbleed": 2,
    "dos": 2,
    "dos slowloris": 2,
    "dos slowhttptest": 2,
    "dos hulk": 2,
    "dos goldeneye": 2,
    "ddos": 2,
    
    # 3: Lateral Movement (TA0008)
    "infiltration": 3,
    "lateral": 3,
    "internal pivot": 3,
    
    # 4: Command and Control (TA0011)
    "bot": 4,
    "botnet": 4,
    "c2": 4,
    "command and control": 4,
    "beaconing": 4,
}


def map_raw_label_to_stage(label: str) -> int:
    """Map raw flow label string to conservative 5-stage taxonomy class [0-4].
    
    Args:
        label: Raw label from dataset (case-insensitive).
        
    Returns:
        Integer stage code (0 to 4). Defaults to 0 (Benign) if unknown or unclassified.
    """
    clean_label = str(label).strip().lower()
    
    # Direct lookup
    if clean_label in RAW_LABEL_MAPPING:
        return RAW_LABEL_MAPPING[clean_label]
        
    # Substring search for common variants
    for key, stage_code in RAW_LABEL_MAPPING.items():
        if key in clean_label:
            return stage_code
            
    return 0


def get_stage_metadata(stage_code: int) -> Dict[str, Any]:
    """Retrieve metadata and defensive guidance for a predicted behavioral stage.
    
    Args:
        stage_code: Integer between 0 and 4.
        
    Returns:
        Dict containing stage name, tactic_id, display label, description, and risk level.
    """
    return STAGE_TAXONOMY.get(int(stage_code), STAGE_TAXONOMY[0])
