"""
PROJECT: [V5-Tenable Health Check API Automation]
VERSION: 5.1.3
LAYER: Reports / Export
DESCRIPTION: Forensic PDF and Detailed TXT Report Generator.
AUTHOR: Senior Software Architect
"""
import os
from datetime import datetime
from fpdf import FPDF
from typing import List, Dict
from core.models import Finding

def generate_reports(findings: List[Finding], scores: Dict[int, float], global_score: float, exec_time: float):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    report_dir = "reports/reports"
    os.makedirs(report_dir, exist_ok=True)
    base_filename = f"{report_dir}/Audit_Report_{timestamp}"
    
    domain_map = {
        1: "Asset Visibility (Shadow IT)",
        2: "Scanning Operations",
        3: "Risk Prioritization",
        4: "Remediation & SLA",
        5: "Identity Hygiene",
        6: "Ecosystem & Governance"
    }

    # 1. Generación de TXT Forense Detallado (v5.1.3)
    with open(f"{base_filename}.txt", "w") as f:
        f.write("="*70 + "\n")
        f.write(f"{'DETAILED MATURITY AUDIT REPORT':^70}\n")
        f.write(f"{'Tenable.io Health Check v5.1.3':^70}\n")
        f.write("="*70 + "\n\n")
        
        f.write(f"Execution Time         : {exec_time:.2f} seconds\n")
        f.write(f"GLOBAL MATURITY SCORE  : {global_score:.2f} / 5.0\n\n")
        
        f.write("[I] DOMAIN SUMMARY\n")
        f.write("-" * 30 + "\n")
        for d_id, score in scores.items():
            f.write(f" > Domain {d_id} - {domain_map[d_id]:<30}: {score:.2f}/5.0\n")
        
        f.write("\n[II] DETAILED EVIDENCE & FINDINGS\n")
        f.write("-" * 30 + "\n")
        for idx, issue in enumerate(findings, 1):
            f.write(f"Finding #{idx}: {issue.title}\n")
            f.write(f" Domain      : {domain_map.get(issue.domain, 'Unknown')}\n")
            actual_score = issue.override_score if issue.override_score is not None else issue.score
            f.write(f" Score Impact: {actual_score:.1f}\n")
            f.write(f" Observation : {issue.observation}\n")
            f.write(" Recommendations:\n")
            for rec in issue.recommendations:
                f.write(f"   * {rec}\n")
            f.write("-" * 40 + "\n")

    # 2. PDF Placeholder
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(190, 10, 'Tenable Maturity Assessment v5.1.3', 1, 1, 'C')
    pdf.set_font("Arial", '', 12)
    pdf.ln(10)
    pdf.cell(190, 10, f"Global Score: {global_score:.2f} / 5.0", 0, 1)
    pdf.output(f"{base_filename}.pdf")
    
    print(f"[*] Forensic Reports saved: {base_filename}.txt/.pdf")
