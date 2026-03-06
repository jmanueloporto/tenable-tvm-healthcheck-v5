"""
PROJECT: [V5-Tenable Health Check API Automation]
VERSION: 5.0.6
LAYER: Business / Modules
DESCRIPTION: Generates findings for Domain 3 (Risk Prioritization & Analysis).
AUTHOR: Senior Software Architect
"""

from core.models import Finding
from typing import List, Dict, Any

def run_audit(master_data: Dict[str, Any]) -> List[Finding]:
    """
    Analyzes vulnerability risk, prioritization adoption (VPR), and recurrence.
    """
    all_findings: List[Finding] = []
    domain_id = 3
    source_tag = "api"

    try:
        vulns = master_data.get("vulns_raw", [])
        assets = master_data.get("assets_raw", [])
        
        # Validación de datos: Si no hay vulnerabilidades, no podemos auditar riesgo
        if not isinstance(vulns, list) or len(vulns) == 0:
            return [Finding(
                title="Insufficient Data for Risk Analysis",
                domain=domain_id, source=source_tag,
                metrics={"vulns_count": 0},
                score=1.0, confidence="High",
                recommendations=["Ensure Step 5 of Data Collector (Vuln Export) is working"]
            )]

        total_vulns = len(vulns)
        total_assets = len(assets) if isinstance(assets, list) and len(assets) > 0 else 1

        # --- Finding 3.1: Vulnerability Density ---
        density = total_vulns / total_assets
        if density > 50:
            score_density = 1.0 if density > 100 else 2.0
            all_findings.append(Finding(
                title="High Vulnerability Density per Asset",
                domain=domain_id, source=source_tag,
                metrics={"density": round(density, 2), "total_vulns": total_vulns},
                score=score_density, confidence="High",
                recommendations=["Focus on golden image hardening", "Implement automated patch management"]
            ))

        # --- Finding 3.2: VPR Adoption (Tenable Risk-Based Approach) ---
        # Analizamos una muestra para ver si el scoring VPR es diferente al CVSS base
        vpr_present = any("vpr_score" in v for v in vulns[:500]) # Muestra de 500
        if not vpr_present:
            all_findings.append(Finding(
                title="Low Adoption of Risk-Based Prioritization (VPR)",
                domain=domain_id, source=source_tag,
                metrics={"vpr_field_missing": True},
                score=3.0, confidence="Medium",
                recommendations=["Enable Tenable VPR scoring", "Prioritize assets using VPR > 9.0 instead of CVSS 10"]
            ))

        # --- Finding 3.3: Vulnerability Recurrence (Reopened Rate) ---
        reopened = [v for v in vulns if v.get("state") == "reopened"]
        reopened_rate = (len(reopened) / total_vulns) * 100 if total_vulns > 0 else 0
        
        if reopened_rate > 15:
            all_findings.append(Finding(
                title="High Vulnerability Recurrence Rate",
                domain=domain_id, source=source_tag,
                metrics={"reopened_rate": f"{round(reopened_rate, 2)}%"},
                score=2.0, confidence="High",
                recommendations=["Audit configuration management process", "Check for baseline regression in deployments"]
            ))

    except Exception as e:
        all_findings.append(Finding(
            title="Critical Module Failure: Domain 3",
            domain=domain_id, source="system",
            metrics={"exception": str(e)},
            score=1.0, confidence="High",
            recommendations=["Verify API Export JSON structure for vulnerabilities"]
        ))

    return all_findings
