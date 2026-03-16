# VERSION: 5.3.3-FINAL
"""
PROJECT: [V5-Tenable Health Check API Automation]
VERSION: 5.3.3
LAYER: Business / Modules
DESCRIPTION: Generates findings for Domain 4 (Remediation & Response).
             Analyzes MTTR, Fix Rates, and Effort Alignment.
AUTHOR: Senior Software Architect
"""

from core.models import Finding
from typing import List, Dict, Any
from datetime import datetime

def run_audit(master_data: Dict[str, Any]) -> List[Finding]:
    """
    Evaluates remediation velocity, coverage, and risk-based prioritization.
    """
    all_findings: List[Finding] = []
    domain_id = 4
    source_tag = "api"

    try:
        vulns = master_data.get("vulns_raw", [])
        if not isinstance(vulns, list) or not vulns:
            return []

        # Categorización de datos para análisis
        fixed_vulns = [v for v in vulns if v.get("state") == "fixed"]
        open_vulns = [v for v in vulns if v.get("state") in ["open", "reopened"]]
        
        # --- Finding 4.1: Remediation Velocity (MTTR) ---
        ttr_days = []
        for v in [fv for fv in fixed_vulns if fv.get("severity") == "critical"]:
            try:
                # Conversión de timestamps ISO a objetos datetime
                first = datetime.fromisoformat(v['first_found'].replace('Z', '+00:00'))
                last = datetime.fromisoformat(v['last_fixed'].replace('Z', '+00:00'))
                ttr_days.append((last - first).days)
            except (KeyError, ValueError):
                continue

        if ttr_days:
            avg_ttr = sum(ttr_days) / len(ttr_days)
            if avg_ttr > 30:
                score = 1.0 if avg_ttr > 60 else 2.0
                all_findings.append(Finding(
                    title="Remediation SLA Breach (MTTR)",
                    domain=domain_id, source=source_tag,
                    metrics={"avg_ttr_critical_days": round(avg_ttr, 1)},
                    score=score, confidence="High",
                    recommendations=[f"Reduce Critical MTTR to < 30 days. Current: {round(avg_ttr, 1)}"]
                ))

        # --- Finding 4.2: Remediation Coverage (Fix Rate) ---
        crit_total = len([v for v in vulns if v.get("severity") == "critical"])
        crit_fixed = len([v for v in fixed_vulns if v.get("severity") == "critical"])
        high_total = len([v for v in vulns if v.get("severity") == "high"])
        high_fixed = len([v for v in fixed_vulns if v.get("severity") == "high"])

        fix_rate_crit = (crit_fixed / crit_total * 100) if crit_total > 0 else 100
        fix_rate_high = (high_fixed / high_total * 100) if high_total > 0 else 100

        if fix_rate_crit < 70 or fix_rate_high < 50:
            all_findings.append(Finding(
                title="Low Remediation Coverage",
                domain=domain_id, source=source_tag,
                metrics={"crit_fix_rate": f"{round(fix_rate_crit,1)}%", "high_fix_rate": f"{round(fix_rate_high,1)}%"},
                score=2.0, confidence="High",
                recommendations=["Focus patching efforts on Critical/High backlogs"]
            ))

        # --- Finding 4.3: Effort Misalignment (VPR vs Fix) ---
        low_vpr_fixed = len([v for v in fixed_vulns if float(v.get("vpr_score", 0) or 0) < 4.0])
        high_vpr_fixed = len([v for v in fixed_vulns if float(v.get("vpr_score", 0) or 0) >= 7.0])

        if low_vpr_fixed > high_vpr_fixed and high_vpr_fixed > 0:
            all_findings.append(Finding(
                title="Inefficient Remediation Prioritization",
                domain=domain_id, source=source_tag,
                metrics={"low_vpr_fixed": low_vpr_fixed, "high_vpr_fixed": high_vpr_fixed},
                score=2.0, confidence="Medium",
                recommendations=["Redirect patching teams to address High VPR vulnerabilities first"]
            ))

    except Exception as e:
        # Resiliencia Estricta v5.0.6
        all_findings.append(Finding(
            title="Module 4 Error",
            domain=domain_id, source="system",
            metrics={"exception": str(e)},
            score=1.0, confidence="High",
            recommendations=["Review API data structure and date formats in domain4_remediation.py"]
        ))

    return all_findings
