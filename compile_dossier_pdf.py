import os
import re
import markdown
from playwright.sync_api import sync_playwright

workspace = r"c:\Users\nithin.reddy\Desktop\Loreal"

# Ordered list of active, authoritative OptiChroma v2.4 documents
files = [
    ("concept/claims-governance.md", "Executive Summary & Non-Negotiable Claims Governance"),
    ("research/evidence-register.md", "Evidence Register & Claims Auditing Baseline"),
    ("research/mission-analysis.md", "Brandstorm 2027 Mission Analysis & LDB Strategic Alignment"),
    ("research/scientific-evidence.md", "Scientific Foundations: Photomedicine, Cross-Polarization & Colorimetry"),
    ("research/market-research.md", "Market Epidemiology, Deeply Pigmented Skin Optics & Pharmacy Triage"),
    ("research/competitor-analysis.md", "Competitor Benchmarking & Innovation White Space"),
    ("concept/optichroma-concept.md", "La Roche-Posay OptiChroma v2.3 — Core Concept Specification"),
    ("concept/user-workflow.md", "Multi-Stakeholder Clinical & Commercial User Journeys"),
    ("architecture/optichroma-v2.4-engineering-spec.md", "Master Systems Architecture & MVP Engineering Specification"),
    ("architecture/hardware-design.md", "Optical, Mechanical & Forensic Electrical Architecture"),
    ("architecture/camera-acquisition.md", "Camera Acquisition Architecture & Sensor Calibration"),
    ("architecture/image-processing-pipeline.md", "Computational Vision Pipeline & Mathematical Formulations"),
    ("architecture/validation-protocol.md", "Laboratory Verification & Non-Invasive Validation Protocols"),
    ("submission/pitch-deck-content.md", "Official Brandstorm 2027 3-Slide Pitch Deck (Working Draft)"),
    ("submission/video-script-outline.md", "Official Brandstorm 2027 3-Minute Video Script (Working Draft)")
]

