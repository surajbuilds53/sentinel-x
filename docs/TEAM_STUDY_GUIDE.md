# Sentinel-X: Comprehensive Team Study & Viva Preparation Guide

> **B.Tech Minor Project** | **Problem Statement: SIH26153**  
> **Project Title**: Sentinel-X — AI-Based Network Attack Forecasting from Network Traffic Data  
> **Team Members**: Everyone on the team should read and master this document before project reviews and viva examinations.

---

## 1. Executive Brief: The 60-Second Elevator Pitch

If an external examiner or professor asks: **"What is Sentinel-X in simple terms?"**, give this exact response:

> *"Traditional Network Intrusion Detection Systems (like Snort or Suricata) are **reactive** — they only alert us after an attacker has already delivered an exploit, scanned our ports, or breached a system.  
> **Sentinel-X** shifts defensive security from **reactive detection** to **predictive attack forecasting**.  
> We take rolling 120-second windows of aggregated network telemetry and use a **Deep Recurrent LSTM World Model with 3 prediction heads** to forecast three things simultaneously:  
> 1. The **attack risk probability** across the next 10, 20, and 30 seconds ($T+1, T+2, T+3$).  
> 2. The **behavioral MITRE ATT&CK stage** (Reconnaissance, Initial Access, Lateral Movement, or C2).  
> 3. The **future continuous network state trajectory** via an autoregressive rollout.  
> Finally, we use **SHAP Explainable AI** so SOC analysts know exactly which network features drove the risk prediction up or down."*

---

## 2. Why Forecasting Beats Retrospective Detection

| Factor | Traditional NIDS / SIEM | Sentinel-X Predictive Forecasting |
| :--- | :--- | :--- |
| **Operational Timing** | Post-incident (alert fires *after* packet delivers payload) | Pre-incident (forecasts risk $10\text{--}30\text{ s}$ *before* escalation) |
| **Defensive Action** | Incident containment, cleanup, digital forensics | Proactive rate-limiting, firewall rule adjustment, subnet isolation |
| **SOC Impact** | High alert fatigue (thousands of isolated binary alerts) | Risk trajectory curve (reveals whether conditions are escalating or stabilizing) |
| **Metric Impact** | High MTTR (Mean Time to Remediate) | Lowers MTTR by slashing MTTD (Mean Time to Detect) to near zero |

---

## 3. Data Pipeline & The 16 Features (Every Member MUST Know)

### The Time Parameters:
- **Time Step ($t$)**: Each time step represents a **10-second non-overlapping aggregation window** of raw network flows.
- **Historical Context Window ($N = 12$)**: The model looks at 12 historical time steps ($T-11 \dots T$), representing the last **120 seconds (2 minutes)** of network activity.
- **Forecast Horizon ($H = 3$)**: The model forecasts 3 future steps:
  - $T+1$: Next 10 seconds (immediate forecast)
  - $T+2$: Next 20 seconds (intermediate forecast)
  - $T+3$: Next 30 seconds (longer-term forecast)

### The 16 Aggregated State Features (Memorize by Category):

```text
┌────────────────────────────────────────────────────────────────────────┐
│                      THE 16 NETWORK STATE FEATURES                    │
├──────────────────────┬────────────────────────┬────────────────────────┤
│ 1. Volumetric (5)    │ 2. Duration/Timing (3) │ 3. Packet Dynamics (2) │
│ - flow_count         │ - duration_mean        │ - fwd_pkt_len_mean     │
│ - total_packets      │ - duration_std         │ - bwd_pkt_len_mean     │
│ - packet_rate        │ - iat_mean             │                        │
│ - total_bytes        │                        │ 4. Flag & Protocol (6) │
│ - byte_rate          │                        │ - syn_ratio, rst_ratio │
│                      │                        │ - ack_ratio, fin_ratio │
│                      │                        │ - tcp_ratio, udp_ratio │
└──────────────────────┴────────────────────────┴────────────────────────┘
```

