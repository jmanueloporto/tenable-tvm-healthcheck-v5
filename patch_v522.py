""" VERSION: 5.4.0 | STATUS: Stable """
# VERSION: 5.3.4-FINAL
import os
import json

def apply_patch():
    print("[*] Iniciando aplicación de Parche v5.2.2 - Forensic & Context Restoration...")

    # --- TAREA 1: RESTAURAR CONTEXTO ESTRATÉGICO REAL ---
    # Se asegura que los valores estén envueltos en la llave raíz "context"
    context_path = 'data/context_input.json'
    os.makedirs('data', exist_ok=True)
    context_data = {
        "context": {
            "expected_assets": 100,
            "internal_sla_critical": 15,
            "maintenance_windows": True
        }
    }
    with open(context_path, 'w', encoding='utf-8') as f:
        json.dump(context_data, f, indent=4)
    print(f"[OK] Contexto estratégico restaurado en {context_path}")

    # --- TAREA 2: NUEVO MOTOR DE EXPORTACIÓN FORENSE (v5.2.2) ---
    export_engine_code = """
import os
import json
from datetime import datetime
from fpdf import FPDF
from typing import List, Dict
from core.models import Finding

def generate_reports(findings: List[Finding], scores: Dict[int, float], global_score: float, exec_time: float):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    report_dir = "reports/reports"
    os.makedirs(report_dir, exist_ok=True)
    base_filename = f"{report_dir}/Audit_Report_{timestamp}"
    
    domain_map = {
        1: "Asset Visibility (Shadow IT)",
        2: "Scanning Operations",
        3: "Risk Prioritization",
        4: "Remediation & SLA",
        5: "Identity Hygiene",
        6: "Ecosystem & Governance"
    }

    # 1. Dashboard JSON (latest_results.json)
    dashboard_data = {
        "timestamp": datetime.now().isoformat(),
        "execution_time": round(exec_time, 2),
        "global_score": round(global_score, 2),
        "domain_scores": scores,
        "findings": [
            {
                "title": f.title,
                "domain": f.domain,
                "domain_name": domain_map.get(f.domain, "Unknown"),
                "score": f.override_score if f.override_score is not None else f.score,
                "observation": f.observation,
                "recommendations": f.recommendations
            } for f in findings
        ]
    }
    with open("reports/latest_results.json", "w", encoding='utf-8') as jf:
        json.dump(dashboard_data, jf, indent=4)

    # 2. TXT Forense Detallado
    with open(f"{base_filename}.txt", "w", encoding='utf-8') as f:
        f.write("="*70 + "\\n")
        f.write(f"{'DETAILED MATURITY AUDIT REPORT (v5.2.2)':^70}\\n")
        f.write(f"{'Generated: ' + timestamp:^70}\\n")
        f.write("="*70 + "\\n\\n")
        f.write(f"GLOBAL MATURITY SCORE  : {global_score:.2f} / 5.0\\n")
        f.write(f"EXECUTION TIME         : {exec_time:.2f}s\\n\\n")
        
        f.write("[I] DOMAIN SUMMARY\\n" + "-"*30 + "\\n")
        for d_id, score in scores.items():
            f.write(f" > Domain {d_id} - {domain_map[d_id]:<35}: {score:.2f}/5.0\\n")
        
        f.write("\\n[II] DETAILED EVIDENCE & FINDINGS\\n" + "-"*30 + "\\n")
        for idx, issue in enumerate(findings, 1):
            f.write(f"Finding #{idx}: {issue.title}\\n")
            f.write(f" Domain      : {domain_map.get(issue.domain, 'Unknown')}\\n")
            impact = issue.override_score if issue.override_score is not None else issue.score
            f.write(f" Impact Score: {impact:.1f}\\n")
            f.write(f" Observation : {issue.observation}\\n")
            f.write(" Recommendations:\\n")
            for rec in issue.recommendations:
                f.write(f"   * {rec}\\n")
            f.write("-" * 40 + "\\n")

    # 3. PDF Ejecutivo (Estilo Dashboard)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_fill_color(230, 230, 230)
    
    # Header
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(190, 15, 'TENABLE HEALTH CHECK - EXECUTIVE DASHBOARD', 1, 1, 'C', True)
    pdf.ln(5)
    
    # KPI Cells
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(95, 10, f"Global Maturity: {global_score:.2f} / 5.0", 1, 0, 'C')
    pdf.cell(95, 10, f"Execution Time: {exec_time:.2f}s", 1, 1, 'C')
    pdf.ln(10)
    
    # Domain Table
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(150, 10, "Domain Maturity Summary", 1, 0, 'L', True)
    pdf.cell(40, 10, "Score", 1, 1, 'C', True)
    pdf.set_font("Arial", '', 10)
    for d_id, s in scores.items():
        pdf.cell(150, 8, f" {domain_map[d_id]}", 1, 0, 'L')
        pdf.cell(40, 8, f"{s:.2f}/5.0", 1, 1, 'C')
    
    # Critical Alerts Section
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    pdf.set_text_color(200, 0, 0)
    pdf.cell(190, 10, "CRITICAL FINDINGS & ALERTS (Score >= 2.0)", 0, 1, 'L')
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", '', 9)
    for issue in findings:
        impact = issue.override_score if issue.override_score is not None else issue.score
        if impact >= 2.0:
            pdf.set_font("Arial", 'B', 10)
            pdf.multi_cell(190, 7, f"ALERTA: {issue.title}", 'T', 'L')
            pdf.set_font("Arial", '', 9)
            pdf.multi_cell(190, 5, f"Observacion: {issue.observation}", 0, 'L')
            pdf.ln(2)

    pdf.output(f"{base_filename}.pdf")
"""
    with open('reports/export_engine.py', 'w', encoding='utf-8') as f:
        f.write(export_engine_code.strip())
    print("[OK] Motor de exportación v5.2.2 reconstruido.")

    # --- TAREA 3: RESTAURAR ORQUESTRADOR PRINCIPAL (v5.2.2) ---
    main_code = """
import time
from core import connection, data_collector, scoring, context_loader
from modules import domain1_assets, domain2_scans, domain3_risks, domain4_remediation, domain5_6_proxy
from reports import export_engine

def main():
    start_time = time.time()
    print("="*60)
    print("               V5-TENABLE HEALTH CHECK SYSTEM               ")
    print("      Orchestrator V5.2.2 - PHASE 3 (Forensic Restored)     ")
    print("="*60)

    # Load Context
    context = context_loader.load_context()
    context_loader.display_context_info(context)

    # Connection & Collection
    conn = connection.TenableConnection()
    collector = data_collector.TenableDataCollector(conn)
    master_data = collector.collect_all()
    master_data['context'] = context

    # Audit Modules
    print("[*] Executing Strategic Audit Modules...")
    all_findings = []
    all_findings.extend(domain1_assets.run_audit(master_data))
    all_findings.extend(domain2_scans.run_audit(master_data))
    all_findings.extend(domain3_risks.run_audit(master_data))
    all_findings.extend(domain4_remediation.run_audit(master_data))
    all_findings.extend(domain5_6_proxy.run_audit(master_data))

    # Scoring & Reports
    scores, global_score = scoring.calculate_maturity(all_findings, context)
    exec_time = time.time() - start_time
    
    export_engine.generate_reports(all_findings, scores, global_score, exec_time)
    print(f"\\n[DONE] Strategic Audit v5.2.2 Completed in {exec_time:.2f}s.")

if __name__ == '__main__':
    main()
"""
    with open('main.py', 'w', encoding='utf-8') as f:
        f.write(main_code.strip())
    print("[OK] Orchestrator main.py actualizado a v5.2.2.")

    print("\\n[SUCCESS] Parche aplicado. Ejecutando auditoría de validación...")
    os.system('/home/adminu/mpiv/tenable-tvm-healthcheck-v5/.venv/bin/python main.py')

if __name__ == "__main__":
    apply_patch()
