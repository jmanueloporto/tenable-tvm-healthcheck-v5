""" VERSION: 5.4.2 | STATUS: STABLE - PURE API """ VERSION: 5.4.2 | STATUS: STABLE - PURE API """ VERSION: 5.4.2 | STATUS: STABLE - PURE API """ VERSION: 5.4.2 | STATUS: STABLE - PURE API """ VERSION: 5.4.2 | STATUS: STABLE - PURE API """ VERSION: 5.4.2 | STATUS: STABLE - PURE API """ VERSION: 5.4.2 | STATUS: Stable | DESC: Full Incremental High-Fidelity Reporter with FPDF """ MTTR ENGINE """ MTTR ENGINE """ MTTR ENGINE """ MTTR ENGINE """ MTTR ENGINE """ MTTR ENGINE """
import datetime
import os
from fpdf import FPDF

class ReportGenerator:
    def __init__(self, data):
        self.data = data
        self.report_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def _compile_all_text(self):
        content = []
        
        # 1.1 Summary
        content.append("1.1 SENSOR INFRASTRUCTURE SUMMARY (DOMAIN 6)")
        content.append("-" * 60)
        content.append(f"{'Tipo de Sensor':<30} {'Cant.':<8} {'Activos':<10} {'Inactivos':<10}")
        stats = self.data.get('sensors', {}).get('stats_by_type', {})
        order = ["Nessus Scanners", "Nessus Agents", "Nessus Network Monitors", "OT Connectors", "Web Application Scanners"]
        for label in order:
            d = stats.get(label, {"qty": 0, "active": 0, "inactive": 0})
            content.append(f"{label:<30} {d['qty']:<8} {d['active']:<10} {d['inactive']:<10}")
        content.append(f"\nTOTAL SENSORS: {self.data.get('sensors',{}).get('summary',{}).get('total',0)}\n")

        # 1.2 Detailed Inventory
        content.append("1.2 DETAILED INVENTORY BY SENSOR TYPE")
        content.append("-" * 60)
        inventory = self.data.get('sensors', {}).get('inventory', [])
        for label in order:
            content.append(f"\n>>> CATEGORY: {label.upper()}")
            found = [s for s in inventory if s['label'] == label]
            if not found:
                content.append("   (No sensors detected in this category)")
            else:
                for s in found:
                    content.append(f" - {s['name'][:45]:<45} Status: {s['status']}")
        content.append("")

        # 1.3 Raw Types Summary
        content.append("1.3 DISCOVERY: API RAW TYPES (SUMMARY)")
        content.append("-" * 60)
        content.append(f"{'API Raw Type':<30} {'Cant.':<8} {'Activos':<10} {'Inactivos':<10}")
        raw_stats = {}
        for s in inventory:
            rt = s['raw_type']
            if rt not in raw_stats: raw_stats[rt] = {"q": 0, "a": 0, "i": 0}
            raw_stats[rt]["q"] += 1
            if s['status'] == "on": raw_stats[rt]["a"] += 1
            else: raw_stats[rt]["i"] += 1
        for rt, d in sorted(raw_stats.items()):
            content.append(f"{rt:<30} {d['q']:<8} {d['a']:<10} {d['i']:<10}")
        content.append("")

        # 1.4 Raw List
        content.append("1.4 DETAILED SENSOR LIST BY RAW TYPE")
        content.append("-" * 60)
        for rt in sorted(raw_stats.keys()):
            content.append(f"\n[RAW TYPE: {rt.upper()}]")
            for s in [i for i in inventory if i['raw_type'] == rt]:
                content.append(f" - {s['name'][:45]:<45} Status: {s['status']}")
        content.append("")

        # 2.1 Findings
        content.append("2.1 EXECUTIVE FINDINGS (DOMAIN ANALYSIS)")
        content.append("-" * 60)
        findings = self.data.get('findings', [])
        if not findings:
            content.append("No findings detected.")
        else:
            for f in findings:
                content.append(f">>> Domain {f['domain']}: {f['title']}")
                content.append(f"    Score Override: {f['override_score']}")
                content.append(f"    Observation: {f['observation']}\n")
        
        return content

    def generate_txt(self, filename):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        text_lines = self._compile_all_text()
        with open(filename, 'w') as f:
            f.write("=" * 60 + "\n")
            f.write("      TENABLE VULNERABILITY MANAGEMENT HEALTH CHECK\n")
            f.write(f"      Technical Audit Report v5.4.2 | {self.report_date}\n")
            f.write("=" * 60 + "\n\n")
            f.write("\n".join(text_lines))
            f.write("\n" + "=" * 60 + "\n")
            f.write("              END OF TECHNICAL AUDIT REPORT\n")
            f.write("=" * 60 + "\n")

    def generate_pdf(self, filename):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Courier", size=10)
        
        pdf.cell(190, 10, txt="TENABLE TVM HEALTH CHECK REPORT", ln=True, align='C')
        pdf.cell(190, 10, txt=f"Report Date: {self.report_date}", ln=True, align='C')
        pdf.ln(5)
        
        text_lines = self._compile_all_text()
        for line in text_lines:
            safe_line = line.encode('latin-1', 'replace').decode('latin-1')
            pdf.cell(0, 5, txt=safe_line, ln=True)
            
        pdf.output(filename)