css = """
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

@page {
    size: A4;
    margin: 20mm 15mm 20mm 15mm;
}

body {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    color: #0f172a;
    background-color: #ffffff;
    line-height: 1.6;
    font-size: 9.5pt;
}

/* Cover Page */
.cover-page {
    height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    page-break-after: always;
    padding: 35px 25px;
    box-sizing: border-box;
    background: linear-gradient(135deg, #001233 0%, #002244 40%, #001b3a 100%);
    color: #ffffff;
    border-radius: 8px;
    position: relative;
    overflow: hidden;
}

.cover-page::before {
    content: "";
    position: absolute;
    top: -50px;
    right: -50px;
    width: 300px;
    height: 300px;
    background: radial-gradient(circle, rgba(0, 158, 226, 0.25) 0%, rgba(0, 0, 0, 0) 70%);
    border-radius: 50%;
}

.cover-header {
    border-bottom: 2px solid rgba(0, 158, 226, 0.5);
    padding-bottom: 20px;
}

.cover-brand {
    font-size: 13pt;
    letter-spacing: 4px;
    text-transform: uppercase;
    color: #009ee2;
    font-weight: 800;
}

.cover-pill {
    display: inline-block;
    padding: 6px 16px;
    background: rgba(0, 158, 226, 0.15);
    border: 1px solid rgba(0, 158, 226, 0.4);
    color: #38bdf8;
    border-radius: 20px;
    font-size: 8pt;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-top: 15px;
}

.cover-title {
    font-size: 26pt;
    font-weight: 800;
    line-height: 1.15;
    margin-top: 25px;
    margin-bottom: 12px;
    letter-spacing: -0.5px;
    color: #ffffff;
}

.cover-tagline {
    font-size: 12.5pt;
    color: #38bdf8;
    font-weight: 600;
    margin-bottom: 12px;
}

.cover-subtitle {
    font-size: 10pt;
    color: #cbd5e1;
    font-weight: 400;
    line-height: 1.5;
    max-width: 94%;
}

.cover-meta {
    margin-top: auto;
    border-top: 1px solid rgba(255, 255, 255, 0.15);
    padding-top: 18px;
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 14px;
    font-size: 8pt;
}

.cover-meta-item strong {
    display: block;
    color: #009ee2;
    text-transform: uppercase;
    font-size: 7pt;
    letter-spacing: 1px;
    margin-bottom: 2px;
}

/* Typography */
h1, h2, h3, h4 {
    color: #0f172a;
    font-weight: 700;
    letter-spacing: -0.2px;
    page-break-after: avoid;
}

h1 {
    font-size: 14.5pt;
    border-bottom: 2px solid #e2e8f0;
    padding-bottom: 6px;
    margin-top: 26px;
    margin-bottom: 12px;
    color: #002244;
}

.section-divider {
    page-break-before: always;
}

h2 {
    font-size: 11.5pt;
    margin-top: 20px;
    margin-bottom: 10px;
    color: #1e293b;
    border-left: 4px solid #009ee2;
    padding-left: 10px;
}

h3 {
    font-size: 10pt;
    margin-top: 14px;
    margin-bottom: 6px;
    color: #334155;
}

p {
    margin-bottom: 8px;
}

/* Tables */
table {
    width: 100%;
    border-collapse: collapse;
    margin: 14px 0 18px 0;
    font-size: 7.5pt;
    page-break-inside: avoid;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    border-radius: 4px;
    overflow: hidden;
}

th, td {
    padding: 6px 8px;
    text-align: left;
    vertical-align: top;
    border: 1px solid #e2e8f0;
}

th {
    background-color: #002244;
    color: #ffffff;
    font-weight: 600;
    font-size: 7pt;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

tr:nth-child(even) td {
    background-color: #f8fafc;
}

tr:hover td {
    background-color: #f1f5f9;
}

/* Blockquotes & Callouts */
blockquote {
    margin: 14px 0;
    padding: 10px 16px;
    border-left: 4px solid #009ee2;
    background-color: #f0f9ff;
    color: #0369a1;
    border-radius: 0 4px 4px 0;
    font-style: normal;
    page-break-inside: avoid;
}

blockquote p {
    margin: 0;
    font-weight: 500;
}

/* Code & Pre Blocks */
pre {
    background-color: #0f172a;
    color: #f8fafc;
    padding: 10px 12px;
    border-radius: 4px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 7pt;
    line-height: 1.4;
    overflow-x: auto;
    page-break-inside: avoid;
    margin: 12px 0;
    border: 1px solid #1e293b;
}

code {
    font-family: 'JetBrains Mono', monospace;
    background-color: #f1f5f9;
    color: #0f172a;
    padding: 2px 4px;
    border-radius: 3px;
    font-size: 7.5pt;
}

pre code {
    background: transparent;
    color: inherit;
    padding: 0;
    font-size: inherit;
}

ul, ol {
    margin-bottom: 10px;
    padding-left: 18px;
}

li {
    margin-bottom: 3px;
}

a {
    color: #0284c7;
    text-decoration: none;
}

.table-of-contents {
    page-break-after: always;
    padding: 15px 0;
}

.toc-header {
    border-bottom: 2px solid #002244;
    padding-bottom: 8px;
    margin-bottom: 18px;
}

.toc-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 6px 0;
    border-bottom: 1px dashed #cbd5e1;
    font-size: 8pt;
    font-weight: 500;
}

.toc-number {
    font-weight: 700;
    color: #009ee2;
    margin-right: 8px;
}
"""

html_body = []

# Cover page
html_body.append("""
<div class="cover-page">
    <div class="cover-header">
        <div class="cover-brand">L'ORÉAL BRANDSTORM 2027</div>
        <div class="cover-pill">Playing Field 3 — Reinvent the Doctor-Patient Relationship</div>
    </div>
    <div class="cover-main">
        <div class="cover-title">LA ROCHE-POSAY OPTICHROMA (v2.4)</div>
        <div class="cover-tagline">Frozen Student MVP Specification & Forensic Verification Dossier</div>
        <div class="cover-subtitle">
            An accessible, standardized optical smartphone imaging attachment and reference-calibrated software platform designed to eliminate specular surface glare, standardize remote skin documentation across all skin tones, and empower patients, community pharmacists, and dermatologists.
        </div>
    </div>
    <div class="cover-meta">
        <div class="cover-meta-item">
            <strong>Target Brand & Division</strong>
            La Roche-Posay<br>
            L'Oréal Dermatological Beauty (LDB)
        </div>
        <div class="cover-meta-item">
            <strong>Innovation Taskforce</strong>
            Multidisciplinary Innovation Team<br>
            Optics • Computer Vision • Clinical Science • Strategy
        </div>
        <div class="cover-meta-item">
            <strong>System Classification</strong>
            Standardized Optical Capture Accessory<br>
            Non-Diagnostic Longitudinal Documentation Platform
        </div>
        <div class="cover-meta-item">
            <strong>Verification Baseline</strong>
            Version 2.4.0 (Frozen Student MVP Baseline)<br>
            42 / 42 Automated Unit Tests Passed (100% Pass Rate)
        </div>
    </div>
</div>
""")

