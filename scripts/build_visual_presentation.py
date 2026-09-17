"""Generate the visual-first, text-light 14-slide Sentinel-X presentation.

Designed to eliminate dense text blocks and replace them with high-resolution
flowcharts, diagrams, infographics, and annotated screenshots while preserving
official Buddha Institute of Technology (BIT) & AKTU branding.
"""

from pathlib import Path
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ASSETS_DIR = PROJECT_ROOT / "docs" / "presentation_assets"
V2_DIR = ASSETS_DIR / "v2"
OUTPUT_PPTX = PROJECT_ROOT / "Sentinel-X_Presentation.pptx"

# Colors
C_NAVY = RGBColor(30, 58, 138)       # #1E3A8A
C_ROYAL = RGBColor(37, 99, 235)      # #2563EB
C_DARK = RGBColor(15, 23, 42)        # #0F172A
C_BODY = RGBColor(30, 41, 59)        # #1E293B
C_MUTED = RGBColor(100, 116, 139)    # #64748B
C_CARD_BG = RGBColor(255, 248, 231)  # Warm cream (#FFF8E7)
C_BORDER = RGBColor(217, 119, 6)     # Amber (#D97706)
C_RED = RGBColor(185, 28, 28)        # Dark Red (#B91C1C)
C_GREEN = RGBColor(21, 128, 61)      # Dark Green (#15803D)


