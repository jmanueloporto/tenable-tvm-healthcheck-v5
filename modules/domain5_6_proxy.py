"""
PROJECT: [V5-Tenable Health Check API Automation]
VERSION: 5.0.7
LAYER: Business / Modules
DESCRIPTION: Analyzes Domain 5 (Governance) and Domain 6 (Ecosystem) via Proxy Indicators.
AUTHOR: Senior Software Architect
"""

from core.models import Finding
from typing import List, Dict, Any

def run_audit(master_data: Dict[str, Any]) -> List[Finding]:
    """
    Evaluates Operational Engagement and Ecosystem Integration based on API metadata.
    """
    all_findings: List[Finding] = []
    source_tag = "api"

    try:
        users = master_data.get('users', [])
        
        # --- DOMINIO 5: Program Governance & Operations ---
        if isinstance(users, list):
            # Finding 5.1: Key-person dependency (Operational Resilience)
            active_users = [u for u in users if u.get('enabled') is True]
            if 0 < len(active_users) <= 2:
                all_findings.append(Finding(
                    title="Key-person Dependency Risk",
                    domain=5, source=source_tag,
                    metrics={"active_users": len(active_users)},
                    score=2.0, confidence="High",
                    recommendations=["Distribute administrative responsibilities", "Onboard additional operational staff"]
                ))

            # Finding 5.2: Admin Hygiene (Inactive Admins)
            # Buscamos admins (permissions >= 64) que no tengan registro de last_login_recent
            # Nota: Adaptamos la lógica según la disponibilidad de campos en la exportación nativa
            inactive_admins = [u for u in users if u.get('permissions', 0) >= 64 and not u.get('last_login_attempt')]
            if inactive_admins:
                all_findings.append(Finding(
                    title="Inactive Administrative Accounts",
                    domain=5, source=source_tag,
                    metrics={"inactive_admin_count": len(inactive_admins)},
                    score=2.0, confidence="Medium",
                    recommendations=["Deactivate unused admin accounts", "Review access control monthly"]
                ))

        # --- DOMINIO 6: Ecosystem Integration & Security Posture ---
        # Finding 6.1: Integration Indicators (Service Accounts)
        service_accounts = [
            u for u in users 
            if any(term in u.get('username', '').lower() or u.get('name', '').lower() 
            for term in ['api', 'svc', 'service', 'automation', 'integration', 'siem', 'itsm'])
        ]
        
        if not service_accounts:
            all_findings.append(Finding(
                title="Lack of Ecosystem Integration",
                domain=6, source=source_tag,
                metrics={"service_accounts_detected": 0},
                score=3.0, confidence="Medium",
                recommendations=["Integrate Tenable with SIEM/ITSM via API Service Accounts", "Automate ticket creation for critical vulns"]
            ))

    except Exception as e:
        # Resiliencia Estricta: Un fallo en el análisis proxy no debe tumbar el reporte
        all_findings.append(Finding(
            title="Proxy Analysis Module Error",
            domain=5, source="system",
            metrics={"exception": str(e)},
            score=1.0, confidence="High",
            recommendations=["Verify 'users' and 'audit_log' structure in master_data"]
        ))

    return all_findings