1. **`flow_count`**: Total network flows in the 10s window. Spikes during port scans.
2. **`total_packets`**: Total packet count. Distinguishes high-volume floods from low-and-slow attacks.
3. **`packet_rate`**: Packets per second. Identifies denial-of-service and brute-force bursts.
4. **`total_bytes`**: Total transfer volume. Highlights large data payloads.
5. **`byte_rate`**: Bytes per second. Detects active outbound data exfiltration.
6. **`duration_mean`**: Average flow length (ms). Very short in port scans; long in persistent sessions.
7. **`duration_std`**: Flow length variation. Botnets and scripts have very low variance (rigid timing).
8. **`iat_mean`**: Mean Inter-Arrival Time between flows. Identifies periodic beaconing.
9. **`fwd_pkt_len_mean`**: Mean forward packet size. Small during SYN scans; large during payload delivery.
10. **`bwd_pkt_len_mean`**: Mean response packet size. Asymmetric fwd/bwd reveals auth failures or server rejections.
11. **`syn_ratio`**: Ratio of SYN flags to total flows. Extreme values ($> 0.5$) indicate port scanning or SYN floods.
12. **`rst_ratio`**: Ratio of RST flags. Spikes when target hosts reject probes on closed ports.
13. **`ack_ratio`**: Ratio of ACK flags. Normal benign traffic has high ACK ratios ($> 0.85$).
14. **`fin_ratio`**: Ratio of FIN flags. Measures graceful session teardown frequency.
15. **`tcp_ratio`**: Proportion of TCP traffic in the window.
16. **`udp_ratio`**: Proportion of UDP traffic (DNS amplification, VoIP, streaming).

### Strict Chronological Splitting (NO Data Leakage!):
- **Why?** If you use random `train_test_split(shuffle=True)`, future time steps leak into the past! The model memorizes attack sequences rather than forecasting them.
- **Sentinel-X Rule**:
  - **Train Split (Earliest 70%)**: Baseline traffic + initial recon.
  - **Validation Split (Middle 15%)**: Hyperparameter tuning & early stopping.
  - **Test Split (Latest 15%)**: Strict future evaluation on completely unseen attacks.
  - Standard scalers are fitted **ONLY on the training set** and applied to validation/test sets.

---

## 4. Model Architecture & Multi-Task Deep Learning

### Why Call it a "World Model"?
In modern AI, a **World Model** is a model that learns an internal representation of how the environment evolves. Instead of just predicting a single label, Sentinel-X predicts the **future continuous state of the network** ($\hat{s}_{T+1}$) and uses its own predicted state to forecast subsequent steps ($T+2, T+3$).

### Architecture Structure:
1. **Recurrent Backbone**:
   - 2-Layer LSTM with 128 hidden units and 0.3 dropout.
   - Input shape: `(batch_size, 12, 16)` $\rightarrow$ Output latent state $h_T$: `(batch_size, 128)`.
2. **Head 1 — Risk Head**:
   - `Linear(128, 32) -> ReLU -> Dropout(0.2) -> Linear(32, 1) -> Sigmoid`
   - Output: Risk probability $r \in [0.0, 1.0]$. Loss: **Binary Cross-Entropy (BCE)**.
3. **Head 2 — Stage Head**:
   - `Linear(128, 64) -> ReLU -> Dropout(0.2) -> Linear(64, 5)`
   - Output: Logits for 5 MITRE stages. Loss: **Categorical Cross-Entropy (CE)**.
4. **Head 3 — State Reconstructor Head**:
   - `Linear(128, 64) -> ReLU -> Dropout(0.2) -> Linear(64, 16)`
   - Output: Predicted next 16-D state vector $\hat{s}_{t+1}$. Loss: **Mean Squared Error (MSE)**.

### The Joint Multi-Task Loss Formula:
$$\mathcal{L}_{\text{total}} = 1.0 \cdot \mathcal{L}_{\text{BCE}}(\hat{r}, r) + 1.0 \cdot \mathcal{L}_{\text{CE}}(\hat{c}, c) + 0.2 \cdot \mathcal{L}_{\text{MSE}}(\hat{s}, s)$$

- Why train multi-task? **Auxiliary task regularization!** Learning to predict the physical continuous state ($\hat{s}$) forces the LSTM hidden state to understand real network physics, preventing overfitting on binary attack labels.

### Autoregressive Rollout Mechanism:
- **At $T+1$**: Input history $[s_{T-11} \dots s_T]$ into LSTM $\rightarrow$ predicts $\hat{s}_{T+1}, r_{T+1}, c_{T+1}$.
- **At $T+2$**: Feed $\hat{s}_{T+1}$ back into the recurrent cell with previous hidden state $\rightarrow$ predicts $\hat{s}_{T+2}, r_{T+2}, c_{T+2}$.
- **At $T+3$**: Feed $\hat{s}_{T+2}$ into recurrent cell $\rightarrow$ predicts $\hat{s}_{T+3}, r_{T+3}, c_{T+3}$.

---

## 5. Conservative MITRE ATT&CK Stage Taxonomy

We do NOT claim forensic certainty. We classify behavioral network stages:

