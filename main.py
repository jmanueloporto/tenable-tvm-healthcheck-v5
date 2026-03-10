"""
PROJECT: [V5-Tenable Health Check API Automation]
VERSION: 5.1.0
LAYER: Orchestration
DESCRIPTION: Main entry point. Now integrates Strategic Context Engine.
AUTHOR: Senior Software Architect
"""
import time
from core import connection, data_collector, scoring, context_loader
from modules import domain1_assets, domain2_scans, domain3_risks, domain4_remediation, domain5_6_proxy
from reports import export_engine

def main():
    print("============================================================")
    print("               V5-TENABLE HEALTH CHECK SYSTEM               ")
    print("                 Orchestrator V5.1.0 - PHASE 2              ")
    print("============================================================")

    # Step 0: Load Strategic Context
    context = context_loader.load_context()
    context_loader.display_context_info(context)

    # Step 1: Connect and Collect
    conn = connection.TenableConnection()
    collector = data_collector.TenableDataCollector(conn)
    master_data = collector.collect_all()
    
    # Inject Context into Master Data for Modules
    master_data['context'] = context

    # Step 2: Audit Domains
    print("[*] Executing Strategic Audit Modules...")
    all_findings = []
    all_findings.extend(domain1_assets.run_audit(master_data))
    all_findings.extend(domain2_scans.run_audit(master_data))
    all_findings.extend(domain3_risks.run_audit(master_data))
    all_findings.extend(domain4_remediation.run_audit(master_data))
    all_findings.extend(domain5_6_proxy.run_audit(master_data))

    # Step 3: Scoring & Reporting
    final_scores = scoring.calculate_maturity(all_findings)
    export_engine.generate_reports(all_findings, final_scores)

    print("\n[SUCCESS] Phase 2 Strategic Health Check Completed.")

if __name__ == "__main__":
    main()
