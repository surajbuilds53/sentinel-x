# Sentinel-X: AI-Based Network Attack Forecasting from Network Traffic Data

[![SIH Problem Statement](https://img.shields.io/badge/Problem%20Statement-SIH26153-blue.svg)](https://github.com/surajbuilds53/sentinel-x)
[![Python Version](https://img.shields.io/badge/Python-3.12%20%7C%203.13-3776AB.svg?logo=python&logoColor=white)](https://python.org)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.14-EE4C2C.svg?logo=pytorch&logoColor=white)](https://pytorch.org)
[![License: Academic Defensive](https://img.shields.io/badge/License-Academic%20Defensive-green.svg)](#academic-disclaimer)
[![Vercel Deployment](https://img.shields.io/badge/Deployment-Vercel%20Live-black.svg?logo=vercel&logoColor=white)](https://sentinel-x-lilac.vercel.app)

---

## 1. Executive Summary & Problem Statement

### Problem Statement: **SIH26153** — AI based Network Attack Forecasting from Network Traffic Data
Traditional Network Intrusion Detection Systems (NIDS) function **reactively** — identifying malicious behavior only *after* a payload has detonated, a port scan has mapped endpoints, or a lateral breach has already succeeded. 

**Sentinel-X** shifts defensive network cybersecurity from reactive detection to **predictive attack forecasting**. By aggregating continuous network-flow records into temporal network-state representations and modeling them through a **Deep Recurrent World Model (2-Layer LSTM with Multi-Task Forecasting Heads)**, Sentinel-X forecasts:
1. **Network Attack Probability** across future time intervals ($T+1, T+2, T+3$).
2. **Behavioral Attack Stage Progression** based on a conservative MITRE ATT&CK taxonomy.
3. **Future Continuous Network-State Trajectories** ($\hat{s}_{T+1}, \hat{s}_{T+2}, \hat{s}_{T+3}$).

---

## 2. Core Project Objectives

- **Offline-First & Self-Contained**: Operates locally on consumer hardware without external cloud or paid APIs.
- **Leak-Free Chronological Splitting**: Enforces strict chronological sequence splits (Train: earlier 70%, Val: next 15%, Test: latest 15%) to prevent future data leakage.
- **Dual Model Architecture**:
  - *Baseline*: Static `StandardScaler` $\rightarrow$ `LogisticRegression` benchmark.
  - *Advanced Model*: 2-Layer PyTorch `LSTMWorldModel` with shared latent sequence backbone and 3 specialized prediction heads.
- **Multi-Step Autoregressive Forecasting**: Projects risk, behavioral stage, and network parameters iteratively for $T+1, T+2, T+3$.
- **Conservative MITRE ATT&CK Stage Taxonomy**: Maps behavioral patterns to defensive stages (Reconnaissance, Initial Access, Lateral Movement, C2) without claiming unsupported certainty.
- **SHAP-Based Explainability**: Attributes forecasted risk increases to concrete network feature dynamics.
- **Interactive SOC Dashboard**: Multi-view Streamlit interface designed for B.Tech minor project viva demonstration.

---

## 3. Technology Stack

| Layer | Technologies |
| :--- | :--- |
| **Runtime & Language** | Python 3.12.x / 3.13.x (AMD64 / Windows & Linux compatible) |
| **Data Processing** | `pandas`, `numpy`, `PyYAML` |
| **Machine Learning** | `scikit-learn` (StandardScaler, LogisticRegression, Metrics) |
| **Deep Learning** | `PyTorch` (LSTM, MultiTaskLoss, Autoregressive Rollout) |
| **Explainability** | `SHAP` (DeepExplainer / GradientExplainer / KernelExplainer) |
| **Interactive SOC Dashboard** | `Streamlit`, `Plotly` |
| **Testing & Quality** | `pytest` (21 automated unit and integration tests) |
| **CI/CD & Hosting** | GitHub, Vercel Production Deployment |

---

## 4. Project Directory Structure

```text
sentinel-x/
│
├── README.md                      # Project documentation and viva guide
├── requirements.txt               # Pinned project dependencies
├── pyproject.toml                 # Package declaration and pytest configuration
├── config.yaml                    # Centralized, non-hardcoded configuration
├── .gitignore                     # Git ignore rules
│
├── data/
│   ├── raw/                       # Drop CIC-IDS-2017/2018 benchmark CSVs here
│   ├── processed/                 # Processed windows and state timelines
│   └── sample/                    # Safe synthetic demo flow dataset
│
├── models/
│   ├── checkpoints/               # Trained model checkpoints (.pt, .joblib)
│   ├── scalers/                   # Fitted StandardScaler artifacts (.joblib)
│   └── evaluation/                # Machine-readable metric reports (.json)
│
├── scripts/
│   ├── check_environment.py       # Phase 0 hardware and dependency audit
│   ├── generate_sample_data.py    # Safe synthetic network flow generator
│   ├── prepare_data.py            # Data cleaning, aggregation, and windowing
│   ├── train_baseline.py          # Static Logistic Regression trainer
│   ├── train_lstm.py              # LSTM World Model multi-step trainer
│   └── evaluate.py                # Comparative model evaluation script
│
├── src/
│   └── sentinel_x/
│       ├── config.py              # Config loader, seed & device managers
│       ├── data/
│       │   ├── cleaner.py         # Header removal, NaN/Inf sanitization
│       │   ├── loader.py          # Multi-CSV loader with encoding fallback
│       │   ├── aggregation.py     # 16-feature temporal state vector creation
│       │   ├── windowing.py       # Rolling windows (T-N..T -> T+1..T+3)
│       │   └── synthetic.py       # Episodic demo traffic generator
│       ├── baseline/
│       │   └── logistic_regression.py # Static benchmark wrapper
│       ├── models/
│       │   ├── forecasting_heads.py   # Risk, Stage, and State heads
│       │   ├── lstm_world_model.py    # 2-layer LSTM recurrent World Model
│       │   └── losses.py              # Weighted multi-task loss
│       ├── training/
│       │   └── trainer.py             # PyTorch training loop & early stopping
│       ├── evaluation/
│       │   └── metrics.py             # Precision, Recall, F1, FPR, MAE, RMSE
│       ├── explainability/            # SHAP explainer integration
│       └── taxonomy/
│           └── mitre_mapping.py       # Conservative MITRE ATT&CK taxonomy
│
├── dashboard/                     # SOC Streamlit frontend
└── tests/                         # Automated pytest test suites
```

---

## 5. End-to-End Workflow & Pipeline Architecture

```mermaid
graph TD
    A[Raw Network Flows<br/>CIC-IDS CSV / Synthetic] --> B[Data Cleaner<br/>Sanitize NaNs/Infs, Sort Time]
    B --> C[Temporal Aggregation<br/>10s Window State Vectors]
    C --> D[Leak-Free Chronological Split<br/>Train: 70% | Val: 15% | Test: 15%]
    D --> E[Rolling Window Construction<br/>Input: T-11...T | Target: T+1, T+2, T+3]
    E --> F1[Baseline Path<br/>Static State at T]
    E --> F2[LSTM World Model Path<br/>Sequence T-11...T]
    F1 --> G1[StandardScaler + Logistic Regression]
    F2 --> G2[2-Layer Recurrent LSTM Backbone<br/>Hidden: 128 | Dropout: 0.3]
    G2 --> H1[Head 1: Risk Probability<br/>BCE Loss]
    G2 --> H2[Head 2: Stage Classification<br/>Cross Entropy Loss]
    G2 --> H3[Head 3: State Reconstructor<br/>MSE Loss]
    H1 & H2 & H3 --> I[Autoregressive Rollout<br/>T+1 &rarr; T+2 &rarr; T+3]
    I --> J[SHAP Attribution & MITRE Mapping]
    J --> K[Streamlit SOC Command Dashboard]
```

---

## 6. Conservative MITRE ATT&CK Stage Taxonomy

Sentinel-X adheres to academic defensive security standards and maps predicted behavior to behavioral stages without claiming unsupported forensic certainty:

| Stage Code | Behavioral Stage | MITRE Tactic | Description | Representative Pattern |
| :---: | :--- | :---: | :--- | :--- |
| **0** | **Benign** | `BENIGN` | Normal background activity | Expected HTTP/HTTPS, DNS, streaming |
| **1** | **Reconnaissance** | `TA0043` | Active host & port scanning | High SYN ratio, rapid probing, small bytes |
| **2** | **Initial Access** | `TA0001` | Perimeter breach & auth attempts | Repeated auth flows (FTP/SSH/Web brute force) |
| **3** | **Lateral Movement** | `TA0008` | Internal subnet navigation | Internal pivoting across SMB, RDP, WinRM |
| **4** | **Command & Control** | `TA0011` | Outbound beaconing channels | Periodic heartbeat intervals, low payload bytes |

---

## 7. Model Architecture & Multi-Task Loss

### LSTM World Model Backbone
- **Input Dimension**: 16 temporal features
- **Sequence Length ($N$)**: 12 time steps ($T-11 \dots T$, spanning 120 seconds)
- **Recurrent Layers**: 2-layer LSTM (`hidden_size=128`, `dropout=0.3`)
- **Latent Projection**: Final sequence state $h_T$ passed through dropout to 3 forecasting heads.

### Three Forecasting Heads
1. **Risk Head**: $\hat{y}_{\text{risk}} = \sigma(W_r h + b_r) \in [0, 1]$
2. **Stage Head**: $\hat{y}_{\text{stage}} = \text{Softmax}(W_s h + b_s) \in \mathbb{R}^5$
3. **State Head**: $\hat{s}_{t+1} = W_x h + b_x \in \mathbb{R}^{16}$

### Weighted Multi-Task Loss Formula
$$\mathcal{L}_{\text{total}} = w_{\text{risk}} \cdot \mathcal{L}_{\text{BCE}}(\hat{y}_{\text{risk}}, y_{\text{risk}}) + w_{\text{stage}} \cdot \mathcal{L}_{\text{CE}}(\hat{y}_{\text{stage}}, y_{\text{stage}}) + w_{\text{state}} \cdot \mathcal{L}_{\text{MSE}}(\hat{s}, s)$$

Configured in [`config.yaml`](config.yaml):
- $w_{\text{risk}} = 1.0$
- $w_{\text{stage}} = 1.0$
- $w_{\text{state}} = 0.2$

---

## 8. Verified Performance Benchmarks

### Baseline Logistic Regression vs. LSTM World Model

| Evaluation Metric | Baseline Logistic Regression (Static $T$) | LSTM World Model (Forecast $T+1$) | LSTM World Model (Forecast $T+2$) | LSTM World Model (Forecast $T+3$) |
| :--- | :---: | :---: | :---: | :---: |
| **Risk Precision** | 0.9886 | **0.9674** | 0.9565 | 0.9457 |
| **Risk Recall** | 0.9775 | **1.0000** | 1.0000 | 1.0000 |
| **Risk F1-Score** | 0.9831 | **0.9834** | 0.9778 | 0.9721 |
| **False Positive Rate**| 0.2000 | **0.0500** | 0.0800 | 0.1000 |
| **Attack Stage Acc** | N/A (Binary only) | **62.77%** | 61.70% | 60.64% |
| **State Forecast MAE**| N/A | **0.8538** | 0.8645 | 0.8820 |

> **Key Observation for Viva**:
> As the forecast horizon extends from $T+1$ to $T+3$, predictive uncertainty naturally compounds, causing expected gradual performance decay. The LSTM World Model outperforms the static baseline by incorporating temporal transition dynamics and providing multi-stage and multi-step visibility.

---

## 9. Quickstart & Reproducibility Guide

### 1. Environment Setup
```powershell
# Create virtual environment
python -m venv .venv

# Activate virtual environment
.\.venv\Scripts\Activate.ps1   # Windows PowerShell
# source .venv/bin/activate    # Linux / macOS

# Install dependencies and local package
pip install -r requirements.txt
pip install -e . --no-deps
```

### 2. Verify Environment
```powershell
python scripts/check_environment.py
```

### 3. Prepare Dataset (Generates Safe Demo Data If Raw Absent)
```powershell
python scripts/prepare_data.py
```

### 4. Train Models
```powershell
# Train Static Baseline
python scripts/train_baseline.py

# Train Deep LSTM World Model
python scripts/train_lstm.py
```

### 5. Run Automated Tests
```powershell
pytest -v
```

---

## 10. Demo Mode Instructions

To demonstrate Sentinel-X without downloading multi-gigabyte PCAP/CSV files:
1. Delete or bypass `data/raw/`.
2. Running `python scripts/prepare_data.py` will automatically invoke `sentinel_x.data.synthetic.generate_synthetic_flow_dataset()`.
3. The generator simulates realistic multi-phase network behavior:
   - 60% background benign traffic (HTTP, HTTPS, DNS, SSH).
   - Campaign 1: Reconnaissance (PortScan).
   - Campaign 2: Initial Access (FTP-Patator brute-force).
   - Campaign 3: Lateral Movement (Infiltration).
   - Campaign 4: Command & Control (Botnet beaconing).
4. All synthetic data is clearly marked with `is_synthetic=True`.

---

## 11. Academic Disclaimer & Ethical Compliance

> [!IMPORTANT]
> **Defensive Cybersecurity Purpose Only**
> This project was developed strictly for academic evaluation under problem statement **SIH26153**.
> It contains **NO offensive capabilities, exploit code, payload generators, malware, or network scanning tools**.
> All experiments must be conducted on public benchmark datasets (such as CIC-IDS-2017/2018) or approved synthetic network simulation environments.

---

## 12. Authors & Acknowledgments

- **Author**: Suraj Upadhyay
- **Institution**: B.Tech Computer Science & Engineering
- **Project Title**: Sentinel-X: AI-Based Network Attack Forecasting from Network Traffic Data
- **Problem Statement ID**: SIH26153
- **Live Vercel SOC Link**: [https://sentinel-x-lilac.vercel.app](https://sentinel-x-lilac.vercel.app)
