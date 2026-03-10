"""
PROJECT: [V5-Tenable Health Check API Automation]
VERSION: 5.1.0
LAYER: Business / Modules
DESCRIPTION: Re-engineered Domain 3 (Risk Prioritization & Analysis).
             Focuses on Vuln Density, VPR Adoption, and Aging.
AUTHOR: Senior Software Architect
"""

from core.models import Finding
from typing import List, Dict, Any, Tuple
from datetime import datetime, timezone

def run_audit(master_data: Dict[str, Any]) -> List[Finding]:
    all_findings: List[Finding] = []
    domain_id = 3
    source_tag = "api"
    base_score = 5.0
    now = datetime.now(timezone.utc)

    try:
        vulns = master_data.get('vulnerabilities', [])
        assets = master_data.get('assets', [])
        total_assets = len(assets)
        total_vulns = len(vulns)

        if total_assets == 0:
            return [Finding(
                title="Insufficient Data for Risk Analysis",
                domain=domain_id,
                score=1.0,
                observation="No assets found to calculate vulnerability density.",
                recommendations=["Ensure Step 2 and Step 5 of Data Collector are functional."]
            )]

        # --- Finding 3.1: Vulnerability Landscape & Density ---
        density = total_vulns / total_assets
        if density > 50:
            base_score -= 1.0
            evidence = f"Vulnerability density is {density:.2f} per asset. Total C/H/M/L: {total_vulns}."
            all_findings.append(Finding(
                title="High Vulnerability Density",
                domain=domain_id,
                score=1.0,
                observation=evidence,
                recommendations=["Target assets with highest density for immediate remediation."]
            ))

        # --- Finding 3.2: VPR Adoption vs CVSS ---
        # Analizamos vulnerabilidades con VPR Crítico (> 9.0)
        high_vpr_vulns = [v for v in vulns if float(v.get('vpr_score', 0) or 0) >= 9.0]
        high_vpr_count = len(high_vpr_vulns)
        
        # Si no hay VPR en la mayoría o hay muchos riesgos críticos VPR
        if high_vpr_count > 0:
            base_score -= 1.0
            evidence = f"Detected {high_vpr_count} Critical VPR risks. Prioritizing by VPR > 9.0 could reduce immediate exposure."
            all_findings.append(Finding(
                title="VPR Prioritization Opportunity",
                domain=domain_id,
                score=1.0,
                observation=evidence,
                recommendations=["Shift from CVSS-only to VPR-based prioritization to focus on exploitable risks."]
            ))

        # --- Finding 3.3: Vulnerability Aging (Critical > 30 days) ---
        old_criticals = []
        for v in vulns:
            severity = str(v.get('severity', '')).lower()
            if severity == 'critical':
                first_found_str = v.get('first_found')
                if first_found_str:
                    try:
                        # Parseo ISO 8601 compatible con v5.0.17
                        dt = datetime.fromisoformat(first_found_str.replace('Z', '+00:00'))
                        age_days = (now - dt).days
                        if age_days > 30:
                            old_criticals.append(v)
                    except:
                        pass

        if len(old_criticals) > 0:
            base_score -= 1.0
            titles = [v.get('plugin', {}).get('name', 'Unknown')[:30] for v in old_criticals]
            evidence = f"Critical vulnerabilities older than 30 days ({len(old_criticals)}): " + ", ".join(titles[:5])
            all_findings.append(Finding(
                title="Critical Vulnerability Aging",
                domain=domain_id,
                score=1.0,
                observation=evidence,
                recommendations=["Enforce stricter SLAs for 'Critical' severity findings to stay under 30 days."]
            ))

    except Exception as e:
        base_score = 1.0
        all_findings.append(Finding(
            title="Domain 3 Audit Error",
            domain=domain_id,
            score=1.0,
            observation=f"Error processing risk data: {str(e)}"
        ))

    return all_findings
