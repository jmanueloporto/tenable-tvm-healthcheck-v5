""" VERSION: 5.4.2 | STATUS: STABLE - PURE API ARCHITECTURE & MTTR ENGINE """
import os, datetime
from core import connection, data_collector
from modules import domain4_remediation, report_generator

def main():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
    report_dir = "reports/reports"
    txt_file = os.path.join(report_dir, f"Audit_Report_{timestamp}.txt")
    pdf_file = os.path.join(report_dir, f"Audit_Report_{timestamp}.pdf")
    
    os.makedirs(report_dir, exist_ok=True)

    conn = connection.TenableConnection()
    collector = data_collector.TenableDataCollector(conn)
    master_data = collector.collect_all()
    
    # Domain 4 logic
    dom4 = domain4_remediation.RemediationAuditor(master_data)
    master_data['findings'] = dom4.run_audit()
    
    # Reporting
    reporter = report_generator.ReportGenerator(master_data)
    reporter.generate_txt(txt_file)
    reporter.generate_pdf(pdf_file)
    
    print(f"\n[DONE] Audit completed. Check {report_dir}")

if __name__ == "__main__":
    main()
