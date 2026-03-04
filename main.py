"""
PROJECT: [V5-Tenable Health Check API Automation]
VERSION: 5.0.0
LAYER: Orchestration
DESCRIPTION: The 'Dumb Orchestrator'. Coordinates real data collection, Domain 1 & Domain 2 audit, and scoring.
AUTHOR: Senior Software Architect
"""

import sys
import time
from core.connection import TenableConnection
from core.data_collector import TenableDataCollector
from core.scoring import ScoringEngine
from core.models import Finding
from modules.domain1_assets import run_audit as run_domain1
from modules.domain2_scans import run_audit as run_domain2

def main():
    print("="*60)
    print(f"{'V5-TENABLE HEALTH CHECK SYSTEM':^60}")
    print(f"{'Orchestrator V5.0.0 - Production':^60}")
    print("="*60)

    try:
        # --- PASO 1: Setup & Initialization ---
        start_time = time.time()
        print("[*] Initializing Core Components...")
        conn = TenableConnection()
        collector = TenableDataCollector(conn)
        scoring_engine = ScoringEngine()
        
        all_findings = []

        # --- PASO 2: Data Collection (7-Step Async) ---
        master_raw_data = collector.collect_all()

        # --- PASO 3: Module Execution ---
        print("[*] Running Audit: Domain 1 (Asset Visibility)...")
        d1_findings = run_domain1(master_raw_data)
        all_findings.extend(d1_findings)

        print("[*] Running Audit: Domain 2 (Scanning Operations)...")
        d2_findings = run_domain2(master_raw_data)
        all_findings.extend(d2_findings)
        
        # --- PASO 4: Scoring Engine ---
        print("[*] Processing Scoring Engine...")
        domain_scores = scoring_engine.calculate_domain_scores(all_findings)
        overall_score = scoring_engine.calculate_overall_score(domain_scores)

        # --- PASO 5: Presentation Layer ---
        print("\n" + "-"*60)
        print(f"{'FINAL MATURITY ASSESSMENT':^60}")
        print("-" * 60)
        
        dom_names = {
            1: "Asset Visibility", 
            2: "Scanning Ops", 
            3: "Scan Coverage", 
            4: "Compliance", 
            5: "Reporting", 
            6: "Operations"
        }

        for d_id in sorted(dom_names.keys()):
            name = dom_names[d_id]
            d_score = domain_scores.get(d_id, 5.0)
            status = "HEALTHY " if d_score >= 4.0 else "WARNING " if d_score >= 2.5 else "CRITICAL"
            print(f" > {name:<20}: {d_score:^5.2f}/5.0 [{status}]")
            
        print("-" * 60)
        print(f" PLATFORM MATURITY SCORE: {overall_score:^5.2f}/5.0")
        print("-" * 60)
        
        execution_time = round(time.time() - start_time, 2)
        print(f"\n[SUCCESS] Health Check completed in {execution_time}s.")
        print("="*60)

    except Exception as e:
        print(f"\n[!] CRITICAL SYSTEM ERROR: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
