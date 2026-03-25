""" VERSION: 5.5.0-STABLE | STATUS: DOMAIN 1 READY """
import os, datetime, json
from core import connection, data_collector
from modules import domain1_assets, domain4_remediation, report_generator

def load_local_context():
    context_path = "data/context_input.json"
    if os.path.exists(context_path):
        with open(context_path, 'r') as f:
            return json.load(f)
    return {"context": {"expected_assets": 0}}

def main():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
    report_dir = "reports/reports"
    txt_file = os.path.join(report_dir, f"Audit_Report_{timestamp}.txt")
    pdf_file = os.path.join(report_dir, f"Audit_Report_{timestamp}.pdf")
    os.makedirs(report_dir, exist_ok=True)

    conn = connection.TenableConnection()
    collector = data_collector.TenableDataCollector(conn)
    master_data = collector.collect_all()
    
    context_data = load_local_context()
    master_data['findings'] = []

    # Ejecución de Dominios
    try:
        dom1 = domain1_assets.AssetAuditor(master_data, context_data)
        master_data['findings'].extend(dom1.run_audit())
        dom4 = domain4_remediation.RemediationAuditor(master_data)
        master_data['findings'].extend(dom4.run_audit())
    except Exception as e:
        print(f"[!] Error en dominios: {e}")

    # GUARDADO SINCRONIZADO PARA LA WEB (v5.5.0)
    with open("reports/latest_results.json", 'w') as f:
        json.dump(master_data, f, indent=4)

    reporter = report_generator.ReportGenerator(master_data)
    reporter.generate_txt(txt_file)
    reporter.generate_pdf(pdf_file)
    
    print(f"\n[DONE] Audit v5.5.0 completed. Check {report_dir}")

if __name__ == "__main__":
    main()
