# VERSION: 5.3.3-FINAL
"""
PROJECT: [V5-Tenable Health Check API Automation]
VERSION: 5.3.3
LAYER: Business / Modules
DESCRIPTION: Generates findings for Domain 4 (Compliance & Policy Adherence).
AUTHOR: Senior Software Architect
"""

from core.models import Finding
from typing import List, Dict, Any

def run_audit(master_data: Dict[str, Any]) -> List[Finding]:
    """
    Analyzes configuration audits, benchmarking and policy usage.
    """
    all_findings: List[Finding] = []
    domain_id = 4
    source_tag = "api"

    try:
        policies = master_data.get("policies", [])
        if not isinstance(policies, list):
            policies = []

        # --- Finding 4.1: Compliance Scan Adoption ---
        # Buscamos políticas que incluyan "audit" o "compliance" o "cis"
        comp_policies = [p for p in policies if any(x in p.get("name", "").lower() for x in ["audit", "compliance", "cis", "pci"])]
        
        if not comp_policies:
            all_findings.append(Finding(
                title="Absence of Compliance Benchmarking",
                domain=domain_id, source=source_tag,
                metrics={"compliance_policies_found": 0},
                score=1.5, confidence="High",
                recommendations=["Implement CIS Benchmarks scans", "Audit server hardening configurations"]
            ))

        # --- Finding 4.2: Policy Complexity/Health ---
        # Si tienes demasiadas políticas (> 50), suele haber un desorden administrativo
        if len(policies) > 50:
            all_findings.append(Finding(
                title="Scan Policy Sprawl",
                domain=domain_id, source=source_tag,
                metrics={"policy_count": len(policies)},
                score=3.0, confidence="Medium",
                recommendations=["Consolidate scan policies", "Remove unused or legacy policy templates"]
            ))

    except Exception as e:
        all_findings.append(Finding(
            title="Module Error: Domain 4",
            domain=domain_id, source="system",
            metrics={"exception": str(e)},
            score=1.0, confidence="High",
            recommendations=["Check master_data['policies'] structure"]
        ))

    return all_findings
