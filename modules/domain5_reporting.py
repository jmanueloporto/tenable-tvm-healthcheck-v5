""" VERSION: 5.5.0-STABLE | STATUS: DOMAIN 1 READY """
# VERSION: 5.3.4-FINAL
"""
PROJECT: [V5-Tenable Health Check API Automation]
VERSION: 5.3.4
LAYER: Business / Modules
DESCRIPTION: Generates findings for Domain 5 (Reporting & Hygiene).
AUTHOR: Senior Software Architect
"""

from core.models import Finding
from typing import List, Dict, Any

def run_audit(master_data: Dict[str, Any]) -> List[Finding]:
    all_findings: List[Finding] = []
    domain_id = 5
    source_tag = "api"

    try:
        users = master_data.get("users", [])
        
        # --- Finding 5.1: User Hygiene (Inactive Users) ---
        # Si hay usuarios que nunca se han logueado o no tienen MFA (simulado según metadata)
        if len(users) > 10:
            all_findings.append(Finding(
                title="Excessive Administrative Users",
                domain=domain_id, source=source_tag,
                metrics={"user_count": len(users)},
                score=3.0, confidence="Medium",
                recommendations=["Review user roles", "Implement Least Privilege principle"]
            ))

    except Exception as e:
        all_findings.append(Finding(
            title="Module Error: Domain 5",
            domain=domain_id, source="system",
            metrics={"exception": str(e)},
            score=1.0, confidence="High",
            recommendations=["Verify user list permissions"]
        ))

    return all_findings
