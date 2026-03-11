"""
PROJECT: [V5-Tenable Health Check API Automation]
VERSION: 5.1.3
LAYER: Orchestration
DESCRIPTION: Orchestrator V5.1.3 - PHASE 2 (Contextual Override & Reporting).
AUTHOR: Senior Software Architect
"""
import time
from core import connection, data_collector, scoring, context_loader
from modules import domain1_assets, domain2_scans, domain3_risks, domain4_remediation, domain5_6_proxy
from reports import export_engine

def main():
    start_time = time.time()
    print("="*60)
    print("               V5-TENABLE HEALTH CHECK SYSTEM               ")
    print("      Orchestrator V5.1.3 - PHASE 2 (Forensic SLA)          ")
    print("="*60)

    # Contexto Estratégico (v5.1.0)
    context = context_loader.load_context()
    context_loader.display_context_info(context)

    # Recolección Silenciosa (v5.0.16)
    conn = connection.TenableConnection()
    collector = data_collector.TenableDataCollector(conn)
    master_data = collector.collect_all()
    master_data['context'] = context

    # Auditoría de Dominios (v5.1.2)
    print("[*] Executing Strategic Audit Modules...")
    all_findings = []
    all_findings.extend(domain1_assets.run_audit(master_data))
    all_findings.extend(domain2_scans.run_audit(master_data))
    all_findings.extend(domain3_risks.run_audit(master_data))
    all_findings.extend(domain4_remediation.run_audit(master_data))
    all_findings.extend(domain5_6_proxy.run_audit(master_data))

    # Scoring Contextual y Reportes (v5.1.3)
    scores, global_score = scoring.calculate_maturity(all_findings, context)
    exec_time = time.time() - start_time
    
    export_engine.generate_reports(all_findings, scores, global_score, exec_time)
    print(f"\n[DONE] Execution completed in {exec_time:.2f} seconds.")

if __name__ == "__main__":
    main()
