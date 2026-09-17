"""Generate the official Sentinel-X academic B.Tech presentation.

Matches the Buddha Institute of Technology (BIT) & AKTU slide template, styling,
and required presentation structure.
"""

from pathlib import Path
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ASSETS_DIR = PROJECT_ROOT / "docs" / "presentation_assets"
OUTPUT_PPTX = PROJECT_ROOT / "Sentinel-X_Presentation.pptx"

# Color Palette matching Buddha Institute of Technology Presentation Template
COLOR_PRIMARY_BLUE = RGBColor(30, 58, 138)     # Deep Navy Blue (#1E3A8A)
COLOR_ACCENT_BLUE = RGBColor(37, 99, 235)      # Royal Blue (#2563EB)
COLOR_DARK_TEXT = RGBColor(15, 23, 42)         # Slate 900 (#0F172A)
COLOR_BODY_TEXT = RGBColor(30, 41, 59)         # Slate 800 (#1E293B)
COLOR_MUTED_TEXT = RGBColor(100, 116, 139)     # Slate 500 (#64748B)
COLOR_CARD_BG = RGBColor(255, 248, 231)        # Slightly lighter warm cream (#FFF8E7)
COLOR_CARD_BORDER = RGBColor(217, 119, 6)      # Amber/Gold border (#D97706)
COLOR_GREEN = RGBColor(22, 101, 52)            # Forest Green (#166534)
COLOR_RED = RGBColor(153, 27, 27)              # Dark Crimson Red (#991B1B)


