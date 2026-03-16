# VERSION: 5.3.3-FINAL
"""
PROJECT: [V5-Tenable Health Check API Automation]
VERSION: 5.3.3
LAYER: Reports / Export
DESCRIPTION: Forensic PDF and TXT Report Generator.
AUTHOR: Senior Software Architect
"""
import os
from datetime import datetime
from fpdf import FPDF
from typing import List, Dict
from core.models import Finding

def generate_reports(findings: List[Finding], scores: Dict[int, float]):
    """
    Main entry point for report generation.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    report_dir = "reports/reports"
    os.makedirs(report_dir, exist_ok=True)
    
    base_filename = f"{report_dir}/Audit_Report_{timestamp}"
    
    # Simple TXT generation for verification
    with open(f"{base_filename}.txt", "w") as f:
        f.write("TENABLE HEALTH CHECK SUMMARY\n")
        f.write("="*30 + "\n")
        for domain, score in scores.items():
            f.write(f"Domain {domain}: {score:.2f}/5.0\n")
            
    print(f"[*] TXT Report saved in: {base_filename}.txt")
    
    # PDF generation logic (Minimalist)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(40, 10, 'Tenable Maturity Assessment v5.1.0')
    pdf.output(f"{base_filename}.pdf")
    print(f"[*] PDF Report saved in: {base_filename}.pdf")