def create_visual_presentation():
    prs = pptx.Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    title_bg = str(ASSETS_DIR / "title_slide_bg.png")
    master_bg = str(ASSETS_DIR / "master_slide_bg.png")
    thankyou_bg = str(ASSETS_DIR / "page_4.png")

    def setup_slide(slide, title_text):
        """Add master slide background, centered title, and accent underline."""
        slide.shapes.add_picture(master_bg, 0, 0, width=prs.slide_width, height=prs.slide_height)

        t_box = slide.shapes.add_textbox(Inches(2.0), Inches(0.82), Inches(9.333), Inches(0.85))
        tf = t_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.name = "Georgia"
        p.font.size = Pt(25)
        p.font.bold = True
        p.font.color.rgb = C_NAVY
        p.alignment = PP_ALIGN.CENTER

        # Underline bar
        bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(4.7), Inches(1.58), Inches(3.933), Inches(0.04))
        bar.fill.solid()
        bar.fill.fore_color.rgb = C_ROYAL
        bar.line.color.rgb = C_ROYAL

    # =========================================================================
    # SLIDE 1: TITLE SLIDE (Official Format)
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_layout)
    slide1.shapes.add_picture(title_bg, 0, 0, width=prs.slide_width, height=prs.slide_height)

    tbox = slide1.shapes.add_textbox(Inches(2.0), Inches(1.15), Inches(9.333), Inches(5.8))
    tf = tbox.text_frame
    tf.word_wrap = True

    p0 = tf.paragraphs[0]
    p0.text = "A Project Presentation\non"
    p0.font.name = "Georgia"
    p0.font.size = Pt(20)
    p0.font.italic = True
    p0.font.color.rgb = C_DARK
    p0.alignment = PP_ALIGN.CENTER

    p1 = tf.add_paragraph()
    p1.text = "Sentinel-X: AI-Based Network Attack Forecasting\nfrom Network Traffic Data"
    p1.font.name = "Georgia"
    p1.font.size = Pt(25)
    p1.font.bold = True
    p1.font.color.rgb = C_NAVY
    p1.alignment = PP_ALIGN.CENTER
    p1.space_before = Pt(8)
    p1.space_after = Pt(14)

    p2 = tf.add_paragraph()
    p2.text = "Presentation by :"
    p2.font.name = "Arial"
    p2.font.size = Pt(15)
    p2.font.bold = True
    p2.font.color.rgb = C_DARK
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
        pm.font.color.rgb = C_BODY
        pm.alignment = PP_ALIGN.CENTER

    p3 = tf.add_paragraph()
    p3.text = "Under the guidance of :"
    p3.font.name = "Arial"
    p3.font.size = Pt(14)
    p3.font.bold = True
    p3.font.color.rgb = C_DARK
    p3.alignment = PP_ALIGN.CENTER
    p3.space_before = Pt(10)

    p4 = tf.add_paragraph()
    p4.text = "Mr. Akash Gupta\n(Assistant Professor)"
    p4.font.name = "Arial"
    p4.font.size = Pt(14)
    p4.font.bold = True
    p4.font.color.rgb = C_NAVY
    p4.alignment = PP_ALIGN.CENTER

    p5 = tf.add_paragraph()
    p5.text = "Department of Computer Science and Engineering\nBuddha Institute of Technology, GIDA, Gorakhpur\nSession 2026-27"
    p5.font.name = "Georgia"
    p5.font.size = Pt(13.5)
    p5.font.bold = True
    p5.font.color.rgb = C_RED
    p5.alignment = PP_ALIGN.CENTER
    p5.space_before = Pt(10)

    # =========================================================================
    # SLIDE 2: ROADMAP / AGENDA (VISUAL PROCESS CARDS)
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    setup_slide(slide2, "Project Content Roadmap")

    agenda_cards = [
        ("01", "Introduction & Shift", "Reactive NIDS vs Predictive Forecasting (SIH26153)"),
        ("02", "Literature & Objectives", "Survey of existing NIDS & research gaps addressed"),
        ("03", "System Pipeline", "End-to-end telemetry workflow & architecture"),
        ("04", "16 State Features", "10s aggregation capturing attack kinetics"),
        ("05", "Sequence Windowing", "Leak-free chronological 70/15/15 splitting"),
        ("06", "LSTM World Model", "2-layer backbone with 3 multi-task heads"),
        ("07", "Autoregressive Rollout", "Multi-step rollout (T+1..T+3) & joint loss"),
        ("08", "MITRE ATT&CK Lifecycle", "5-stage conservative behavioral progression"),
        ("09", "Explainable AI (SHAP)", "Signed risk drivers, inhibitors & temporal saliency"),
        ("10", "Empirical Benchmarks", "100% Recall, 75% FPR reduction & degradation"),
        ("11", "SOC Command Dashboard", "5 interactive views running locally offline"),
        ("12", "Relevance & Conclusion", "Critical defense, green AI & future SDN roadmap"),
    ]

    for i, (num, heading, sub) in enumerate(agenda_cards):
        row = i // 4
        col = i % 4
        x = Inches(1.0 + col * 2.85)
        y = Inches(1.9 + row * 1.65)

        card = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Inches(2.7), Inches(1.45))
        card.fill.solid()
        card.fill.fore_color.rgb = C_CARD_BG
        card.line.color.rgb = C_ROYAL
        card.line.width = Pt(1.5)

        c_tf = card.text_frame
        c_tf.word_wrap = True
        
        p = c_tf.paragraphs[0]
        p.text = f"{num}. {heading}"
        p.font.name = "Georgia"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = C_NAVY
        p.space_after = Pt(2)

        pr = c_tf.add_paragraph()
        pr.text = sub
        pr.font.name = "Arial"
        pr.font.size = Pt(9.5)
        pr.font.color.rgb = C_BODY

    # =========================================================================
    # SLIDE 3: PROBLEM STATEMENT & THE PARADIGM SHIFT
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    setup_slide(slide3, "Problem Statement: Shift to Predictive Defense")

    # Diagram
    img3 = str(V2_DIR / "diag_reactive_vs_predictive.png")
    slide3.shapes.add_picture(img3, Inches(1.4), Inches(1.85), width=Inches(10.5))

    # Bottom summary callout card
    callout3 = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.4), Inches(6.15), Inches(10.5), Inches(0.95))
    callout3.fill.solid()
    callout3.fill.fore_color.rgb = C_CARD_BG
    callout3.line.color.rgb = C_BORDER
    callout3.line.width = Pt(1.5)
    c3_tf = callout3.text_frame
    c3_tf.word_wrap = True
    p = c3_tf.paragraphs[0]
    p.text = "SIH26153 Mandate: Transition from reactive detection (alerting post-breach) to predictive forecasting."
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = C_NAVY
    p2 = c3_tf.add_paragraph()
    p2.text = "• By predicting risk 10 to 30 seconds into the future, automated firewall policies can isolate malicious hosts before damage occurs."
    p2.font.size = Pt(11)
    p2.font.color.rgb = C_BODY

    # =========================================================================
    # SLIDE 4: SYSTEM ARCHITECTURE & END-TO-END PIPELINE
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    setup_slide(slide4, "End-to-End System Pipeline")

    img4 = str(V2_DIR / "diag_pipeline_flowchart.png")
    slide4.shapes.add_picture(img4, Inches(1.15), Inches(1.85), width=Inches(11.0))

    callout4 = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.15), Inches(6.25), Inches(11.0), Inches(0.85))
    callout4.fill.solid()
    callout4.fill.fore_color.rgb = C_CARD_BG
    callout4.line.color.rgb = C_BORDER
    callout4.line.width = Pt(1.5)
    c4_tf = callout4.text_frame
    c4_tf.word_wrap = True
    p = c4_tf.paragraphs[0]
    p.text = "Closed-Loop Data & Neural Pipeline: Raw Flows → 10s Window Aggregator → 2-Layer LSTM → 3 Heads → Rollout → Dashboard"
    p.font.bold = True
    p.font.size = Pt(11.5)
    p.font.color.rgb = C_NAVY

    # =========================================================================
    # SLIDE 5: THE 16 NETWORK STATE FEATURES
    # =========================================================================
    slide5 = prs.slides.add_slide(blank_layout)
    setup_slide(slide5, "16-Dimensional Network State Representation")

    img5 = str(V2_DIR / "diag_16_features_grid.png")
    slide5.shapes.add_picture(img5, Inches(1.4), Inches(1.85), width=Inches(10.5))

    callout5 = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.4), Inches(6.25), Inches(10.5), Inches(0.85))
    callout5.fill.solid()
    callout5.fill.fore_color.rgb = C_CARD_BG
    callout5.line.color.rgb = C_BORDER
    callout5.line.width = Pt(1.5)
    c5_tf = callout5.text_frame
    c5_tf.word_wrap = True
    p = c5_tf.paragraphs[0]
    p.text = "Why 10-Second Windows? Packet-by-packet sniffing overflows memory on gigabit links; statistical windowing captures attack kinetics."
    p.font.bold = True
    p.font.size = Pt(11.5)
    p.font.color.rgb = C_NAVY

    # =========================================================================
    # SLIDE 6: LEAK-FREE CHRONOLOGICAL SEQUENCE ENGINEERING
    # =========================================================================
    slide6 = prs.slides.add_slide(blank_layout)
    setup_slide(slide6, "Leak-Free Chronological Windowing")

    img6 = str(V2_DIR / "diag_chronological_split.png")
    slide6.shapes.add_picture(img6, Inches(1.4), Inches(1.85), width=Inches(10.5))

    callout6 = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.4), Inches(6.15), Inches(10.5), Inches(0.95))
    callout6.fill.solid()
    callout6.fill.fore_color.rgb = C_CARD_BG
    callout6.line.color.rgb = C_BORDER
    callout6.line.width = Pt(1.5)
    c6_tf = callout6.text_frame
    c6_tf.word_wrap = True
    p = c6_tf.paragraphs[0]
    p.text = "Guaranteed Zero Data Leakage: Standard train_test_split(shuffle=True) causes temporal leakage in time series."
    p.font.bold = True
    p.font.size = Pt(11.5)
    p.font.color.rgb = C_NAVY
    p2 = c6_tf.add_paragraph()
    p2.text = "• Strict chronological split (Train 70% | Val 15% | Test 15%). Scaler is fitted strictly on the training set."
    p2.font.size = Pt(10.5)
    p2.font.color.rgb = C_BODY

    # =========================================================================
    # SLIDE 7: DEEP LSTM WORLD MODEL ARCHITECTURE
    # =========================================================================
    slide7 = prs.slides.add_slide(blank_layout)
    setup_slide(slide7, "Deep LSTM World Model Architecture")

    img7 = str(V2_DIR / "diag_world_model.png")
    slide7.shapes.add_picture(img7, Inches(1.4), Inches(1.85), width=Inches(10.5))

    callout7 = slide7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.4), Inches(6.15), Inches(10.5), Inches(0.95))
    callout7.fill.solid()
    callout7.fill.fore_color.rgb = C_CARD_BG
    callout7.line.color.rgb = C_BORDER
    callout7.line.width = Pt(1.5)
    c7_tf = callout7.text_frame
    c7_tf.word_wrap = True
    p = c7_tf.paragraphs[0]
    p.text = "World Model Paradigm: It doesn't just output a static class; it predicts how the environment itself evolves."
    p.font.bold = True
    p.font.size = Pt(11.5)
    p.font.color.rgb = C_NAVY
    p2 = c7_tf.add_paragraph()
    p2.text = "• 2-Layer LSTM (Hidden 128) concurrently drives: Risk Head (BCE), Stage Head (CE), and State Reconstructor (MSE)."
    p2.font.size = Pt(10.5)
    p2.font.color.rgb = C_BODY

    # =========================================================================
    # SLIDE 8: AUTOREGRESSIVE ROLLOUT & MULTI-TASK LOSS
    # =========================================================================
    slide8 = prs.slides.add_slide(blank_layout)
    setup_slide(slide8, "Autoregressive Rollout & Multi-Task Loss")

    img8 = str(V2_DIR / "diag_rollout_loss.png")
    slide8.shapes.add_picture(img8, Inches(1.4), Inches(1.85), width=Inches(10.5))

    callout8 = slide8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.4), Inches(6.25), Inches(10.5), Inches(0.85))
    callout8.fill.solid()
    callout8.fill.fore_color.rgb = C_CARD_BG
    callout8.line.color.rgb = C_BORDER
    callout8.line.width = Pt(1.5)
    c8_tf = callout8.text_frame
    c8_tf.word_wrap = True
    p = c8_tf.paragraphs[0]
    p.text = "Auxiliary Task Regularization: Predicting continuous state (w_state=0.2) forces the LSTM to learn real network physics."
    p.font.bold = True
    p.font.size = Pt(11.5)
    p.font.color.rgb = C_NAVY

    # =========================================================================
    # SLIDE 9: MITRE ATT&CK BEHAVIORAL LIFECYCLE
    # =========================================================================
    slide9 = prs.slides.add_slide(blank_layout)
    setup_slide(slide9, "Conservative MITRE ATT&CK Lifecycle")

    img9 = str(V2_DIR / "diag_mitre_chevrons.png")
    slide9.shapes.add_picture(img9, Inches(1.4), Inches(1.85), width=Inches(10.5))

    callout9 = slide9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.4), Inches(6.15), Inches(10.5), Inches(0.95))
    callout9.fill.solid()
    callout9.fill.fore_color.rgb = C_CARD_BG
    callout9.line.color.rgb = C_BORDER
    callout9.line.width = Pt(1.5)
    c9_tf = callout9.text_frame
    c9_tf.word_wrap = True
    p = c9_tf.paragraphs[0]
    p.text = "Academic Defensive Posture: We classify behavioral telemetry stages for SOC triage, NOT definitive forensic certainty."
    p.font.bold = True
    p.font.size = Pt(11.5)
    p.font.color.rgb = C_NAVY
    p2 = c9_tf.add_paragraph()
    p2.text = "• 5 Distinct Stages: Benign Baseline (0) → Recon (1) → Initial Access (2) → Lateral Movement (3) → Command & Control (4)."
    p2.font.size = Pt(10.5)
    p2.font.color.rgb = C_BODY

    # =========================================================================
    # SLIDE 10: EXPLAINABLE AI (SHAP THREAT ATTRIBUTION)
    # =========================================================================
    slide10 = prs.slides.add_slide(blank_layout)
    setup_slide(slide10, "Explainable AI (SHAP Threat Attribution)")

    img10 = str(V2_DIR / "diag_shap_force.png")
    slide10.shapes.add_picture(img10, Inches(1.4), Inches(1.85), width=Inches(10.5))

    callout10 = slide10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.4), Inches(6.15), Inches(10.5), Inches(0.95))
    callout10.fill.solid()
    callout10.fill.fore_color.rgb = C_CARD_BG
    callout10.line.color.rgb = C_BORDER
    callout10.line.width = Pt(1.5)
    c10_tf = callout10.text_frame
    c10_tf.word_wrap = True
    p = c10_tf.paragraphs[0]
    p.text = "Eliminating the Black Box: Explains exactly WHY future risk was predicted to escalate."
    p.font.bold = True
    p.font.size = Pt(11.5)
    p.font.color.rgb = C_NAVY
    p2 = c10_tf.add_paragraph()
    p2.text = "• Red Bars = Risk Drivers (syn_ratio, packet_rate)  |  Green Bars = Risk Inhibitors (ack_ratio, duration_mean)."
    p2.font.size = Pt(10.5)
    p2.font.color.rgb = C_BODY

    # =========================================================================
    # SLIDE 11: EXPERIMENTAL RESULTS & BENCHMARKS
    # =========================================================================
    slide11 = prs.slides.add_slide(blank_layout)
    setup_slide(slide11, "Empirical Results: Baseline vs. World Model")

    img11 = str(ASSETS_DIR / "chart_performance.png")
    slide11.shapes.add_picture(img11, Inches(1.4), Inches(1.85), width=Inches(7.2))

    # Right side metric callouts
    callouts11 = [
        ("100.0% RECALL", "Zero missed attacks at T+1\n(Baseline missed 2.2%)", C_GREEN),
        ("75% LESS FALSE ALARMS", "FPR reduced from 20% to 5%\nDirectly solves alert fatigue", C_ROYAL),
        ("0.9834 F1-SCORE", "F1 tapers to 0.9721 at T+3\n(Expected horizon decay)", C_BORDER),
    ]

    for idx, (stat, detail, colr) in enumerate(callouts11):
        y_pos = Inches(1.95 + idx * 1.5)
        stat_card = slide11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.8), y_pos, Inches(3.2), Inches(1.3))
        stat_card.fill.solid()
        stat_card.fill.fore_color.rgb = C_CARD_BG
        stat_card.line.color.rgb = colr
        stat_card.line.width = Pt(2)
        sc_tf = stat_card.text_frame
        sc_tf.word_wrap = True
        p = sc_tf.paragraphs[0]
        p.text = stat
        p.font.name = "Georgia"
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = colr
        p2 = sc_tf.add_paragraph()
        p2.text = detail
        p2.font.size = Pt(10)
        p2.font.color.rgb = C_BODY
        p2.space_before = Pt(2)

    callout11 = slide11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.4), Inches(6.35), Inches(10.6), Inches(0.75))
    callout11.fill.solid()
    callout11.fill.fore_color.rgb = C_CARD_BG
    callout11.line.color.rgb = C_BORDER
    callout11.line.width = Pt(1.5)
    c11_tf = callout11.text_frame
    c11_tf.word_wrap = True
    p = c11_tf.paragraphs[0]
    p.text = "Key Takeaway: Predictive variance compounds naturally as horizon extends, proving genuine autoregressive rollout."
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = C_NAVY

    # =========================================================================
    # SLIDE 12: INTERACTIVE SOC COMMAND DASHBOARD
    # =========================================================================
    slide12 = prs.slides.add_slide(blank_layout)
    setup_slide(slide12, "Interactive SOC Command Dashboard")

    img12 = str(ASSETS_DIR / "dashboard_screenshot.png")
    slide12.shapes.add_picture(img12, Inches(1.4), Inches(1.75), width=Inches(10.5))

    callout12 = slide12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.4), Inches(6.20), Inches(10.5), Inches(0.85))
    callout12.fill.solid()
    callout12.fill.fore_color.rgb = C_CARD_BG
    callout12.line.color.rgb = C_BORDER
    callout12.line.width = Pt(1.5)
    c12_tf = callout12.text_frame
    c12_tf.word_wrap = True
    p = c12_tf.paragraphs[0]
    p.text = "5 Operational Views: Executive Risk Gauge | Forecast Timeline (95% CI) | Threat Attribution | Benchmarks | System Status"
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = C_NAVY

    # =========================================================================
    # SLIDE 13: RELEVANCE, FEASIBILITY & FUTURE SCOPE
    # =========================================================================
    slide13 = prs.slides.add_slide(blank_layout)
    setup_slide(slide13, "Societal Impact & Future Roadmap")

    img13 = str(V2_DIR / "diag_future_pillars.png")
    slide13.shapes.add_picture(img13, Inches(1.4), Inches(1.85), width=Inches(10.5))

    callout13 = slide13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.4), Inches(6.15), Inches(10.5), Inches(0.95))
    callout13.fill.solid()
    callout13.fill.fore_color.rgb = C_CARD_BG
    callout13.line.color.rgb = C_BORDER
    callout13.line.width = Pt(1.5)
    c13_tf = callout13.text_frame
    c13_tf.word_wrap = True
    p = c13_tf.paragraphs[0]
    p.text = "Green AI Architecture: Single-sample inference latency < 20 ms on standard laptop CPU with zero cloud costs."
    p.font.bold = True
    p.font.size = Pt(11.5)
    p.font.color.rgb = C_NAVY
    p2 = c13_tf.add_paragraph()
    p2.text = "• Proactive shielding for critical infrastructure (power, banking, healthcare) against multi-phase ransomware & breaches."
    p2.font.size = Pt(10.5)
    p2.font.color.rgb = C_BODY

    # =========================================================================
    # SLIDE 14: CONCLUSION & THANK YOU
    # =========================================================================
    slide14 = prs.slides.add_slide(blank_layout)
    slide14.shapes.add_picture(thankyou_bg, 0, 0, width=prs.slide_width, height=prs.slide_height)

    # Center card below THANK YOU
    ty_card = slide14.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.8), Inches(4.35), Inches(9.733), Inches(2.7))
    ty_card.fill.solid()
    ty_card.fill.fore_color.rgb = C_CARD_BG
    ty_card.line.color.rgb = C_BORDER
    ty_card.line.width = Pt(2)
    ty_tf = ty_card.text_frame
    ty_tf.word_wrap = True

    p = ty_tf.paragraphs[0]
    p.text = "Questions & Discussion"
    p.font.name = "Georgia"
    p.font.size = Pt(21)
    p.font.bold = True
    p.font.color.rgb = C_NAVY
    p.alignment = PP_ALIGN.CENTER

    p_team = ty_tf.add_paragraph()
    p_team.text = "Shristi Jaiswal  |  Suraj Prakash Chaudhary  |  Suraj Upadhyay  |  Udai Kumar Srivastava"
    p_team.font.name = "Arial"
    p_team.font.size = Pt(13.5)
    p_team.font.bold = True
    p_team.font.color.rgb = C_DARK
    p_team.alignment = PP_ALIGN.CENTER
    p_team.space_before = Pt(6)

    p_guide = ty_tf.add_paragraph()
    p_guide.text = "Under the guidance of: Mr. Akash Gupta (Assistant Professor)\nDepartment of Computer Science and Engineering\nBuddha Institute of Technology, GIDA, Gorakhpur"
    p_guide.font.name = "Arial"
    p_guide.font.size = Pt(12)
    p_guide.font.bold = True
    p_guide.font.color.rgb = C_RED
    p_guide.alignment = PP_ALIGN.CENTER
    p_guide.space_before = Pt(4)

    p_link = ty_tf.add_paragraph()
    p_link.text = "GitHub: github.com/surajbuilds53/sentinel-x   |   Live Hub: sentinel-x-lilac.vercel.app"
    p_link.font.name = "Arial"
    p_link.font.size = Pt(11.5)
    p_link.font.color.rgb = C_MUTED
    p_link.alignment = PP_ALIGN.CENTER
    p_link.space_before = Pt(6)

    prs.save(str(OUTPUT_PPTX))
    print(f"Visual 14-slide presentation generated successfully at: {OUTPUT_PPTX}")


if __name__ == "__main__":
    create_visual_presentation()