# Table of Contents
toc_items = []
for idx, (rel_path, section_title) in enumerate(files, 1):
    category = "Architecture & Testing" if "architecture" in rel_path else ("Research & Evidence" if "research" in rel_path else ("Concept & Strategy" if "concept" in rel_path else "Competition Working Draft"))
    toc_items.append(f"""
    <div class="toc-item">
        <span><span class="toc-number">SECTION {idx:02d}</span> {section_title}</span>
        <span><em>{category}</em></span>
    </div>
    """)

html_body.append(f"""
<div class="table-of-contents">
    <div class="toc-header">
        <h1 style="border:none; margin:0; padding:0; color:#002244;">Table of Contents</h1>
        <p style="color:#64748b; font-size:8pt; margin:4px 0 0 0;">Forensic Master Dossier — Frozen Student MVP Baseline (v2.4)</p>
    </div>
    {''.join(toc_items)}
</div>
""")

# Convert each MD file
for idx, (rel_path, section_title) in enumerate(files, 1):
    full_path = os.path.join(workspace, rel_path)
    with open(full_path, "r", encoding="utf-8") as f:
        md_text = f.read()
    
    # Render to HTML
    converted_html = markdown.markdown(
        md_text,
        extensions=['tables', 'fenced_code', 'toc']
    )
    
    html_body.append(f"""
    <div class="section-divider">
        <div style="font-size:7pt; text-transform:uppercase; letter-spacing:1px; color:#009ee2; font-weight:700; margin-bottom:4px;">
            Section {idx:02d} — {section_title}
        </div>
        {converted_html}
    </div>
    """)

full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>L'Oréal Brandstorm 2027 — La Roche-Posay OptiChroma Final Dossier (v2.3)</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css">
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js"></script>
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js"
        onload="renderMathInElement(document.body, {{
            delimiters: [
                {{left: '$$', right: '$$', display: true}},
                {{left: '$', right: '$', display: false}}
            ]
        }});"></script>
    <style>
        {css}
    </style>
</head>
<body>
    {''.join(html_body)}
</body>
</html>
"""

temp_html_path = os.path.join(workspace, "dossier_final_temp.html")
output_pdf_path = os.path.join(workspace, "LOREAL_BRANDSTORM_2027_OPTICHROMA_FINAL_DOSSIER.pdf")

with open(temp_html_path, "w", encoding="utf-8") as f:
    f.write(full_html)

print("HTML generated. Compiling PDF with Playwright...")

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(f"file:///{temp_html_path.replace(os.sep, '/')}")
    page.wait_for_load_state("networkidle")
    
    page.pdf(
        path=output_pdf_path,
        format="A4",
        print_background=True,
        margin={"top": "20mm", "bottom": "20mm", "left": "15mm", "right": "15mm"},
        display_header_footer=True,
        header_template="<div style='font-size: 7pt; color: #64748b; width: 100%; text-align: right; padding-right: 15mm; font-family: sans-serif;'>La Roche-Posay OptiChroma v2.4 (MVP Freeze) | L'Oréal Brandstorm 2027</div>",
        footer_template="<div style='font-size: 7pt; color: #64748b; width: 100%; text-align: center; font-family: sans-serif;'><span class='pageNumber'></span> / <span class='totalPages'></span></div>"
    )
    browser.close()

if os.path.exists(temp_html_path):
    os.remove(temp_html_path)

print(f"Successfully generated final dossier PDF: {output_pdf_path}")
