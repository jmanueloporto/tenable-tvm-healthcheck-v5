"""
PROJECT: [V5-Tenable Health Check API Automation]
VERSION: 5.0.7
LAYER: Business / Modules
DESCRIPTION: Generates findings for Domain 2 (Scanning Operations & Data Quality).
AUTHOR: Senior Software Architect
"""

from core.models import Finding
from typing import List, Dict, Any

def run_audit(master_data: Dict[str, Any]) -> List[Finding]:
    """
    Analyzes master_data to assess Scanning Operations health and Data Quality.
    Evaluates: Scan Success, Authentication Coverage, Policies, and Exclusions.
    """
    all_findings: List[Finding] = []
    domain_id = 2
    source_tag = "api"

    try:
        # --- Finding 2.1: Scan Execution Health ---
        scans_data = master_data.get("scans", {})
        if isinstance(scans_data, dict):
            scans_list = scans_data.get("scans", [])
            # Identificamos escaneos que no terminaron en 'completed' (ej. 'canceled', 'failed')
            abnormal_scans = [s for s in scans_list if s.get("status") not in ["completed", "imported"]]
            
            if abnormal_scans:
                all_findings.append(Finding(
                    title="Incomplete Scan Executions",
                    domain=domain_id,
                    source=source_tag,
                    metrics={"total_scans": len(scans_list), "abnormal_count": len(abnormal_scans)},
                    score=2.5,
                    confidence="High",
                    recommendations=["Investigate scans in 'canceled' or 'failed' status", "Check scanner capacity"]
                ))
        
        # --- Finding 2.2: Scan Policy Optimization ---
        policies = master_data.get("policies", [])
        if isinstance(policies, list):
            # Si hay demasiadas políticas (ej. > 50), suele indicar falta de estandarización
            if len(policies) > 50:
                all_findings.append(Finding(
                    title="Scan Policy Proliferation",
                    domain=domain_id,
                    source=source_tag,
                    metrics={"policy_count": len(policies)},
                    score=3.0,
                    confidence="Medium",
                    recommendations=["Consolidate scan policies using the 'Advanced Network Scan' template"]
                ))

        # --- Finding 2.3: Data Quality (Authentication Coverage) ---
        # Analizamos assets_raw para ver el 'auth_effort' o 'authentication_success'
        assets = master_data.get("assets_raw", [])
        if isinstance(assets, list) and len(assets) > 0:
            # Simulamos análisis: si no hay evidencia de auth, bajamos score
            unauthenticated_assets = [a for a in assets if not a.get("auth_success", True)]
            if unauthenticated_assets:
                all_findings.append(Finding(
                    title="Low Credentialed Scan Coverage",
                    domain=domain_id,
                    source=source_tag,
                    metrics={"total_assets": len(assets), "unauth_count": len(unauthenticated_assets)},
                    score=2.0,
                    confidence="High",
                    recommendations=["Deploy credentials for authenticated scanning", "Review scan credentials logs"]
                ))

        # --- Finding 2.4: Global Exclusions ---
        exclusions = master_data.get("exclusions", [])
        if isinstance(exclusions, list) and len(exclusions) > 10:
             all_findings.append(Finding(
                title="Excessive Scan Exclusions",
                domain=domain_id,
                source=source_tag,
                metrics={"exclusion_count": len(exclusions)},
                score=3.0,
                confidence="Medium",
                recommendations=["Review global exclusions to ensure no critical assets are being skipped"]
            ))

    except Exception as e:
        all_findings.append(Finding(
            title="Module Error: Domain 2 (Scans)",
            domain=domain_id,
            source="system",
            metrics={"exception": str(e)},
            score=1.0,
            confidence="High",
            recommendations=["Verify core/data_collector.py Paso 3 data structure"]
        ))

    return all_findings
