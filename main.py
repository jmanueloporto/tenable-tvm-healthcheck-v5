"""
PROJECT: [V5-Tenable Health Check API Automation]
VERSION: 5.0.6
LAYER: Orchestration
DESCRIPTION: Orchestrator integrating Domain 4 (Remediation). 
             Strict adherence to REST API and official Domain Naming.
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

def main():
    print("="*60)
    print(f"{'V5-TENABLE HEALTH CHECK SYSTEM':^60}")
    print(f"{'Orchestrator V5.0.6 - Remediation & Response':^60}")
    print("="*60)

    try:
        start_time = time.time()
        
        # --- PASO 1: Setup ---
        print("[*] Initializing Core Architecture...")
        conn = TenableConnection()
        collector = TenableDataCollector(conn)
        scoring_engine = ScoringEngine()
        
        all_findings = []

        # --- PASO 2: Data Collection ---
        master_raw_data = collector.collect_all()

        # --- PASO 3: Module Execution ---
        print("[*] Executing Audit Modules...")
        
        print(" [D1] Auditing Asset Visibility & Inventory...")
        all_findings.extend(run_domain1(master_raw_data))

        print(" [D2] Auditing Scanning Operations & Data Quality...")
        all_findings.extend(run_domain2(master_raw_data))

        print(" [D3] Auditing Risk Prioritization & Analysis...")
        all_findings.extend(run_domain3(master_raw_data))

        print(" [D4] Auditing Remediation & Response...")
        all_findings.extend(run_domain4(master_raw_data))

        # --- PASO 4: Scoring Engine ---
        print("[*] Calculating Platform Maturity Metrics...")
        domain_scores = scoring_engine.calculate_domain_scores(all_findings)
        overall_score = scoring_engine.calculate_overall_score(domain_scores)

        # --- PASO 5: Presentation ---
        print("\n" + "-"*60)
        print(f"{'OFFICIAL MATURITY ASSESSMENT (v5.0.6)':^60}")
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
            
            if d_score >= 4.0: status = "HEALTHY "
            elif d_score >= 2.5: status = "WARNING "
            else: status = "CRITICAL"
            
            print(f" > {name:<40}: {d_score:^5.2f}/5.0 [{status}]")
            
        print("-" * 60)
        print(f" PLATFORM MATURITY SCORE: {overall_score:^5.2f}/5.0")
        print("-" * 60)
        
        exec_time = round(time.time() - start_time, 2)
        print(f"\n[SUCCESS] Health Check completed in {exec_time}s.")
        print("="*60)

    except Exception as e:
        print(f"\n[!] CRITICAL ORCHESTRATION ERROR: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
