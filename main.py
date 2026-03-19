""" VERSION: 5.4.2 | STATUS: STABLE - PURE API """ VERSION: 5.4.2 | STATUS: STABLE - PURE API """ VERSION: 5.4.2 | STATUS: STABLE - PURE API """ VERSION: 5.4.2 | STATUS: STABLE - PURE API """ VERSION: 5.4.2 | STATUS: STABLE - PURE API """ VERSION: 5.4.2 | STATUS: STABLE - PURE API """ VERSION: 5.4.0 | STATUS: Stable """ MTTR ENGINE """ MTTR ENGINE """ MTTR ENGINE """ MTTR ENGINE """ MTTR ENGINE """ MTTR ENGINE """
import os
import datetime
from core import connection, data_collector
from modules import domain4_remediation
from modules import report_generator

def main():
    print("[*] Starting Phase 1: Silent Collection (v5.4.0-PURE_API)...")
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
    report_dir = "reports/reports"
    txt_file = os.path.join(report_dir, f"Audit_Report_{timestamp}.txt")
    pdf_file = os.path.join(report_dir, f"Audit_Report_{timestamp}.pdf")
    
    os.makedirs(report_dir, exist_ok=True)

    # Fase 1: Recoleccion
    conn = connection.TenableConnection()
    collector = data_collector.TenableDataCollector(conn)
    master_data = collector.collect_all()
    
    # Inyectar configuracion default para SLA (30 dias) si no existe
    if 'config' not in master_data:
        master_data['config'] = {'internal_sla_critical': 30}
    
    print("\n[*] Starting Phase 2: Logical Audit Engines...")
    findings = []
    
    # Ejecutar Dominio 4 (Remediacion y MTTR)
    print(" [>] Running Domain 4: SLA & MTTR Engine...")
    dom4_auditor = domain4_remediation.RemediationAuditor(master_data)
    dom4_findings = dom4_auditor.run_audit()
    findings.extend(dom4_findings)
    
    # Adjuntar los hallazgos al master_data para que el reporte los vea
    master_data['findings'] = findings
    
    print("\n[*] Starting Phase 3: Reporting...")
    reporter = report_generator.ReportGenerator(master_data)
    reporter.generate_txt(txt_file)
    reporter.generate_pdf(pdf_file)
    
    print(f"\n[DONE] Audit v5.4.0 completed. Check {report_dir}")

if __name__ == "__main__":
    main()
