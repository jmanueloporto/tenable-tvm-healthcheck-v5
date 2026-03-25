""" VERSION: 5.5.0-STABLE | STATUS: PDF PAGINATION FORCED """
import datetime, os
from fpdf import FPDF

class ReportGenerator:
    def __init__(self, data):
        self.data = data
        self.report_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def _get_lines(self):
        """Genera una lista de líneas limpias para el reporte"""
        lines = []
        lines.append("1.1 SENSOR INFRASTRUCTURE SUMMARY")
        lines.append("-" * 60)
        lines.append(f"{'Tipo de Sensor':<30} {'Cant.':<8} {'Activos':<10} {'Inactivos':<10}")
        
        stats = self.data.get('sensors', {}).get('stats_by_type', {})
        order = ["Nessus Scanners", "Nessus Agents", "Nessus Network Monitors", "OT Connectors", "Web Application Scanners"]
        for label in order:
            d = stats.get(label, {"qty": 0, "active": 0, "inactive": 0})
            lines.append(f"{label:<30} {d['qty']:<8} {d['active']:<10} {d['inactive']:<10}")
        
        lines.append(f"\nTOTAL SENSORS: {self.data.get('sensors',{}).get('summary',{}).get('total',0)}")
        lines.append("\n1.2 DETAILED INVENTORY BY SENSOR TYPE")
        lines.append("-" * 60)
        
        inventory = self.data.get('sensors', {}).get('inventory', [])
        for label in order:
            lines.append(f"\n>>> CATEGORY: {label.upper()}")
            found = [s for s in inventory if s['label'] == label]
            if not found:
                lines.append("   (No sensors detected)")
            else:
                for s in found:
                    lines.append(f" - {s['name'][:45]:<45} Status: {s['status']}")
        
        lines.append("\n\n2.1 EXECUTIVE FINDINGS (DOMAIN ANALYSIS)")
        lines.append("-" * 60)
        findings = self.data.get('findings', [])
        if findings:
            for f in findings:
                lines.append(f">>> [DOM {f['domain']}] {f['title']}")
                lines.append(f"    Score: {f['override_score']}")
                lines.append(f"    Obs: {f['observation']}\n")
        else:
            lines.append("No critical findings detected.")
            
        return lines

    def generate_txt(self, filename):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("="*60 + f"\n      TENABLE AUDIT REPORT v5.5.0-STABLE\n" + "="*60 + "\n\n")
            for line in self._get_lines():
                f.write(line + "\n")

    def generate_pdf(self, filename):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        # Configuración de página vertical A4
        pdf = FPDF(orientation='P', unit='mm', format='A4')
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        
        # Título
        pdf.set_font("Courier", 'B', 14)
        pdf.cell(0, 10, "Tenable TVM Strategic Audit Report", ln=True, align='C')
        pdf.set_font("Courier", size=8)
        pdf.cell(0, 5, f"Generated: {self.report_date}", ln=True, align='C')
        pdf.ln(5)
        
        # Renderizado línea por línea para asegurar saltos de página automáticos
        pdf.set_font("Courier", size=9)
        for line in self._get_lines():
            # Limpieza de caracteres para compatibilidad con PDF Estándar
            clean_line = line.encode('latin-1', 'replace').decode('latin-1')
            # ln=True fuerza el salto de línea tras cada celda
            pdf.cell(0, 5, clean_line, ln=True)
            
        pdf.output(filename)
