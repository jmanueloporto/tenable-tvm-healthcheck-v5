"""
PROJECT: [V5-Tenable Health Check API Automation]
VERSION: 5.0.19
LAYER: Reporting / Export
DESCRIPTION: Report Engine with nested directory support (reports/reports).
AUTHOR: Senior Software Architect
"""

import os
from datetime import datetime
from fpdf import FPDF

class ReportGenerator:
    def __init__(self, final_score, domain_scores, findings):
        self.final_score = final_score
        self.domain_scores = domain_scores
        self.findings = findings
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        self.reports_dir = "reports/reports"
        os.makedirs(self.reports_dir, exist_ok=True)
        
        self.dom_names = {
            1: "Asset Visibility & Inventory", 
            2: "Scanning Operations & Data Quality", 
            3: "Risk Prioritization & Analysis", 
            4: "Remediation & Response", 
            5: "Program Governance & Operations", 
            6: "Ecosystem Integration & Security Posture"
        }

    def _sanitize(self, text):
        return str(text).encode('latin-1', 'replace').decode('latin-1')

    def generate_txt(self):
        filename = f"Audit_Report_{self.timestamp}.txt"
        filepath = os.path.join(self.reports_dir, filename)
        with open(filepath, "w") as f:
            f.write("="*80 + "\n")
            f.write(f"{'DETAILED MATURITY AUDIT REPORT':^80}\n")
            f.write(f"{'Timestamp: ' + self.timestamp:^80}\n")
            f.write("="*80 + "\n\n")
            f.write(f"GLOBAL MATURITY SCORE: {self.final_score:.2f} / 5.0\n\n")
            
            f.write("DOMAIN SUMMARY:\n")
            for d_id, score in sorted(self.domain_scores.items()):
                f.write(f" [{d_id}] {self.dom_names.get(d_id):<45}: {score:.2f}/5.0\n")
            
            f.write("\nDETAILED EVIDENCE & FINDINGS:\n")
            f.write("-" * 80 + "\n")
            for find in self.findings:
                f.write(f"FINDING: {find.title} (Domain {find.domain})\n")
                f.write(f"EVIDENCE: {find.metrics.get('affected_accounts', 'N/A')}\n")
                f.write(f"RECS: {', '.join(find.recommendations)}\n")
                f.write("-" * 40 + "\n")
        
        print(f"[*] TXT Report saved in: {filepath}")

    def generate_pdf(self):
        filename = f"Audit_Report_{self.timestamp}.pdf"
        filepath = os.path.join(self.reports_dir, filename)
        pdf = FPDF()
        pdf.add_page()
        
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, txt="Tenable VM Executive Audit", ln=True, align='C')
        pdf.set_font("Arial", size=10)
        pdf.cell(0, 10, txt=f"Platform Score: {self.final_score:.2f} / 5.0", ln=True, align='C')
        pdf.ln(10)

        pdf.set_font("Arial", 'B', 11)
        pdf.set_fill_color(230, 230, 230)
        pdf.cell(140, 8, txt="Security Domain", border=1, fill=True)
        pdf.cell(50, 8, txt="Score", border=1, fill=True, ln=True)
        
        for d_id, score in sorted(self.domain_scores.items()):
            pdf.cell(140, 8, txt=f" {self.dom_names.get(d_id)}", border=1)
            pdf.cell(50, 8, txt=f"{score:.2f}/5.0", border=1, ln=True)
        pdf.ln(10)

        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, txt="Evidence & Recommendations", ln=True)
        
        for find in self.findings:
            pdf.set_font("Arial", 'B', 10)
            pdf.multi_cell(0, 7, txt=self._sanitize(f"Finding: {find.title}"))
            pdf.set_font("Arial", 'I', 9)
            pdf.set_text_color(100, 100, 100)
            evidence_text = f"Evidence: {find.metrics.get('affected_accounts', 'N/A')}"
            pdf.multi_cell(0, 5, txt=self._sanitize(evidence_text))
            pdf.set_text_color(0, 0, 0)
            pdf.set_font("Arial", size=9)
            pdf.multi_cell(0, 5, txt=self._sanitize(f"Action: {', '.join(find.recommendations)}"))
            pdf.ln(2)
            pdf.cell(0, 0, '', 'T', ln=True)
            pdf.ln(3)

        pdf.output(filepath)
        print(f"[*] PDF Report saved in: {filepath}")
