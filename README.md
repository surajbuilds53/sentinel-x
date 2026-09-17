# Sentinel-X: AI-Based Network Attack Forecasting from Network Traffic Data

[![SIH Problem Statement](https://img.shields.io/badge/Problem%20Statement-SIH26153-blue.svg)](https://github.com/surajbuilds53/sentinel-x)
[![Python Version](https://img.shields.io/badge/Python-3.12%20%7C%203.13-3776AB.svg?logo=python&logoColor=white)](https://python.org)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.14-EE4C2C.svg?logo=pytorch&logoColor=white)](https://pytorch.org)
[![License: Academic Defensive](https://img.shields.io/badge/License-Academic%20Defensive-green.svg)](#3-defensive-scope--ethical-compliance)
[![Vercel Deployment](https://img.shields.io/badge/Deployment-Vercel%20Static%20Landing-black.svg?logo=vercel&logoColor=white)](https://sentinel-x-lilac.vercel.app)

> **B.Tech Minor Project** | **Academic Year 2025–2026**  
> **Problem Statement ID**: SIH26153 — *AI based Network Attack Forecasting from Network Traffic Data*  
> **Primary Author**: Suraj Upadhyay  
> **Domain**: Defensive Machine Learning & Network Telemetry Forecasting

---

## Table of Contents
1. [Project Overview & Problem Statement (SIH26153)](#1-project-overview--problem-statement-sih26153)
2. [Motivation & Theoretical Foundation](#2-motivation--theoretical-foundation)
3. [Defensive Scope & Ethical Compliance](#3-defensive-scope--ethical-compliance)
4. [System Architecture & End-to-End Pipeline](#4-system-architecture--end-to-end-pipeline)
5. [The 16 Aggregated Network-State Features](#5-the-16-aggregated-network-state-features)
6. [Data Pipeline & Leak-Free Windowing Methodology](#6-data-pipeline--leak-free-windowing-methodology)
7. [Dataset Strategy: Benchmark vs. Synthetic Demo](#7-dataset-strategy-benchmark-vs-synthetic-demo)
8. [Baseline Benchmark: Static Logistic Regression](#8-baseline-benchmark-static-logistic-regression)
9. [Deep Learning Architecture: LSTM World Model](#9-deep-learning-architecture-lstm-world-model)
10. [Autoregressive Multi-Step Rollout Mechanism](#10-autoregressive-multi-step-rollout-mechanism)
11. [Multi-Task Loss Formulation](#11-multi-task-loss-formulation)
12. [Empirical Evaluation & Comparative Benchmark](#12-empirical-evaluation--comparative-benchmark)
13. [Explainable AI (XAI) & Threat Attribution via SHAP](#13-explainable-ai-xai--threat-attribution-via-shap)
14. [Conservative MITRE ATT&CK Stage Taxonomy](#14-conservative-mitre-attck-stage-taxonomy)
15. [Hardware & System Requirements](#15-hardware--system-requirements)
16. [Installation & Offline Setup Guide](#16-installation--offline-setup-guide)
17. [Interactive SOC Command Dashboard Walkthrough](#17-interactive-soc-command-dashboard-walkthrough)
18. [Deployment Architecture: Vercel Landing vs. Local Model](#18-deployment-architecture-vercel-landing-vs-local-model)
19. [Viva Preparation Guide & Technical Defense](#19-viva-preparation-guide--technical-defense)

---

## 1. Project Overview & Problem Statement (SIH26153)

Traditional Network Intrusion Detection Systems (NIDS) and SIEM correlation engines operate **retrospectively**: they raise an alert only *after* malicious signatures or statistical anomalies manifest in historical logs. In modern advanced persistent threat (APT) scenarios, waiting for an exploit payload or exfiltration event to trigger an alert leaves security operations centers (SOCs) with zero proactive mitigation buffer.

**Sentinel-X** addresses Smart India Hackathon problem statement **SIH26153** by reframing network intrusion analysis as a **predictive forecasting challenge**. Instead of classifying static flow snapshots, Sentinel-X ingests rolling historical windows of network-state telemetry ($T-11 \dots T$) and employs an autoregressive **Deep Recurrent World Model (2-Layer LSTM with 3 Multi-Task Heads)** to forecast:
1. **Network Attack Risk Probability** across multi-step future horizons ($T+1, T+2, T+3$).
2. **Behavioral Attack Progression Stages** mapped to a conservative MITRE ATT&CK taxonomy.
3. **Continuous Future Network State Trajectories** ($\hat{s}_{T+1}, \hat{s}_{T+2}, \hat{s}_{T+3}$).
4. **Actionable Threat Attribution** via Explainable AI (SHAP) to explain *why* the model predicts risk escalation.

---

## 2. Motivation & Theoretical Foundation

### The Shift from Reactive Detection to Predictive Forecasting
In high-throughput enterprise backbones, reactive alerts lead to two critical operational failure modes:
- **High Mean Time to Remediate (MTTR)**: By the time an intrusion is flagged at time $T$, credentials may have been dumped or command-and-control channels established.
- **Alert Fatigue in Tier-1 SOC Analysts**: Binary alerts provide no visibility into whether network conditions are actively deteriorating or returning to equilibrium.

Forecasting addresses this fundamental limitation:
$$\text{Observed History: } \{s_{T-N}, \dots, s_{T}\} \xrightarrow{\mathcal{M}_{\theta}} \text{Future Forecast: } \{\hat{y}^{\text{risk}}_{T+1}, \hat{y}^{\text{risk}}_{T+2}, \hat{y}^{\text{risk}}_{T+3}\}$$

By predicting risk 10 to 30 seconds into the future, defensive firewalls and rate limiters can proactively deploy automated defensive policies before malicious traffic reaches critical infrastructure.

---

## 3. Defensive Scope & Ethical Compliance

> [!IMPORTANT]
> **Defensive Cybersecurity Policy**
> - Sentinel-X is an **exclusively defensive and academic research project**.
> - The codebase contains **NO exploit payloads, penetration testing scripts, packet injectors, denial-of-service tools, or offensive network scanning mechanisms**.
> - The application operates exclusively in an offline local environment using public academic benchmark datasets (CIC-IDS) or deterministic synthetic statistical traffic simulations.
> - MITRE ATT&CK labels are non-definitive behavioral classifications intended for defensive triage prioritization, not forensic proof of compromise.

---

## 4. System Architecture & End-to-End Pipeline

```mermaid
graph TD
    A[Raw Network Telemetry<br/>CIC-IDS CSV / Synthetic] --> B[Data Sanitization & Cleaning<br/>NaN/Inf Removal, Type Enforcement]
    B --> C[Temporal Window Aggregation<br/>10-Second Windows &rarr; 16-D State Vectors]
    C --> D[Leak-Free Chronological Splitting<br/>Train: 70% | Val: 15% | Test: 15%]
    D --> E[Rolling Sequence Construction<br/>Input: T-11...T &rarr; Target: T+1, T+2, T+3]
    E --> F1[Baseline Pipeline<br/>Current State s_T]
    E --> F2[Recurrent World Model Pipeline<br/>Sequence Window s_{T-11...T}]
    F1 --> G1[StandardScaler + Logistic Regression]
    F2 --> G2[2-Layer PyTorch LSTM Backbone<br/>Hidden Size: 128 | Dropout: 0.3]
    G2 --> H1[Risk Head<br/>BCE Loss]
    G2 --> H2[Stage Head<br/>Cross-Entropy Loss]
    G2 --> H3[State Head<br/>MSE Loss]
    H1 & H2 & H3 --> I[Autoregressive Rollout Engine<br/>Iterative T+1 &rarr; T+2 &rarr; T+3]
    I --> J[SHAP Attribution Engine<br/>Kernel / Gradient Fallback]
    J --> K[Interactive Streamlit SOC Dashboard]
```

---

## 5. The 16 Aggregated Network-State Features

Individual packet-level classification fails on high-speed links due to sheer packet volume and packet loss. Sentinel-X aggregates flows into fixed 10-second non-overlapping windows, extracting a compact 16-dimensional continuous state vector:

| # | Feature Name | Physical Interpretation | Cybersecurity Relevance |
| :-: | :--- | :--- | :--- |
| **1** | `flow_count` | Total active network flows in window | Sudden spikes suggest scanning or high-frequency probing. |
| **2** | `total_packets` | Aggregated packet count across all flows | Distinguishes volumetric bursts from trickle beaconing. |
| **3** | `packet_rate` | Packets per second in window | High rates indicate denial-of-service or brute force attempts. |
| **4** | `total_bytes` | Aggregated transfer volume (bytes) | Identifies heavy data transfers or file exfiltration. |
| **5** | `byte_rate` | Bytes per second in window | Sustained elevated byte rates indicate active outbound transfer. |
| **6** | `duration_mean` | Mean duration of completed flows (ms) | Short flows indicate scanning; long flows indicate persistent connections. |
| **7** | `duration_std` | Standard deviation of flow durations | Low variance in connection duration suggests automated scripts or botnet loops. |
| **8** | `fwd_pkt_len_mean`| Mean length of forward packets (bytes) | Small forward packets align with SYN/ACK probes or ping sweeps. |
| **9** | `bwd_pkt_len_mean`| Mean length of backward packets (bytes)| Asymmetry between fwd/bwd length reveals response sizes (e.g. auth rejection). |
| **10**| `iat_mean` | Mean inter-arrival time between flows (ms)| Irregular bursts vs. rigidly periodic intervals. |
| **11**| `syn_ratio` | Ratio of SYN flags to total flows | Extreme values ($> 0.5$) indicate port scanning or SYN flood attacks. |
| **12**| `rst_ratio` | Ratio of RST flags to total flows | Elevated RST indicates closed ports rejecting connection attempts. |
| **13**| `ack_ratio` | Ratio of ACK flags to total flows | Normal benign traffic maintains high ACK ratios ($> 0.85$). |
| **14**| `fin_ratio` | Ratio of FIN flags to total flows | Monitors graceful session termination frequencies. |
| **15**| `tcp_ratio` | Proportion of TCP traffic in window | Captures transport-layer protocol balance. |
| **16**| `udp_ratio` | Proportion of UDP traffic in window | Captures DNS volume, streaming, or UDP amplification floods. |

---

## 6. Data Pipeline & Leak-Free Windowing Methodology

### Strict Chronological Train / Val / Test Partitioning
Random splitting (such as `train_test_split(shuffle=True)`) creates catastrophic **temporal data leakage** in time-series forecasting. An adversary's probing phase would leak information into the training set about a subsequent breach in the test set.

Sentinel-X enforces **strictly chronological, non-random splits**:
- **Train Split (Earliest 70%)**: Initial benign baseline and early reconnaissance activity.
- **Validation Split (Middle 15%)**: Hyperparameter tuning and model checkpointing during transitional attack phases.
- **Test Split (Latest 15%)**: Final held-out evaluation on unseen future attacks.

### Rolling Horizon Construction
- **Historical Context ($N = 12$)**: Inputs sequence $X = [s_{T-11}, s_{T-10}, \dots, s_{T}]$ (120 seconds of continuous telemetry).
- **Multi-Step Forecasting Targets ($H = 3$)**:
  - $Y_{\text{risk}} = [r_{T+1}, r_{T+2}, r_{T+3}] \in \{0, 1\}^3$
  - $Y_{\text{stage}} = [c_{T+1}, c_{T+2}, c_{T+3}] \in \{0, \dots, 4\}^3$
  - $Y_{\text{state}} = [s_{T+1}, s_{T+2}, s_{T+3}] \in \mathbb{R}^{3 \times 16}$

---

## 7. Dataset Strategy: Benchmark vs. Synthetic Demo

1. **Benchmark Evaluation (CIC-IDS-2017 / CIC-IDS-2018)**:
   - Users can place official benchmark CSV files in `data/raw/`.
   - The data loader automatically standardizes column headers, filters corrupted records, and normalizes features via a fitted `StandardScaler`.
2. **Deterministic Safe Synthetic Flow Generator**:
   - For viva demonstration and environments without multi-gigabyte PCAP downloads, `scripts/prepare_data.py` includes a deterministic synthetic generator (`generate_synthetic_flow_dataset()`).
   - Simulates 6,000 flows containing benign web traffic and 4 progressive attack campaigns (PortScan, Patator brute force, subnet pivot, and C2 beaconing).
   - Every synthetic record is tagged with `is_synthetic=True` for complete research transparency.

---

## 8. Baseline Benchmark: Static Logistic Regression

To prove the necessity of temporal modeling, Sentinel-X includes a baseline benchmark:
- **Architecture**: `StandardScaler` pipeline feeding a regularized `LogisticRegression` classifier ($C = 1.0$, L2 penalty).
- **Inputs**: Only the current instantaneous state vector $s_T$.
- **Limitations**:
  - Cannot model multi-step future horizons ($T+2, T+3$) without external feature engineering.
  - Incapable of autoregressive state projection.
  - Lacks temporal context to distinguish a momentary benign burst from an escalating reconnaissance campaign.

---

## 9. Deep Learning Architecture: LSTM World Model

```text
Input Sequence [Batch, 12, 16]
         │
         ▼
┌──────────────────────────────────────────────┐
│  2-Layer Recurrent LSTM Backbone             │
│  - Input Size: 16                            │
│  - Hidden Size: 128                          │
│  - Dropout: 0.3                              │
└──────────────────────────────────────────────┘
         │
         ▼
   Latent State h_T [Batch, 128]
         │
         ├──────────────────────┬──────────────────────┐
         ▼                      ▼                      ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Risk Head     │    │   Stage Head    │    │   State Head    │
│ Linear(128, 32) │    │ Linear(128, 64) │    │ Linear(128, 64) │
│ ReLU + Dropout  │    │ ReLU + Dropout  │    │ ReLU + Dropout  │
│ Linear(32, 1)   │    │ Linear(64, 5)   │    │ Linear(64, 16)  │
│ Sigmoid         │    │ Logits          │    │ Linear Projection
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                      │                      │
         ▼                      ▼                      ▼
    Risk Prob r_1        Stage Logits l_1       State Pred s_1
```

---

## 10. Autoregressive Multi-Step Rollout Mechanism

Forecasting multiple steps into the future requires an autoregressive rollout:
1. **Step 1 ($T+1$)**: The LSTM processes the full 12-step historical sequence $[s_{T-11} \dots s_T]$ with hidden state initialization $h_0 = 0$. The state head produces predicted state $\hat{s}_{T+1}$, while the risk and stage heads predict $r_{T+1}$ and $c_{T+1}$.
2. **Step 2 ($T+2$)**: The predicted state $\hat{s}_{T+1}$ is fed back as input for a single recurrent step using the updated recurrent hidden state $(h_1, c_1)$, outputting $\hat{s}_{T+2}, r_{T+2}, c_{T+2}$.
3. **Step 3 ($T+3$)**: $\hat{s}_{T+2}$ is fed into the recurrent cell with $(h_2, c_2)$, outputting $\hat{s}_{T+3}, r_{T+3}, c_{T+3}$.

This closed-loop rollout enables the model to predict how the network environment will dynamically evolve under attack.

---

## 11. Multi-Task Loss Formulation

The network is trained end-to-end using a joint weighted loss function:

$$\mathcal{L}_{\text{total}} = w_{\text{risk}} \cdot \mathcal{L}_{\text{BCE}}(\hat{r}, r) + w_{\text{stage}} \cdot \mathcal{L}_{\text{CE}}(\hat{c}, c) + w_{\text{state}} \cdot \mathcal{L}_{\text{MSE}}(\hat{s}, s)$$

- **Binary Cross Entropy ($\mathcal{L}_{\text{BCE}}$)**: Penalizes incorrect attack probability predictions across all forecast horizons.
- **Categorical Cross Entropy ($\mathcal{L}_{\text{CE}}$)**: Supervises the behavioral MITRE stage classifier over the 5 stage classes.
- **Mean Squared Error ($\mathcal{L}_{\text{MSE}}$)**: Constrains the continuous state reconstructor to preserve physical telemetry dynamics.
- **Weights**: Configured in `config.yaml` as $w_{\text{risk}} = 1.0$, $w_{\text{stage}} = 1.0$, $w_{\text{state}} = 0.2$.

---

## 12. Empirical Evaluation & Comparative Benchmark

The following metrics are generated on the held-out test split (stored in `models/evaluation/model_comparison.json`):

| Evaluation Metric | Baseline Logistic Regression (Static $T$) | LSTM World Model (Forecast $T+1$) | LSTM World Model (Forecast $T+2$) | LSTM World Model (Forecast $T+3$) |
| :--- | :---: | :---: | :---: | :---: |
| **Risk Precision** | 0.9886 | **0.9674** | 0.9565 | 0.9457 |
| **Risk Recall** | 0.9775 | **1.0000** | 1.0000 | 1.0000 |
| **Risk F1-Score** | 0.9831 | **0.9834** | 0.9778 | 0.9721 |
| **False Positive Rate**| 0.2000 | **0.0500** | 0.0800 | 0.1000 |
| **Attack Stage Accuracy** | N/A (Binary Only) | **62.77%** | 61.70% | 60.64% |
| **State Forecast MAE**| N/A | **0.8538** | 0.8645 | 0.8820 |

### Key Engineering Takeaways:
1. **Zero Missed Attacks ($100\%$ Recall)**: The LSTM World Model achieves perfect recall on $T+1$, ensuring defensive teams do not miss incoming attack waves.
2. **75% Reduction in False Positives**: The false positive rate drops from $20\%$ (baseline) down to $5\%$ ($T+1$), reducing SOC alert fatigue.
3. **Expected Horizon Degradation**: As forecast horizon extends from $T+1$ to $T+3$, predictive uncertainty naturally causes F1-score to taper from $0.9834$ to $0.9721$.

---

## 13. Explainable AI (XAI) & Threat Attribution via SHAP

Black-box neural network predictions are unacceptable in defensive operations. Sentinel-X integrates **SHAP (SHapley Additive exPlanations)** via `SentinelXExplainer`:

- **SHAP KernelExplainer**: Evaluates marginal feature contributions against a summary background distribution of benign network sequences.
- **Signed Feature Attribution**:
  - **Risk Drivers (Red)**: Features pushing future risk upward (e.g. `syn_ratio` $+0.3547$, `packet_rate` $+0.2463$).
  - **Risk Inhibitors (Green)**: Features anchoring risk downward (e.g. `ack_ratio` $-0.1299$, `duration_mean` $-0.0845$).
- **Temporal Saliency**: Measures which historical sequence steps ($T-11 \dots T$) exerted the greatest influence on the future prediction.
- **Deterministic Gradient Fallback**: If background sampling encounters degenerate matrices, the explainer seamlessly falls back to gradient-based input saliency ($\nabla_x \cdot x$).

---

## 14. Conservative MITRE ATT&CK Stage Taxonomy

Sentinel-X maps behavioral predictions to a conservative 5-stage taxonomy:

| Stage Code | Behavioral Label | MITRE Tactic | Academic Definition | Telemetry Pattern |
| :-: | :--- | :---: | :--- | :--- |
| **0** | **Benign** | `BENIGN` | Normal background operational traffic | High ACK ratio, stable flow duration, low SYN count |
| **1** | **Reconnaissance** | `TA0043` | Active host discovery & port enumeration | High SYN ratio, high flow count, minimal backward bytes |
| **2** | **Initial Access** | `TA0001` | Authentication brute force / exploit attempt | Elevated byte rates, repeated connections to auth ports |
| **3** | **Lateral Movement** | `TA0008` | Internal subnet pivot & host traversal | Bursty flow intervals across SMB/RDP/WinRM ports |
| **4** | **Command & Control**| `TA0011` | Outbound beaconing / management channel | Periodic inter-arrival intervals, consistent payload sizes |

---

## 15. Hardware & System Requirements

Sentinel-X was engineered to operate on standard academic laptop hardware:
- **Operating System**: Windows 10/11, Ubuntu Linux 22.04+, or macOS (Apple Silicon / Intel).
- **Python**: 3.12.x or 3.13.x.
- **CPU**: Intel Core i5 / AMD Ryzen 5 or higher (multithreaded data loading).
- **RAM**: Minimum 8 GB (16 GB recommended for full CIC-IDS datasets).
- **GPU (Optional)**: NVIDIA CUDA 11.8+ supported; single-sample dashboard inference executes in $< 20\text{ ms}$ on standard CPU.
- **Disk Space**: ~500 MB for repository, dependencies, and model checkpoints.

---

## 16. Installation & Offline Setup Guide

### 1. Clone Repository & Setup Virtual Environment
```powershell
git clone https://github.com/surajbuilds53/sentinel-x.git
cd sentinel-x

# Create virtual environment
python -m venv .venv

# Activate virtual environment
.\.venv\Scripts\Activate.ps1    # Windows PowerShell
# source .venv/bin/activate     # Linux / macOS
```

### 2. Install Dependencies
```powershell
pip install -r requirements.txt
pip install -e . --no-deps
```

### 3. Run Environment Audit
```powershell
python scripts/check_environment.py
```

### 4. Prepare Dataset & Train Models
```powershell
# Prepares data (uses synthetic generator if data/raw is empty)
python scripts/prepare_data.py

# Train baseline and LSTM World Model
python scripts/train_baseline.py
python scripts/train_lstm.py

# Run comparative evaluation & SHAP attribution
python scripts/evaluate.py
```

### 5. Run Automated Tests
```powershell
pytest -v
```

### 6. Launch the Interactive SOC Dashboard
```powershell
streamlit run dashboard/app.py
```
Open your browser at `http://localhost:8501`.

---

## 17. Interactive SOC Command Dashboard Walkthrough

The Streamlit dashboard (`dashboard/app.py`) provides 5 dedicated defensive views:

1. **Executive Risk Overview (View 1)**:
   - Live risk probability gauge with dynamic status coloring (Green: Normal, Amber: Warning, Red: Critical).
   - Multi-step trend delta ($T+3 - T$) indicating whether threats are escalating or de-escalating.
   - MITRE ATT&CK behavioral stage card with model confidence and academic non-definitive notice.
2. **Forecast Timeline (View 2)**:
   - Line chart contrasting verified historical observations ($T-11 \dots T$) against future autoregressive rollouts ($T+1, T+2, T+3$).
   - 95% forecast confidence interval band expanding across the forecast horizon.
3. **Threat Attribution & Explainability (View 3)**:
   - Signed horizontal bar chart displaying SHAP feature contributions.
   - Top positive risk drivers (red) vs. negative risk inhibitors (green).
   - Historical temporal importance bar chart across sequence steps $T-11 \dots T$.
4. **Model Performance & Comparative Benchmark (View 4)**:
   - Full comparative evaluation table contrasting Logistic Regression against the LSTM World Model.
   - Multi-step Precision, Recall, and F1-score grouped bar charts.
   - Degradation curves illustrating stage accuracy decay and state forecast MAE across horizons.
5. **System Diagnostics & Telemetry Pipeline (View 5)**:
   - Real-time environment telemetry: Python/PyTorch versions, CPU/CUDA hardware status, active dataset mode.
   - Model checkpoint registry table reporting artifact status, file size, and path verification.

---

## 18. Deployment Architecture: Vercel Landing vs. Local Model

To ensure transparency regarding deployment:
- **Streamlit + PyTorch Local Execution**: The deep learning inference engine, PyTorch models, and interactive Streamlit UI run locally (`http://localhost:8501`) because serverless cloud tiers (such as free Vercel serverless functions) cannot sustain long-running PyTorch neural network checkpoints or Python runtime dependencies without a separate GPU backend.
- **Vercel Static Landing Page**: The live Vercel deployment at [https://sentinel-x-lilac.vercel.app](https://sentinel-x-lilac.vercel.app) hosts the static project command center, documentation, architecture diagrams, and viva reference materials.

---

## 19. Viva Preparation Guide & Technical Defense

### Expected Examiner Questions & Model Answers

**Q1: Why use an LSTM World Model instead of a simpler classifier like Random Forest or XGBoost?**  
*Answer*: Random Forest and XGBoost excel at classifying isolated, independent feature vectors. However, network intrusions are inherently **sequential processes** that unfold over time (e.g., scanning $\rightarrow$ credential brute-force $\rightarrow$ lateral pivot). The LSTM maintains a persistent hidden recurrent state across time steps, enabling it to model temporal dependencies. Crucially, the World Model includes a **state reconstructor head** that forecasts future network telemetry ($\hat{s}_{T+1}$), which is fed back autoregressively to predict multi-step horizons ($T+2, T+3$). Static tree models cannot perform closed-loop autoregressive state projection.

**Q2: How do you prevent data leakage during time-series data preparation?**  
*Answer*: We enforce strict chronological partitioning without shuffling. The first 70% of chronological time steps forms the training set, the next 15% forms the validation set, and the final 15% forms the held-out test set. Standard scalers are fitted **only on the training split** and applied transformationally to validation and test splits. Rolling windows are constructed strictly such that inputs span $[T-11 \dots T]$ and targets span $[T+1 \dots T+3]$ with no temporal overlap across split boundaries.

**Q3: Why is forecasting risk more valuable to a SOC than detection?**  
*Answer*: Traditional NIDS alerts after an attack packet has been delivered, forcing SOC analysts into a reactive incident response cycle. Forecasting provides proactive lead time (e.g., 10 to 30 seconds). If Sentinel-X forecasts a $95\%$ probability of initial access within $T+1$, automated firewall rules can dynamically rate-limit suspicious IPs or isolate vulnerable subnets *before* the attacker establishes command-and-control access.

**Q4: What are the primary limitations of your implementation?**  
*Answer*: First, the autoregressive rollout incurs gradual error compounding; predictions at $T+3$ inherently have wider uncertainty bands than $T+1$. Second, our multi-stage classifier assumes network intrusions follow a progression loosely aligned with MITRE ATT&CK; zero-day attacks that bypass reconnaissance straight to data exfiltration may exhibit lower stage classification confidence. Third, high-throughput deployment requires hardware acceleration (GPU/TPU) for sub-millisecond batch aggregation.

---

## License & Academic Attribution
Developed for academic presentation and defensive cybersecurity evaluation under problem statement **SIH26153**.
Licensed under the [MIT License](LICENSE).
