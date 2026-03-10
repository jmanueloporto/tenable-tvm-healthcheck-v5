"""
PROJECT: [V5-Tenable Health Check API Automation]
VERSION: 5.1.1
LAYER: Orchestration
DESCRIPTION: Main entry point. Shadow IT Engine Integration.
AUTHOR: Senior Software Architect
"""
import time
from core import connection, data_collector, scoring, context_loader
from modules import domain1_assets, domain2_scans, domain3_risks, domain4_remediation, domain5_6_proxy
from reports import export_engine

def main():
    print("="*60)
    print("               V5-TENABLE HEALTH CHECK SYSTEM               ")
    print("           Orchestrator V5.1.1 - PHASE 2 (Shadow IT Engine) ")
    print("="*60)

    # 1. Carga de contexto estratégico
    context = context_loader.load_context()
    context_loader.display_context_info(context)

    # 2. Conexión y recolección
    conn = connection.TenableConnection()
    collector = data_collector.TenableDataCollector(conn)
    master_data = collector.collect_all()
    master_data['context'] = context

    # 3. Auditoría de Dominios
    print("[*] Executing Strategic Audit Modules...")
    all_findings = []
    modules = [domain1_assets, domain2_scans, domain3_risks, domain4_remediation, domain5_6_proxy]
    
    for mod in modules:
        try:
            findings = mod.run_audit(master_data)
            if findings:
                all_findings.extend(findings)
        except Exception as e:
            print(f"[ERROR] Fail in {mod.__name__}: {e}")

    # 4. Scoring y Reporte
    final_scores = scoring.calculate_maturity(all_findings)
    export_engine.generate_reports(all_findings, final_scores)

    print("\n[DONE] Shadow IT Audit v5.1.1 completed successfully.")

if __name__ == "__main__":
    main()
