# VERSION: 5.3.3-FINAL
"""
PROJECT: [V5-Tenable Health Check API Automation]
VERSION: 5.3.3
LAYER: Orchestration
DESCRIPTION: Main entry point. Fixed import for domain3_risk.
"""
import time
from core import connection, data_collector, scoring, context_loader
from modules import domain1_assets, domain2_scans, domain3_risk, domain4_remediation, domain5_6_proxy
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

    # 3. Auditoría de Dominios (Importación corregida)
    print("[*] Executing Strategic Audit Modules...")
    all_findings = []
    modules = [domain1_assets, domain2_scans, domain3_risk, domain4_remediation, domain5_6_proxy]
    
    for mod in modules:
        try:
            findings = mod.run_audit(master_data)
            if findings:
                all_findings.extend(findings)
        except Exception as e:
            print(f"[ERROR] Fail in {mod.__name__}: {e}")

    # 4. Scoring y Reporte
    domain_scores, global_score = scoring.calculate_maturity(all_findings, context)
    export_engine.generate_reports(all_findings, domain_scores)

    print(f"\n[DONE] Audit v5.1.1 completed successfully. Global Score: {global_score:.2f}")

if __name__ == "__main__":
    main()