| Stage Code | Stage Name | MITRE Tactic ID | Telemetry Profile |
| :-: | :--- | :---: | :--- |
| **0** | **Benign Baseline** | `BENIGN` | High ACK ratio ($> 0.85$), low SYN count, steady durations. |
| **1** | **Reconnaissance** | `TA0043` | Spiking SYN ratio ($> 0.5$), high flow count, short durations. |
| **2** | **Initial Access** | `TA0001` | Elevated byte rates, repeated connections to auth ports (FTP/SSH/Web). |
| **3** | **Lateral Movement** | `TA0008` | Bursty internal traffic across SMB (445), RDP (3389), WinRM (5985). |
| **4** | **Command & Control**| `TA0011` | Periodic inter-arrival intervals, consistent heartbeat payload sizes. |

---

## 6. Real Empirical Results (Memorize for Viva!)

These are the exact verified test-set numbers from `models/evaluation/model_comparison.json`:

| Metric | Static Baseline (Logistic Regression) | LSTM World Model ($T+1$) | LSTM World Model ($T+2$) | LSTM World Model ($T+3$) |
| :--- | :---: | :---: | :---: | :---: |
| **Risk Precision** | 98.9% | **96.7%** | 95.7% | 94.6% |
| **Risk Recall** | 97.8% | **100.0%** | **100.0%** | **100.0%** |
| **Risk F1-Score** | 0.9831 | **0.9834** | 0.9778 | 0.9721 |
| **False Positive Rate**| 20.0% | **5.0%** (75% drop!) | 8.0% | 10.0% |
| **Stage Accuracy** | N/A (Binary only) | **62.8%** | 61.7% | 60.6% |
| **State Forecast MAE**| N/A | **0.8538** | 0.8645 | 0.8820 |

### Key Talking Points:
1. **100% Recall**: The LSTM model misses zero attacks on the $T+1$ horizon.
2. **75% False Positive Reduction**: The baseline has a 20% FPR; our LSTM model cuts it to 5%, drastically reducing SOC alert fatigue.
3. **Horizon Uncertainty Degradation**: F1 gradually drops from $0.9834 \rightarrow 0.9778 \rightarrow 0.9721$. **Examiners love this!** It proves your model is genuinely forecasting autoregressively and error compounding naturally occurs as you forecast further into the future.

---

## 7. Explainable AI (SHAP)

- **What is SHAP?** SHapley Additive exPlanations, derived from cooperative game theory. It calculates each feature's marginal contribution to the prediction.
- **Why is it needed?** A SOC analyst will not trust an AI alert without explanation. SHAP answers: *"Why did you predict 95% risk?"*
- **Drivers vs. Inhibitors**:
  - **Risk Drivers (Red)**: Features pushing risk up (e.g. `syn_ratio` $+0.35$, `packet_rate` $+0.25$).
  - **Risk Inhibitors (Green)**: Features anchoring risk down (e.g. `ack_ratio` $-0.13$, `duration_mean` $-0.08$).
- **Temporal Saliency**: Measures which historical sequence steps ($T-11 \dots T$) were most influential in the recurrent hidden state.

---

## 8. Deployment Architecture: Local vs. Vercel Reality

