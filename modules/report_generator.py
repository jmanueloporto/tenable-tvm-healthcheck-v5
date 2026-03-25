""" VERSION: 5.4.2 | STATUS: STABLE - PURE API ARCHITECTURE & MTTR ENGINE """
import datetime, os
from fpdf import FPDF

class ReportGenerator:
    def __init__(self, data):
        self.data = data
        self.report_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def _compile_text(self):
        content = []
        content.append("1.1 SENSOR INFRASTRUCTURE SUMMARY (DOMAIN 6)")
        content.append("-" * 60)
        content.append(f"{'Tipo de Sensor':<30} {'Cant.':<8} {'Activos':<10} {'Inactivos':<10}")
        stats = self.data.get('sensors', {}).get('stats_by_type', {})
        order = ["Nessus Scanners", "Nessus Agents", "Nessus Network Monitors", "OT Connectors", "Web Application Scanners"]
        for label in order:
            d = stats.get(label, {"qty": 0, "active": 0, "inactive": 0})
            content.append(f"{label:<30} {d['qty']:<8} {d['active']:<10} {d['inactive']:<10}")
        
        content.append(f"\nTOTAL SENSORS: {self.data.get('sensors',{}).get('summary',{}).get('total',0)}")

        content.append("\n1.2 DETAILED INVENTORY BY SENSOR TYPE")
        content.append("-" * 60)
        inventory = self.data.get('sensors', {}).get('inventory', [])
        for label in order:
            content.append(f"\n>>> CATEGORY: {label.upper()}")
            found = [s for s in inventory if s['label'] == label]
            if not found:
                content.append("   (No sensors detected)")
            else:
                for s in found:
                    content.append(f" - {s['name'][:45]:<45} Status: {s['status']}")
        
        content.append("\n2.1 EXECUTIVE FINDINGS (DOMAIN ANALYSIS)")
        content.append("-" * 60)
        for f in self.data.get('findings', []):
            content.append(f">>> Domain {f['domain']}: {f['title']}\n    Score: {f['override_score']}\n    Obs: {f['observation']}\n")
        return content

    def generate_txt(self, filename):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w') as f:
            f.write("="*60 + f"\n      TENABLE AUDIT REPORT v5.4.2\n" + "="*60 + "\n\n")
            f.write("\n".join(self._compile_text()))

    def generate_pdf(self, filename):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 15, "Tenable TVM HealthCheck Report", ln=True, align='C')
        pdf.set_font("Courier", size=8)
        for line in self._compile_text():
            safe = line.encode('latin-1', 'replace').decode('latin-1')
            pdf.multi_cell(0, 4, safe)
        pdf.output(filename)
