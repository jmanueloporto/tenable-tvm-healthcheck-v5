""" VERSION: 5.5.0-STABLE | STATUS: PRODUCTION READY """
import os
from core import connection, data_collector
from modules import domain1_assets, domain4_remediation, report_generator

def main():
    conn = connection.TenableConnection()
    collector = data_collector.TenableDataCollector(conn)
    
    # Recolección
    data = collector.collect_all()
    
    # Auditoría
    print("\n[*] Auditing Domain 1: Assets & Inventory Gap...")
    data = domain1_assets.audit(data)
    
    print("[*] Auditing Domain 4: Remediation SLAs...")
    data = domain4_remediation.audit(data)
    
    # Reportes
    import json
    with open('reports/latest_results.json', 'w') as f:
        json.dump(data, f, indent=4)
        
    reporter = report_generator.ReportGenerator(data)
    pdf_file = f"reports/Audit_Report_{reporter.report_date.replace(' ', '_').replace(':', '')}.pdf"
    txt_file = pdf_file.replace('.pdf', '.txt')
    
    reporter.generate_txt(txt_file)
    reporter.generate_pdf(pdf_file)
    
    print(f"\n[DONE] Audit v5.5.0 completed. Check reports/")

if __name__ == "__main__":
    main()
