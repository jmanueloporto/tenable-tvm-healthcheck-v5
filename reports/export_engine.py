"""
PROJECT: [V5-Tenable Health Check API Automation]
VERSION: 5.3.3
LAYER: Reports / Export
DESCRIPTION: Full Triple-Engine (JSON/TXT/PDF) with Failsafe Encoding.
AUTHOR: Senior Software Architect
"""
import os
import json
from datetime import datetime
from fpdf import FPDF
from typing import List, Dict
from core.models import Finding

def clean_text(text):
    if not text: return "N/A"
    cleaned = str(text).replace('$', 'USD').replace('>', 'gt').replace('<', 'lt')
    return cleaned.encode('ascii', 'ignore').decode('ascii')

def generate_reports(findings: List[Finding], scores: Dict[int, float], global_score: float, exec_time: float):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    report_dir = "reports/reports"
    os.makedirs(report_dir, exist_ok=True)
    base_filename = f"{report_dir}/Audit_Report_{timestamp}"
    
    domain_map = {
        1: "Asset Visibility (Shadow IT)", 2: "Scanning Operations",
        3: "Risk Prioritization", 4: "Remediation & SLA",
        5: "Identity Hygiene", 6: "Ecosystem & Governance"
    }

    # 1. JSON para Dashboard
    dashboard_data = {
        "timestamp": datetime.now().isoformat(),
        "execution_time": round(exec_time, 2),
        "global_score": round(global_score, 2),
        "domain_scores": scores,
        "findings": [{"title": f.title, "domain": f.domain, "score": f.override_score or f.score, "observation": f.observation} for f in findings]
    }
    with open("reports/latest_results.json", "w", encoding='utf-8') as jf:
        json.dump(dashboard_data, jf, indent=4)

    # 2. TXT Forense (RESTAURADO)
    with open(f"{base_filename}.txt", "w", encoding='utf-8') as f:
        f.write("="*70 + "\n")
        f.write(f"{'DETAILED MATURITY AUDIT REPORT (v5.3.3)':^70}\n")
        f.write("="*70 + "\n\n")
        f.write(f"GLOBAL SCORE: {global_score:.2f} / 5.0 | Time: {exec_time:.2f}s\n\n")
        for idx, issue in enumerate(findings, 1):
            f.write(f"Finding #{idx}: {issue.title}\n")
            f.write(f" Observation : {issue.observation}\n")
            f.write("-" * 40 + "\n")

    # 3. PDF Ejecutivo Robusto
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(190, 15, 'TENABLE HEALTH CHECK - EXECUTIVE DASHBOARD', 1, 1, 'C', True)
    pdf.ln(5)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(95, 10, clean_text(f"Global Score: {global_score:.2f}"), 1, 0, 'C')
    pdf.cell(95, 10, clean_text(f"Time: {exec_time:.2f}s"), 1, 1, 'C')
    pdf.ln(5)

    pdf.set_text_color(180, 0, 0)
    pdf.cell(190, 10, "CRITICAL FINDINGS AND ALERTS", 0, 1, 'L')
    pdf.set_text_color(0, 0, 0)
    
    for issue in findings:
        impact = issue.override_score if issue.override_score is not None else issue.score
        if impact >= 2.0:
            pdf.set_font("Arial", 'B', 10)
            pdf.cell(190, 8, clean_text(f"ALERTA: {issue.title}"), 'T', 1, 'L')
            pdf.set_font("Arial", '', 9)
            pdf.multi_cell(190, 5, clean_text(f"Detalle: {issue.observation}"), 0, 'L')
            pdf.ln(2)

    pdf.output(f"{base_filename}.pdf")
    print(f"[*] Full Triple-Reports (JSON/TXT/PDF) generated (v5.3.3).")