def create_presentation():
    prs = pptx.Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    title_bg_path = str(ASSETS_DIR / "title_slide_bg.png")
    master_bg_path = str(ASSETS_DIR / "master_slide_bg.png")
    thankyou_bg_path = str(ASSETS_DIR / "page_4.png")

    def add_slide_header(slide, title_text):
        """Add master slide background and standardized centered title header."""
        slide.shapes.add_picture(master_bg_path, 0, 0, width=prs.slide_width, height=prs.slide_height)
        
        # Header text box
        title_box = slide.shapes.add_textbox(Inches(2.5), Inches(0.85), Inches(8.333), Inches(0.85))
        tf = title_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.name = "Georgia"
        p.font.size = Pt(26)
        p.font.bold = True
        p.font.color.rgb = COLOR_PRIMARY_BLUE
        p.alignment = PP_ALIGN.CENTER

        # Underline bar under the title
        line = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE,
            Inches(4.5), Inches(1.58), Inches(4.333), Inches(0.04)
        )
        line.fill.solid()
        line.fill.fore_color.rgb = COLOR_ACCENT_BLUE
        line.line.color.rgb = COLOR_ACCENT_BLUE

    # =========================================================================
    # SLIDE 1: TITLE SLIDE
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_layout)
    slide1.shapes.add_picture(title_bg_path, 0, 0, width=prs.slide_width, height=prs.slide_height)

    tbox = slide1.shapes.add_textbox(Inches(2.2), Inches(1.15), Inches(8.933), Inches(5.8))
    tf = tbox.text_frame
    tf.word_wrap = True

    # "A Project Presentation on"
    p0 = tf.paragraphs[0]
    p0.text = "A Project Presentation\non"
    p0.font.name = "Georgia"
    p0.font.size = Pt(20)
    p0.font.italic = True
    p0.font.color.rgb = COLOR_DARK_TEXT
    p0.alignment = PP_ALIGN.CENTER

    # Project Title
    p1 = tf.add_paragraph()
    p1.text = "Sentinel-X: AI-Based Network Attack Forecasting\nfrom Network Traffic Data"
    p1.font.name = "Georgia"
    p1.font.size = Pt(25)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_PRIMARY_BLUE
    p1.alignment = PP_ALIGN.CENTER
    p1.space_before = Pt(8)
    p1.space_after = Pt(14)

    # Team Members Block
    p2 = tf.add_paragraph()
    p2.text = "Presentation by :"
    p2.font.name = "Arial"
    p2.font.size = Pt(15)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_DARK_TEXT
    p2.alignment = PP_ALIGN.CENTER
    p2.space_after = Pt(4)

    members = [
        "Shristi Jaiswal  —  Roll No. 2405250100153",
        "Suraj Prakash Chaudhary  —  Roll No. 2405250100156",
        "Suraj Upadhyay  —  Roll No. 2405250100158",
        "Udai Kumar Srivastava  —  Roll No. 2405250100160",
    ]
    for m in members:
        pm = tf.add_paragraph()
        pm.text = m
        pm.font.name = "Arial"
        pm.font.size = Pt(13.5)
        pm.font.bold = True
        pm.font.color.rgb = COLOR_BODY_TEXT
        pm.alignment = PP_ALIGN.CENTER

    # Guide Block
    p3 = tf.add_paragraph()
    p3.text = "Under the guidance of :"
    p3.font.name = "Arial"
    p3.font.size = Pt(14)
    p3.font.bold = True
    p3.font.color.rgb = COLOR_DARK_TEXT
    p3.alignment = PP_ALIGN.CENTER
    p3.space_before = Pt(10)

    p4 = tf.add_paragraph()
    p4.text = "Mr. Akash Gupta\n(Assistant Professor)"
    p4.font.name = "Arial"
    p4.font.size = Pt(14)
    p4.font.bold = True
    p4.font.color.rgb = COLOR_PRIMARY_BLUE
    p4.alignment = PP_ALIGN.CENTER

    # Institution Block
    p5 = tf.add_paragraph()
    p5.text = "Department of Computer Science and Engineering\nBuddha Institute of Technology, GIDA, Gorakhpur\nSession 2026-27"
    p5.font.name = "Georgia"
    p5.font.size = Pt(13.5)
    p5.font.bold = True
    p5.font.color.rgb = COLOR_RED
    p5.alignment = PP_ALIGN.CENTER
    p5.space_before = Pt(10)

    # =========================================================================
    # SLIDE 2: CONTENT (AGENDA - Matching PDF Page 2)
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    add_slide_header(slide2, "CONTENT")

    cbox = slide2.shapes.add_textbox(Inches(1.8), Inches(2.0), Inches(9.8), Inches(4.8))
    ctf = cbox.text_frame
    ctf.word_wrap = True

    agenda_items = [
        ("Brief Introduction", "SIH26153 Problem Statement & Shift to Predictive Forecasting"),
        ("Literature Review", "Existing NIDS, Gaps in Retrospective Systems & Research Contribution"),
        ("Objective of the Project", "Core Technical & Defensive Cybersecurity Goals"),
        ("Feasibility Study", "Technical, Operational & Economic/Resource Viability"),
        ("Proposed Work", "End-to-End Pipeline & 16-Dimensional Network State Representation"),
        ("Methodology / Technology Used", "Recurrent LSTM World Model, Autoregressive Rollout & SHAP XAI"),
        ("Social & Environmental Relevance", "National Critical Infrastructure Defense & Low-Power AI"),
        ("Conclusion & Future Scope", "Performance Takeaways, Automated SDN Firewalls & ONNX"),
        ("References", "Standard Benchmarks, MITRE ATT&CK & Deep Learning Citations"),
    ]

    for i, (item, sub) in enumerate(agenda_items):
        p = ctf.paragraphs[0] if i == 0 else ctf.add_paragraph()
        p.text = f"❖  {item}  —  "
        p.font.name = "Arial"
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = COLOR_PRIMARY_BLUE
        p.space_after = Pt(5)

        run = p.add_run()
        run.text = sub
        run.font.name = "Arial"
        run.font.size = Pt(13)
        run.font.bold = False
        run.font.color.rgb = COLOR_MUTED_TEXT

    # =========================================================================
    # SLIDE 3: BRIEF INTRODUCTION
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    add_slide_header(slide3, "Brief Introduction")

    # Left Column: Problem & Motivation
    col1 = slide3.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.6), Inches(4.8))
    tf1 = col1.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "The Reactive Cybersecurity Dilemma"
    p.font.name = "Georgia"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = COLOR_RED

    points1 = [
        "Traditional Intrusion Detection Systems (NIDS/SIEM) are retrospective: they alert ONLY after an exploit payload detonates or breach succeeds.",
        "Mean Time to Remediate (MTTR) is dangerously high because security teams react after lateral movement has already begun.",
        "Alert Fatigue: SOC analysts are overwhelmed by thousands of isolated binary alerts with zero predictive trajectory.",
    ]
    for pt in points1:
        p = tf1.add_paragraph()
        p.text = f"• {pt}"
        p.font.size = Pt(13.5)
        p.font.color.rgb = COLOR_BODY_TEXT
        p.space_before = Pt(6)

    # Right Column: The Sentinel-X Solution
    col2 = slide3.shapes.add_textbox(Inches(6.9), Inches(2.0), Inches(5.6), Inches(4.8))
    tf2 = col2.text_frame
    tf2.word_wrap = True

    p = tf2.paragraphs[0]
    p.text = "The Sentinel-X Paradigm Shift"
    p.font.name = "Georgia"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY_BLUE

    points2 = [
        "SIH26153 Mandate: Predict network attack risk 10 to 30 seconds BEFORE intrusions escalate.",
        "Ingests continuous 120-second rolling telemetry (T-11 ... T) and forecasts risk at T+1, T+2, and T+3.",
        "Predicts 3 outputs concurrently: Future Attack Risk, Behavioral MITRE ATT&CK Stage, and Continuous Network-State.",
        "100% Defensive & Academic: Works offline with benchmark data, zero offensive tools, and zero cloud API dependencies.",
    ]
    for pt in points2:
        p = tf2.add_paragraph()
        p.text = f"• {pt}"
        p.font.size = Pt(13.5)
        p.font.color.rgb = COLOR_BODY_TEXT
        p.space_before = Pt(6)

    # =========================================================================
    # SLIDE 4: LITERATURE REVIEW
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    add_slide_header(slide4, "Literature Review")

    lbox = slide4.shapes.add_textbox(Inches(1.0), Inches(1.9), Inches(11.3), Inches(5.0))
    ltf = lbox.text_frame
    ltf.word_wrap = True

    reviews = [
        ("Signature-Based Systems (Snort, Suricata, Bro/Zeek)",
         "High accuracy for known signatures; completely blind to zero-day variants and multi-phase progression. Alert is fired only post-compromise."),
        ("Traditional Machine Learning Classifiers (Random Forest, SVM, XGBoost)",
         "Treats individual flow records as isolated, independent vectors. Incapable of modeling continuous temporal sequences or performing multi-step state rollouts."),
        ("Recurrent Deep Learning Models (Standard RNN, Vanilla LSTM, GRU)",
         "Captures temporal dependencies but models intrusions as static single-step binary classification (Malicious vs Benign) at current time T."),
        ("The Identified Research Gap & Sentinel-X Contribution",
         "Lack of autoregressive World Models that predict future continuous telemetry states (s_t+1) to forecast multi-step risk horizons (T+1..T+3) with Explainable AI."),
    ]

    for i, (title, desc) in enumerate(reviews):
        p = ltf.paragraphs[0] if i == 0 else ltf.add_paragraph()
        p.text = f"{i+1}. {title}"
        p.font.name = "Georgia"
        p.font.size = Pt(15.5)
        p.font.bold = True
        p.font.color.rgb = COLOR_PRIMARY_BLUE if i < 3 else COLOR_GREEN
        p.space_before = Pt(6) if i > 0 else Pt(0)

        pr = ltf.add_paragraph()
        pr.text = f"    {desc}"
        pr.font.size = Pt(13)
        pr.font.color.rgb = COLOR_BODY_TEXT
        pr.space_before = Pt(2)

    # =========================================================================
    # SLIDE 5: OBJECTIVE OF THE PROJECT
    # =========================================================================
    slide5 = prs.slides.add_slide(blank_layout)
    add_slide_header(slide5, "Objective of the Project")

    obox = slide5.shapes.add_textbox(Inches(1.0), Inches(1.9), Inches(11.3), Inches(5.0))
    otf = obox.text_frame
    otf.word_wrap = True

    objs = [
        ("Primary Objective",
         "To engineer and implement Sentinel-X, a defensive machine learning system capable of forecasting multi-step network attack risk from sequential traffic telemetry prior to attack escalation (SIH26153)."),
        ("Continuous Network-State Telemetry Formulation",
         "Aggregate raw network flows into 10-second non-overlapping windows containing 16 key statistical features representing flow rates, packet length asymmetry, and protocol flag ratios."),
        ("Deep Recurrent World Model Architecture",
         "Design a 2-layer LSTM recurrent World Model with three specialized multi-task heads: Risk Head (BCE Loss), Stage Head (Cross-Entropy), and State Reconstructor Head (MSE Loss)."),
        ("Autoregressive Multi-Step Rollout",
         "Iteratively feed the model's predicted continuous state (s_t+1) back into the recurrent loop to project threat trajectories across T+1 (10s), T+2 (20s), and T+3 (30s)."),
        ("Explainable AI & Defensive SOC Dashboard",
         "Integrate SHAP (SHapley Additive exPlanations) to attribute risk drivers and inhibitors, presented via a real-time Streamlit SOC command center for intuitive human-in-the-loop triage."),
    ]

    for i, (h, desc) in enumerate(objs):
        p = otf.paragraphs[0] if i == 0 else otf.add_paragraph()
        p.text = f"❖  {h}: "
        p.font.name = "Georgia"
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = COLOR_PRIMARY_BLUE
        p.space_before = Pt(6) if i > 0 else Pt(0)

        run = p.add_run()
        run.text = desc
        run.font.name = "Arial"
        run.font.size = Pt(13)
        run.font.bold = False
        run.font.color.rgb = COLOR_BODY_TEXT

    # =========================================================================
    # SLIDE 6: FEASIBILITY STUDY
    # =========================================================================
    slide6 = prs.slides.add_slide(blank_layout)
    add_slide_header(slide6, "Feasibility Study")

    # 3 Cards: Technical, Operational, Economic
    cards = [
        ("Technical Feasibility", [
            "Built with open-source PyTorch, scikit-learn, and Streamlit.",
            "2-Layer LSTM with 128 hidden units trains in < 2 minutes on CPU.",
            "Inference latency is under 20 milliseconds per sequence window, well within the 10-second operational telemetry window.",
            "Cross-platform compatibility: Windows 10/11, Ubuntu Linux, and macOS.",
        ], Inches(1.0), COLOR_PRIMARY_BLUE),
        ("Operational Feasibility", [
            "Provides proactive 10 to 30 second lead time for automated mitigation.",
            "Reduces false alarms by 75% compared to static baseline models, directly combating SOC analyst alert fatigue.",
            "Explainable AI (SHAP) provides transparent feature drivers, enabling fast human verification and triage.",
            "Clear visual dashboard requires minimal specialized training.",
        ], Inches(5.0), COLOR_GREEN),
        ("Economic & Ethical", [
            "Zero cost: requires no commercial APIs, cloud credits, or paid licenses.",
            "Self-contained: runs offline on standard academic/laboratory laptops.",
            "Strict defensive posture: contains no exploit code, payload generators, or offensive scanning tools.",
            "Complies with Indian academic evaluation and IEEE research guidelines.",
        ], Inches(9.0), COLOR_RED),
    ]

    for title, points, x_pos, header_color in cards:
        # Background card shape
        rect = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x_pos, Inches(1.9), Inches(3.4), Inches(5.0))
        rect.fill.solid()
        rect.fill.fore_color.rgb = COLOR_CARD_BG
        rect.line.color.rgb = header_color
        rect.line.width = Pt(2)

        # Text inside card
        cbox = slide6.shapes.add_textbox(x_pos + Inches(0.15), Inches(2.0), Inches(3.1), Inches(4.8))
        ctf = cbox.text_frame
        ctf.word_wrap = True

        p = ctf.paragraphs[0]
        p.text = title
        p.font.name = "Georgia"
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = header_color
        p.alignment = PP_ALIGN.CENTER
        p.space_after = Pt(10)

        for pt in points:
            p = ctf.add_paragraph()
            p.text = f"• {pt}"
            p.font.size = Pt(12)
            p.font.color.rgb = COLOR_BODY_TEXT
            p.space_before = Pt(6)

    # =========================================================================
    # SLIDE 7: PROPOSED WORK - SYSTEM PIPELINE
    # =========================================================================
    slide7 = prs.slides.add_slide(blank_layout)
    add_slide_header(slide7, "Proposed Work: End-to-End Pipeline")

    pbox = slide7.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.3), Inches(1.1))
    ptf = pbox.text_frame
    ptf.word_wrap = True
    p = ptf.paragraphs[0]
    p.text = "Sentinel-X Architecture Workflow"
    p.font.name = "Georgia"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY_BLUE
    
    p2 = ptf.add_paragraph()
    p2.text = "From continuous network packet flows to real-time autoregressive forecasting and SOC visualization:"
    p2.font.size = Pt(13)
    p2.font.color.rgb = COLOR_BODY_TEXT

    # Embed Pipeline Diagram
    pipe_img = str(ASSETS_DIR / "chart_pipeline.png")
    slide7.shapes.add_picture(pipe_img, Inches(1.2), Inches(2.9), width=Inches(10.9))

    # =========================================================================
    # SLIDE 8: PROPOSED WORK - 16 FEATURES
    # =========================================================================
    slide8 = prs.slides.add_slide(blank_layout)
    add_slide_header(slide8, "Proposed Work: 16-D Network State")

    fbox = slide8.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.3), Inches(1.0))
    ftf = fbox.text_frame
    ftf.word_wrap = True
    p = ftf.paragraphs[0]
    p.text = "10-Second Flow Aggregation into 16 Continuous State Features"
    p.font.name = "Georgia"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY_BLUE
    p_sub = ftf.add_paragraph()
    p_sub.text = "Packet-by-packet inspection fails on gigabit links; statistical flow windowing captures genuine attack kinetics:"
    p_sub.font.size = Pt(13)
    p_sub.font.color.rgb = COLOR_BODY_TEXT

    # Embed 16 Features Diagram
    feat_img = str(ASSETS_DIR / "chart_features.png")
    slide8.shapes.add_picture(feat_img, Inches(1.2), Inches(2.8), width=Inches(10.9))

    # =========================================================================
    # SLIDE 9: METHODOLOGY - LSTM WORLD MODEL
    # =========================================================================
    slide9 = prs.slides.add_slide(blank_layout)
    add_slide_header(slide9, "Methodology: Deep LSTM World Model")

    # Left: Explanation
    wbox = slide9.shapes.add_textbox(Inches(0.9), Inches(1.9), Inches(5.2), Inches(4.9))
    wtf = wbox.text_frame
    wtf.word_wrap = True

    p = wtf.paragraphs[0]
    p.text = "Why a 'World Model' Architecture?"
    p.font.name = "Georgia"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY_BLUE

    wpoints = [
        "In AI, a World Model learns how an environment evolves over time. Sentinel-X forecasts both the threat label AND the next network state (s_t+1).",
        "2-Layer LSTM Backbone: Ingests 12-step sequence (T-11 ... T = 120s). Hidden dimension: 128, Dropout: 0.3.",
        "Head 1 (Risk): Linear(128,32) -> Sigmoid -> BCE Loss. Predicts continuous probability of intrusion [0, 1].",
        "Head 2 (Stage): Linear(128,64) -> Softmax -> Cross-Entropy. Classifies 5 MITRE ATT&CK stages.",
        "Head 3 (State): Linear(128,64) -> Linear(64,16) -> MSE. Reconstructs next 16-D continuous state vector.",
    ]
    for pt in wpoints:
        p = wtf.add_paragraph()
        p.text = f"• {pt}"
        p.font.size = Pt(12.5)
        p.font.color.rgb = COLOR_BODY_TEXT
        p.space_before = Pt(4)

    # Right: Diagram
    wm_img = str(ASSETS_DIR / "chart_world_model.png")
    slide9.shapes.add_picture(wm_img, Inches(6.2), Inches(2.0), width=Inches(6.4))

    # =========================================================================
    # SLIDE 10: METHODOLOGY - ROLLOUT & MULTI-TASK LOSS
    # =========================================================================
    slide10 = prs.slides.add_slide(blank_layout)
    add_slide_header(slide10, "Methodology: Rollout & Multi-Task Loss")

    rbox = slide10.shapes.add_textbox(Inches(1.0), Inches(1.9), Inches(11.3), Inches(5.0))
    rtf = rbox.text_frame
    rtf.word_wrap = True

    p = rtf.paragraphs[0]
    p.text = "1. Closed-Loop Autoregressive Rollout Engine"
    p.font.name = "Georgia"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY_BLUE

    rpoints = [
        "Step 1 (T+1): Ingests history [s_T-11 ... s_T] -> outputs predicted state s_T+1, risk r_T+1, and stage c_T+1.",
        "Step 2 (T+2): Feeds predicted state s_T+1 back into recurrent cell with updated hidden state (h_1, c_1) -> outputs s_T+2, r_T+2, c_T+2.",
        "Step 3 (T+3): Feeds predicted state s_T+2 into recurrent cell with (h_2, c_2) -> outputs s_T+3, r_T+3, c_T+3.",
        "Eliminates dependency on ground truth future data during live operation.",
    ]
    for pt in rpoints:
        p = rtf.add_paragraph()
        p.text = f"    • {pt}"
        p.font.size = Pt(13)
        p.font.color.rgb = COLOR_BODY_TEXT
        p.space_before = Pt(2)

    p2 = rtf.add_paragraph()
    p2.text = "2. Joint Weighted Multi-Task Loss Formulation"
    p2.font.name = "Georgia"
    p2.font.size = Pt(16)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_RED
    p2.space_before = Pt(10)

    p_eq = rtf.add_paragraph()
    p_eq.text = "    L_total = 1.0 * L_BCE(r_pred, r_true) + 1.0 * L_CE(c_pred, c_true) + 0.2 * L_MSE(s_pred, s_true)"
    p_eq.font.name = "Courier New"
    p_eq.font.size = Pt(13.5)
    p_eq.font.bold = True
    p_eq.font.color.rgb = COLOR_PRIMARY_BLUE
    p_eq.space_before = Pt(3)

    p_aux = rtf.add_paragraph()
    p_aux.text = "    • Auxiliary Task Regularization: Supervising the State Head on physical telemetry dynamics forces the shared LSTM latent space to understand real network behavior, drastically mitigating overfitting on attack labels."
    p_aux.font.size = Pt(13)
    p_aux.font.color.rgb = COLOR_BODY_TEXT
    p_aux.space_before = Pt(3)

    # =========================================================================
    # SLIDE 11: METHODOLOGY - SHAP EXPLAINABILITY
    # =========================================================================
    slide11 = prs.slides.add_slide(blank_layout)
    add_slide_header(slide11, "Methodology: Explainable AI (SHAP)")

    sbox = slide11.shapes.add_textbox(Inches(1.0), Inches(1.9), Inches(11.3), Inches(5.0))
    stf = sbox.text_frame
    stf.word_wrap = True

    shap_points = [
        ("Why XAI is Mandatory for Defensive SOCs",
         "A black-box prediction cannot be trusted for automated containment. Analysts need to know 'WHY' the neural network forecasts risk escalation to execute targeted firewall rules."),
        ("SHAP KernelExplainer Formulation",
         "Derived from cooperative game theory (Shapley Additive exPlanations). Computes the marginal contribution of each network feature by comparing against a background distribution of benign flows."),
        ("Signed Feature Attributions (Risk Drivers vs. Inhibitors)",
         "Risk Drivers (Positive SHAP): Features driving risk upward (e.g. syn_ratio +0.35, packet_rate +0.25).\nRisk Inhibitors (Negative SHAP): Features pulling risk downward (e.g. ack_ratio -0.13, duration_mean -0.08)."),
        ("Temporal Sequence Saliency",
         "Measures which specific historical time steps (T-11 ... T) exerted the strongest influence on the recurrent hidden state, identifying whether threats developed rapidly or gradually."),
        ("Deterministic Gradient Fallback",
         "If background matrix sampling encounters degenerate covariance matrices, Sentinel-X seamlessly falls back to gradient-based input saliency (grad_x * x) to ensure zero dashboard interruption."),
    ]

    for i, (title, desc) in enumerate(shap_points):
        p = stf.paragraphs[0] if i == 0 else stf.add_paragraph()
        p.text = f"❖  {title}"
        p.font.name = "Georgia"
        p.font.size = Pt(14.5)
        p.font.bold = True
        p.font.color.rgb = COLOR_PRIMARY_BLUE
        p.space_before = Pt(4) if i > 0 else Pt(0)

        pr = stf.add_paragraph()
        pr.text = f"    {desc}"
        pr.font.size = Pt(12.5)
        pr.font.color.rgb = COLOR_BODY_TEXT
        pr.space_before = Pt(1)

    # =========================================================================
    # SLIDE 12: METHODOLOGY - MITRE ATT&CK TAXONOMY
    # =========================================================================
    slide12 = prs.slides.add_slide(blank_layout)
    add_slide_header(slide12, "Methodology: MITRE ATT&CK Mapping")

    mbox = slide12.shapes.add_textbox(Inches(1.0), Inches(1.9), Inches(11.3), Inches(5.0))
    mtf = mbox.text_frame
    mtf.word_wrap = True

    p = mtf.paragraphs[0]
    p.text = "Conservative Behavioral Attack Stage Classification"
    p.font.name = "Georgia"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY_BLUE

    p_sub = mtf.add_paragraph()
    p_sub.text = "Sentinel-X maps telemetry patterns to 5 MITRE ATT&CK behavioral stages without claiming unsupported forensic certainty:"
    p_sub.font.size = Pt(13)
    p_sub.font.color.rgb = COLOR_BODY_TEXT
    p_sub.space_after = Pt(6)

    stages = [
        ("Stage 0: Benign Baseline", "BENIGN", "Normal operational traffic (expected HTTP/HTTPS, DNS, streaming). High ACK ratio (> 0.85), low SYN ratio, steady flow durations."),
        ("Stage 1: Reconnaissance", "TA0043", "Active host & port scanning. Elevated SYN ratios (> 0.5), high flow counts, short durations, minimal backward payload bytes."),
        ("Stage 2: Initial Access", "TA0001", "Perimeter breach & authentication brute force (FTP/SSH/Patator). Elevated byte rates, repeated connection spikes to auth services."),
        ("Stage 3: Lateral Movement", "TA0008", "Internal subnet traversal. Bursty flow intervals across SMB (445), RDP (3389), and WinRM (5985) management ports."),
        ("Stage 4: Command & Control", "TA0011", "Outbound beaconing & management channels. Periodic flow inter-arrival intervals (low variance) and consistent heartbeat payloads."),
    ]

    for s_name, tactic, desc in stages:
        p = mtf.add_paragraph()
        p.text = f"• {s_name} [{tactic}]: "
        p.font.name = "Arial"
        p.font.size = Pt(13.5)
        p.font.bold = True
        p.font.color.rgb = COLOR_RED if tactic != "BENIGN" else COLOR_GREEN

        run = p.add_run()
        run.text = desc
        run.font.name = "Arial"
        run.font.size = Pt(12.5)
        run.font.bold = False
        run.font.color.rgb = COLOR_BODY_TEXT
        p.space_before = Pt(3)

    # =========================================================================
    # SLIDE 13: EXPERIMENTAL RESULTS & BENCHMARKS
    # =========================================================================
    slide13 = prs.slides.add_slide(blank_layout)
    add_slide_header(slide13, "Experimental Results & Benchmarks")

    # Left: Benchmark Metrics Table
    tbl_shape = slide13.shapes.add_table(7, 4, Inches(0.9), Inches(1.9), Inches(5.8), Inches(4.8))
    tbl = tbl_shape.table

    headers = ["Metric", "Baseline", "LSTM (T+1)", "LSTM (T+3)"]
    for col_idx, h in enumerate(headers):
        cell = tbl.cell(0, col_idx)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_PRIMARY_BLUE
        p = cell.text_frame.paragraphs[0]
        p.font.bold = True
        p.font.size = Pt(12)
        p.font.color.rgb = RGBColor(255, 255, 255)
        p.alignment = PP_ALIGN.CENTER

    data_rows = [
        ("Risk Recall", "97.8%", "100.0%", "100.0%"),
        ("Risk Precision", "98.9%", "96.7%", "94.6%"),
        ("Risk F1-Score", "0.9831", "0.9834", "0.9721"),
        ("False Positive Rate", "20.0%", "5.0%", "10.0%"),
        ("Stage Accuracy", "N/A", "62.8%", "60.6%"),
        ("State MAE", "N/A", "0.8538", "0.8820"),
    ]

    for row_idx, r in enumerate(data_rows):
        for col_idx, val in enumerate(r):
            cell = tbl.cell(row_idx + 1, col_idx)
            cell.text = val
            cell.fill.solid()
            cell.fill.fore_color.rgb = COLOR_CARD_BG if row_idx % 2 == 0 else RGBColor(255, 255, 255)
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(11.5)
            p.font.bold = (col_idx == 0 or (col_idx == 2 and row_idx in [0, 3]))
            p.font.color.rgb = COLOR_DARK_TEXT
            p.alignment = PP_ALIGN.LEFT if col_idx == 0 else PP_ALIGN.CENTER

    # Right: Chart
    chart_img = str(ASSETS_DIR / "chart_performance.png")
    slide13.shapes.add_picture(chart_img, Inches(6.9), Inches(2.1), width=Inches(5.7))

    # =========================================================================
    # SLIDE 14: INTERACTIVE SOC DASHBOARD
    # =========================================================================
    slide14 = prs.slides.add_slide(blank_layout)
    add_slide_header(slide14, "Interactive SOC Dashboard")

    # Left: Explanation of 5 views
    dbox = slide14.shapes.add_textbox(Inches(0.9), Inches(1.9), Inches(4.8), Inches(4.9))
    dtf = dbox.text_frame
    dtf.word_wrap = True

    p = dtf.paragraphs[0]
    p.text = "Real-Time Defensive Command Center"
    p.font.name = "Georgia"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY_BLUE

    dviews = [
        "View 1 — Executive Risk: Real-time risk probability gauge, multi-step risk delta (T+3 - T), and MITRE stage card with confidence score.",
        "View 2 — Forecast Timeline: Verified historical risk trail (T-11..T) contrasted against future autoregressive forecast (T+1..T+3) with 95% CI band.",
        "View 3 — Threat Attribution: Signed horizontal SHAP bar chart (red risk drivers vs green inhibitors) & temporal sequence importance.",
        "View 4 — Model Performance: Full comparative evaluation table & degradation curves across multi-step horizons.",
        "View 5 — System Status: Hardware diagnostics (CPU/GPU), Python/PyTorch versions, and checkpoint verification.",
    ]
    for dv in dviews:
        p = dtf.add_paragraph()
        p.text = f"• {dv}"
        p.font.size = Pt(11.5)
        p.font.color.rgb = COLOR_BODY_TEXT
        p.space_before = Pt(3)

    # Right: Screenshot
    ss_img = str(ASSETS_DIR / "dashboard_screenshot.png")
    slide14.shapes.add_picture(ss_img, Inches(5.9), Inches(2.0), width=Inches(6.6))

    # =========================================================================
    # SLIDE 15: SOCIAL & ENVIRONMENTAL RELEVANCE
    # =========================================================================
    slide15 = prs.slides.add_slide(blank_layout)
    add_slide_header(slide15, "Social & Environmental Relevance")

    sbox2 = slide15.shapes.add_textbox(Inches(1.0), Inches(1.9), Inches(11.3), Inches(5.0))
    stf2 = sbox2.text_frame
    stf2.word_wrap = True

    impacts = [
        ("1. National Critical Infrastructure Defense (Social & Strategic Impact)",
         "Cyber attacks targeting power grids, healthcare systems, defense networks, and banking portals cause devastating collateral damage. Sentinel-X's proactive 10-30 second forecasting lead time empowers defensive infrastructure to deploy automated rate limiters and isolation policies before services suffer catastrophic disruption."),
        ("2. Human-Centric SOC Workload & Burnout Mitigation (Human Impact)",
         "Cybersecurity professionals suffer extreme cognitive fatigue from sorting through tens of thousands of daily false positives. By reducing the false alarm rate from 20% to 5% (a 75% reduction) and delivering transparent SHAP attributions, Sentinel-X restores analyst focus to genuine high-priority incidents."),
        ("3. Lightweight 'Green AI' on Consumer Hardware (Environmental Impact)",
         "Unlike cloud-heavy generative models that burn megawatts in remote server farms, Sentinel-X is designed as an edge-capable Green AI system. The entire 2-layer recurrent architecture executes inference in < 20 ms on a standard laptop CPU, consuming negligible electrical power with zero cloud carbon footprint."),
    ]

    for title, desc in impacts:
        p = stf2.paragraphs[0] if title == impacts[0][0] else stf2.add_paragraph()
        p.text = title
        p.font.name = "Georgia"
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = COLOR_PRIMARY_BLUE
        p.space_before = Pt(8) if title != impacts[0][0] else Pt(0)

        pr = stf2.add_paragraph()
        pr.text = f"    {desc}"
        pr.font.size = Pt(13)
        pr.font.color.rgb = COLOR_BODY_TEXT
        pr.space_before = Pt(2)

    # =========================================================================
    # SLIDE 16: CONCLUSION & FUTURE SCOPE
    # =========================================================================
    slide16 = prs.slides.add_slide(blank_layout)
    add_slide_header(slide16, "Conclusion & Future Scope")

    # Left: Conclusion
    cbox_l = slide16.shapes.add_textbox(Inches(1.0), Inches(1.9), Inches(5.5), Inches(4.9))
    ctf_l = cbox_l.text_frame
    ctf_l.word_wrap = True

    p = ctf_l.paragraphs[0]
    p.text = "Key Project Achievements"
    p.font.name = "Georgia"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = COLOR_GREEN

    conclusions = [
        "Successfully solved SIH26153 by transitioning network security from reactive post-incident detection to proactive multi-step forecasting.",
        "Demonstrated 100% attack recall on T+1 and a 75% reduction in false alarms over the static baseline benchmark.",
        "Engineered an autoregressive World Model with multi-task loss that simulates continuous network dynamics.",
        "Delivered full explainability via SHAP and an operational 5-view SOC dashboard running locally offline.",
    ]
    for c in conclusions:
        p = ctf_l.add_paragraph()
        p.text = f"• {c}"
        p.font.size = Pt(13)
        p.font.color.rgb = COLOR_BODY_TEXT
        p.space_before = Pt(6)

    # Right: Future Scope
    cbox_r = slide16.shapes.add_textbox(Inches(6.8), Inches(1.9), Inches(5.5), Inches(4.9))
    ctf_r = cbox_r.text_frame
    ctf_r.word_wrap = True

    p = ctf_r.paragraphs[0]
    p.text = "Future Research & Enhancements"
    p.font.name = "Georgia"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY_BLUE

    futures = [
        "Automated SDN Integration: Connecting high-confidence T+1 forecasts directly to Software-Defined Networking (SDN) OpenFlow controllers to enforce instant dynamic firewall rules.",
        "Temporal Graph Neural Networks (GNNs): Modeling multi-host IP interaction topology alongside time-series sequence kinetics.",
        "Model Quantization (ONNX / TensorRT): Compressing the PyTorch LSTM for microsecond deployment directly inside edge enterprise routers.",
    ]
    for f in futures:
        p = ctf_r.add_paragraph()
        p.text = f"• {f}"
        p.font.size = Pt(13)
        p.font.color.rgb = COLOR_BODY_TEXT
        p.space_before = Pt(6)

    # =========================================================================
    # SLIDE 17: REFERENCES
    # =========================================================================
    slide17 = prs.slides.add_slide(blank_layout)
    add_slide_header(slide17, "References")

    rbox_ref = slide17.shapes.add_textbox(Inches(1.0), Inches(1.9), Inches(11.3), Inches(5.0))
    rtf_ref = rbox_ref.text_frame
    rtf_ref.word_wrap = True

    refs = [
        "[1] I. Sharafaldin, A. H. Lashkari, and A. A. Ghorbani, 'Toward Generating a New Intrusion Detection Dataset and Intrusion Traffic Characterization', Proceedings of the 4th International Conference on Information Systems Security and Privacy (ICISSP), pp. 108-116, 2018. (CIC-IDS Dataset)",
        "[2] S. M. Lundberg and S.-I. Lee, 'A Unified Approach to Interpreting Model Predictions', Advances in Neural Information Processing Systems (NeurIPS 30), pp. 4765-4774, 2017. (SHAP Framework)",
        "[3] S. Hochreiter and J. Schmidhuber, 'Long Short-Term Memory', Neural Computation, vol. 9, no. 8, pp. 1735-1780, 1997.",
        "[4] MITRE Corporation, 'MITRE ATT&CK Enterprise Matrix for Cybersecurity Defense', MITRE Corporation Documentation, 2024. Available: https://attack.mitre.org/",
        "[5] Smart India Hackathon (SIH), 'Problem Statement SIH26153: AI based Network Attack Forecasting from Network Traffic Data', Ministry of Education, Govt. of India, 2024.",
        "[6] F. Pedregosa et al., 'Scikit-learn: Machine Learning in Python', Journal of Machine Learning Research, vol. 12, pp. 2825-2830, 2011.",
        "[7] A. Paszke et al., 'PyTorch: An Imperative Style, High-Performance Deep Learning Library', Advances in Neural Information Processing Systems (NeurIPS 32), pp. 8024-8035, 2019.",
    ]

    for i, rf in enumerate(refs):
        p = rtf_ref.paragraphs[0] if i == 0 else rtf_ref.add_paragraph()
        p.text = rf
        p.font.name = "Arial"
        p.font.size = Pt(12)
        p.font.color.rgb = COLOR_BODY_TEXT
        p.space_before = Pt(5) if i > 0 else Pt(0)

    # =========================================================================
    # SLIDE 18: THANK YOU
    # =========================================================================
    slide18 = prs.slides.add_slide(blank_layout)
    slide18.shapes.add_picture(thankyou_bg_path, 0, 0, width=prs.slide_width, height=prs.slide_height)

    ty_box = slide18.shapes.add_textbox(Inches(2.0), Inches(4.3), Inches(9.333), Inches(2.7))
    ty_tf = ty_box.text_frame
    ty_tf.word_wrap = True

    p = ty_tf.paragraphs[0]
    p.text = "Questions & Discussion"
    p.font.name = "Georgia"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY_BLUE
    p.alignment = PP_ALIGN.CENTER

    p_team = ty_tf.add_paragraph()
    p_team.text = "Shristi Jaiswal | Suraj Prakash Chaudhary | Suraj Upadhyay | Udai Kumar Srivastava"
    p_team.font.name = "Arial"
    p_team.font.size = Pt(14)
    p_team.font.bold = True
    p_team.font.color.rgb = COLOR_DARK_TEXT
    p_team.alignment = PP_ALIGN.CENTER
    p_team.space_before = Pt(8)

    p_guide = ty_tf.add_paragraph()
    p_guide.text = "Under the guidance of: Mr. Akash Gupta (Assistant Professor)\nDepartment of Computer Science and Engineering\nBuddha Institute of Technology, GIDA, Gorakhpur"
    p_guide.font.name = "Arial"
    p_guide.font.size = Pt(13)
    p_guide.font.bold = True
    p_guide.font.color.rgb = COLOR_RED
    p_guide.alignment = PP_ALIGN.CENTER
    p_guide.space_before = Pt(6)

    p_link = ty_tf.add_paragraph()
    p_link.text = "GitHub: github.com/surajbuilds53/sentinel-x   |   Live Overview: sentinel-x-lilac.vercel.app"
    p_link.font.name = "Arial"
    p_link.font.size = Pt(12)
    p_link.font.color.rgb = COLOR_MUTED_TEXT
    p_link.alignment = PP_ALIGN.CENTER
    p_link.space_before = Pt(8)

    prs.save(str(OUTPUT_PPTX))
    print(f"Presentation generated successfully with {len(prs.slides)} slides at: {OUTPUT_PPTX}")


if __name__ == "__main__":
    create_presentation()
