""" VERSION: 5.4.0 | STATUS: Stable """
import os
import datetime
from core import connection, data_collector
from modules import report_generator

def main():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
    report_dir = "reports/reports"
    txt_file = os.path.join(report_dir, f"Audit_Report_{timestamp}.txt")
    pdf_file = os.path.join(report_dir, f"Audit_Report_{timestamp}.pdf")
    
    os.makedirs(report_dir, exist_ok=True)

    conn = connection.TenableConnection()
    collector = data_collector.TenableDataCollector(conn)
    master_data = collector.collect_all()
    
    reporter = report_generator.ReportGenerator(master_data)
    reporter.generate_txt(txt_file)
    reporter.generate_pdf(pdf_file)
    
    print(f"\n[DONE] Audit v5.2.8 completed. Check {report_dir}")

if __name__ == "__main__":
    main()
