"""
PROJECT: [V5-Tenable Health Check API Automation]
VERSION: 5.0.19
LAYER: Orchestration
DESCRIPTION: Orchestrator with Forensic Reporting (TXT/PDF).
AUTHOR: Senior Software Architect
"""

import sys
import time
from core.connection import TenableConnection
from core.data_collector import TenableDataCollector
from core.scoring import ScoringEngine
from modules.domain1_assets import run_audit as run_domain1
from modules.domain2_scans import run_audit as run_domain2
from modules.domain3_risks import run_audit as run_domain3
from modules.domain4_remediation import run_audit as run_domain4
from modules.domain5_6_proxy import run_audit as run_domain56
from reports.export_engine import ReportGenerator

def main():
    print("="*60)
    print(f"{'V5-TENABLE HEALTH CHECK SYSTEM':^60}")
    print(f"{'Orchestrator V5.0.11 - Phase 1 Finalized':^60}")
    print("="*60)

    try:
        start_time = time.time()
        conn = TenableConnection()
        collector = TenableDataCollector(conn)
        scoring_engine = ScoringEngine()
        
        # --- PASO 1: Recolección de Datos ---
        master_raw_data = collector.collect_all()

        # --- PASO 2: Ejecución de Auditoría ---
        print("[*] Executing Advanced Audit Modules...")
        all_findings = []
        all_findings.extend(run_domain1(master_raw_data))
        all_findings.extend(run_domain2(master_raw_data))
        all_findings.extend(run_domain3(master_raw_data))
        all_findings.extend(run_domain4(master_raw_data))
        all_findings.extend(run_domain56(master_raw_data))
        
        # --- PASO 3: Scoring ---
        domain_scores = scoring_engine.calculate_domain_scores(all_findings)
        overall_score = scoring_engine.calculate_overall_score(domain_scores)

        # --- PASO 4: Presentación en Consola ---
        print("\n" + "-"*60)
        print(f"{'OFFICIAL MATURITY ASSESSMENT (v5.0.11)':^60}")
        print("-" * 60)
        
        dom_names = {
            1: "Asset Visibility & Inventory", 
            2: "Scanning Operations & Data Quality", 
            3: "Risk Prioritization & Analysis", 
            4: "Remediation & Response", 
            5: "Program Governance & Operations", 
            6: "Ecosystem Integration & Security Posture"
        }

        for d_id in sorted(dom_names.keys()):
            name = dom_names[d_id]
            d_score = domain_scores.get(d_id, 5.0)
            status = "HEALTHY " if d_score >= 4.0 else "WARNING " if d_score >= 2.5 else "CRITICAL"
            print(f" > {name:<42}: {d_score:^5.2f}/5.0 [{status}]")
            
        print("-" * 60)
        print(f" FINAL PLATFORM MATURITY SCORE: {overall_score:^5.2f}/5.0")
        print("-" * 60)

        # --- PASO 5: Generación de Reportes de Archivo ---
        print("[*] Launching Forensic Reporting Engine...")
        reporter = ReportGenerator(overall_score, domain_scores, all_findings)
        reporter.generate_txt()
        reporter.generate_pdf()

        exec_time = round(time.time() - start_time, 2)
        print(f"\n[SUCCESS] Health Check and Reports saved (Time: {exec_time}s).")
        print("="*60)

    except Exception as e:
        print(f"\n[!] CRITICAL ERROR: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
