""" VERSION: 5.5.0-STABLE | STATUS: HYBRID REPORTING FIXED """
import datetime, os
from fpdf import FPDF

class ReportGenerator:
    def __init__(self, data):
        self.data = data
        self.report_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def _compile_text(self):
        content = []
        content.append("1.1 SENSOR INFRASTRUCTURE SUMMARY")
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
        
        content.append("\n\n2.1 EXECUTIVE FINDINGS (DOMAIN ANALYSIS)")
        content.append("-" * 60)
        findings = self.data.get('findings', [])
        if findings:
            for f in findings:
                content.append(f">>> [DOM {f['domain']}] {f['title']}")
                content.append(f"    Score: {f['override_score']}")
                content.append(f"    Obs: {f['observation']}\n")
        else:
            content.append("No critical findings detected.")
            
        return content

    def generate_txt(self, filename):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("="*60 + f"\n      TENABLE AUDIT REPORT v5.5.0-STABLE\n" + "="*60 + "\n\n")
            f.writelines([line + "\n" for line in self._compile_text()])

    def generate_pdf(self, filename):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        
        # Título
        pdf.set_font("Courier", 'B', 14)
        pdf.cell(190, 10, "Tenable TVM HealthCheck Report v5.5.0-STABLE", ln=True, align='C')
        pdf.ln(5)
        
        # Contenido
        pdf.set_font("Courier", size=8)
        for line in self._compile_text():
            # Limpiar caracteres no compatibles con latin-1 para evitar errores de encoding
            safe_line = line.encode('latin-1', 'replace').decode('latin-1')
            pdf.multi_cell(190, 5, safe_line)
            
        pdf.output(filename)