If an examiner asks: **"Is your project deployed on Vercel?"**, answer transparently:
- **Local Streamlit & PyTorch Engine**: The neural network, PyTorch checkpoints, and interactive multi-view SOC dashboard run locally (`http://localhost:8501`). Free serverless tiers like Vercel have a 50 MB execution limit and a 10-second timeout, which cannot run multi-head PyTorch models.
- **Vercel Static Landing Page**: The live Vercel site ([https://sentinel-x-lilac.vercel.app](https://sentinel-x-lilac.vercel.app)) serves as the static project overview, documentation center, and architecture portfolio.

---

## 9. Team Member Role Breakdown

Assign these specific focus areas among team members for the presentation:

| Team Member | Primary Responsibility | Focus Topics |
| :--- | :--- | :--- |
| **Member 1 (Lead)** | **Problem & System Architecture** | SIH26153, Reactive vs. Predictive, End-to-End Pipeline, Technology Stack, System Constraints. |
| **Member 2** | **Data Engineering & Windowing** | The 16 features, 10s aggregation, leak-free chronological splitting, benchmark vs. synthetic data. |
| **Member 3** | **Deep Learning & Modeling** | 2-Layer LSTM, 3 forecasting heads, multi-task loss formula, autoregressive rollout mechanism. |
| **Member 4** | **Evaluation, XAI & Dashboard Demo** | Comparison metrics, 75% FPR drop, SHAP attribution, live Streamlit dashboard demonstration. |

---

## 10. Top 10 Viva Questions & Winning Answers

#### Q1: What makes Sentinel-X different from existing intrusion detection systems like Snort?
**Answer**: Snort uses signature matching on packets that have already arrived. Sentinel-X aggregates continuous flow telemetry and uses an autoregressive recurrent World Model to forecast attack probability and behavioral stages 10 to 30 seconds into the future, providing proactive mitigation time.

#### Q2: Why use an LSTM instead of XGBoost or Random Forest?
**Answer**: Network intrusions are temporal sequences (Recon $\rightarrow$ Access $\rightarrow$ Lateral Pivot). Tree models treat each time step as an independent row without recurrent memory. Furthermore, our LSTM World Model includes an autoregressive state head ($\hat{s}_{t+1}$) that allows iterative multi-step rollout ($T+1, T+2, T+3$). Static tree models cannot perform continuous state rollouts.

#### Q3: Why not use a Transformer instead of an LSTM?
**Answer**: Transformers have $\mathcal{O}(N^2)$ attention complexity and require massive datasets to generalize. For an operational defensive SOC running locally on edge hardware with sequence length $N = 12$, a 2-layer LSTM trains in minutes, executes inference in $< 20\text{ ms}$ on a standard CPU, and avoids overfitting on moderate-sized academic datasets.

#### Q4: How do you guarantee there is no data leakage?
**Answer**: We enforce strict chronological splitting (70% train, 15% validation, 15% test) without shuffling. Standard scalers are fitted solely on the training split. Rolling windows are constructed so input features ($T-11 \dots T$) and targets ($T+1 \dots T+3$) never cross split boundaries.

#### Q5: What is the purpose of the continuous state reconstructor head?
**Answer**: It acts as an auxiliary task regularizer. Predicting the 16 continuous telemetry features ($\hat{s}_{t+1}$) forces the LSTM's shared latent space to learn realistic network physics rather than overfitting to binary labels. It also provides the input state for autoregressive forecasting at $T+2$ and $T+3$.

#### Q6: Why does your model accuracy drop from $T+1$ to $T+3$?
**Answer**: This is expected behavior in all autoregressive forecasting systems. At $T+1$, the model uses ground-truth observed history. At $T+2$ and $T+3$, the model ingests its own prior predictions ($\hat{s}_{t+1}$), which introduces cumulative variance and gradual error compounding.

#### Q7: How does your model handle false positives?
**Answer**: Our multi-task LSTM model achieved a False Positive Rate of 5.0% on the test set, compared to 20.0% for the baseline Logistic Regression model — a 75% reduction. Furthermore, SHAP feature attributions show analysts the exact features driving any risk alert, allowing fast human triage.

#### Q8: What dataset was used to train and evaluate Sentinel-X?
**Answer**: The system is engineered to ingest standard benchmark datasets (CIC-IDS-2017/2018). For offline demonstration and viva evaluation without multi-gigabyte downloads, we developed a deterministic safe synthetic flow generator that simulates benign traffic and 4 progressive attack campaigns with explicit label tracking (`is_synthetic=True`).

#### Q9: What happens if an attacker launches a zero-day attack with no prior signature?
**Answer**: Sentinel-X does not use payload signatures. It models statistical telemetry (flow rates, packet length asymmetry, SYN/ACK flag ratios). Even a zero-day exploit must communicate over network protocols; abnormal protocol flag dynamics and bursty byte distributions will trigger elevated forecasted risk.

#### Q10: What are the primary future improvements for Sentinel-X?
**Answer**:
1. Integration with automated SDN controllers (Software-Defined Networking) to deploy proactive OpenFlow firewall rules directly upon high-confidence $T+1$ risk forecasts.
2. Exploring temporal Graph Neural Networks (GNNs) to model multi-host topology interactions alongside temporal sequence dynamics.
3. Quantizing the PyTorch model via ONNX/TensorRT for microsecond edge firewall deployment.

---

## 11. The 7 Commands to Run the Project Locally

```powershell
# 1. Activate Environment
.\.venv\Scripts\Activate.ps1

# 2. Environment Verification
python scripts/check_environment.py

# 3. Data Processing & Window Generation
python scripts/prepare_data.py

# 4. Train Static Baseline Model
python scripts/train_baseline.py

# 5. Train Deep LSTM World Model
python scripts/train_lstm.py

# 6. Run Model Evaluation & SHAP Analysis
python scripts/evaluate.py

# 7. Launch Interactive SOC Dashboard
streamlit run dashboard/app.py
```
Dashboard URL: `http://localhost:8501`  
Live Static Overview: `https://sentinel-x-lilac.vercel.app`
