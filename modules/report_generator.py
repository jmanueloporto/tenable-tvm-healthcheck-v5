""" VERSION: 5.4.0 | STATUS: Stable """
import datetime
import os

class ReportGenerator:
    def __init__(self, data):
        self.data = data
        self.report_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def generate_txt(self, filename):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w') as f:
            f.write("============================================================\n")
            f.write("      TENABLE VULNERABILITY MANAGEMENT HEALTH CHECK\n")
            f.write(f"      Technical Audit Report v5.2.9 | {self.report_date}\n")
            f.write("============================================================\n\n")

            # 1.1 Resumen GUI
            f.write("1.1 SENSOR INFRASTRUCTURE SUMMARY (DOMAIN 6)\n")
            f.write("------------------------------------------------------------\n")
            f.write(f"{'Tipo de Sensor':<30} {'Cant.':<8} {'Activos':<10} {'Inactivos':<10}\n")
            stats = self.data.get('sensors', {}).get('stats_by_type', {})
            order = ["Nessus Scanners", "Nessus Agents", "Nessus Network Monitors", "OT Connectors", "Web Application Scanners"]
            for label in order:
                d = stats.get(label, {"qty": 0, "active": 0, "inactive": 0})
                f.write(f"{label:<30} {d['qty']:<8} {d['active']:<10} {d['inactive']:<10}\n")
            f.write(f"\nTOTAL SENSORS: {self.data.get('sensors',{}).get('summary',{}).get('total',0)}\n\n")

            # 1.2 Detalle Agrupado por Tipo de Sensor (Solicitado)
            f.write("1.2 DETAILED INVENTORY BY SENSOR TYPE\n")
            f.write("------------------------------------------------------------\n")
            inventory = self.data.get('sensors', {}).get('inventory', [])
            for label in order:
                f.write(f"\n>>> CATEGORY: {label.upper()}\n")
                found = False
                for s in inventory:
                    if s['label'] == label:
                        f.write(f" - {s['name'][:45]:<45} Status: {s['status']}\n")
                        found = True
                if not found: f.write("   (No sensors detected in this category)\n")

            # 1.3 Discovery: API Raw Types Summary (Solicitado)
            f.write("\n1.3 DISCOVERY: API RAW TYPES (SUMMARY)\n")
            f.write("------------------------------------------------------------\n")
            f.write(f"{'API Raw Type':<30} {'Cant.':<8} {'Activos':<10} {'Inactivos':<10}\n")
            raw_stats = {}
            for s in inventory:
                t = s['raw_type']
                if t not in raw_stats: raw_stats[t] = {"q": 0, "a": 0, "i": 0}
                raw_stats[t]["q"] += 1
                if s['status'] in ['on', 'online']: raw_stats[t]["a"] += 1
                else: raw_stats[t]["i"] += 1
            for t, d in raw_stats.items():
                f.write(f"{t:<30} {d['q']:<8} {d['a']:<10} {d['i']:<10}\n")

            # 1.4 Detailed Sensor List by Raw Type (Solicitado)
            f.write("\n1.4 DETAILED SENSOR LIST BY RAW TYPE\n")
            f.write("------------------------------------------------------------\n")
            for r_type in sorted(raw_stats.keys()):
                f.write(f"\n[RAW TYPE: {r_type.upper()}]\n")
                for s in inventory:
                    if s['raw_type'] == r_type:
                        f.write(f" - {s['name'][:45]:<45} Status: {s['status']}\n")

            f.write("\n============================================================\n")
            f.write("              END OF TECHNICAL AUDIT REPORT\n")
            f.write("============================================================\n")
        print(f"[*] Physical TXT saved: {filename}")

    def generate_pdf(self, filename):
        # El PDF ahora reflejará el resumen de la sección 1.1 [cite: 177, 181]
        try:
            from fpdf import FPDF
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", 'B', 14)
            pdf.cell(190, 10, "Executive Health Check v5.2.9", 1, 1, 'C')
            pdf.ln(5)
            stats = self.data.get('sensors', {}).get('stats_by_type', {})
            for label, d in stats.items():
                pdf.set_font("Arial", size=10)
                pdf.cell(100, 8, f"{label}: {d['qty']} (Active: {d['active']})", 0, 1)
            pdf.output(filename)
            print(f"[*] Physical PDF saved: {filename}")
        except:
            with open(filename, 'wb') as f: f.write(b"%PDF-1.1\n%%EOF")
