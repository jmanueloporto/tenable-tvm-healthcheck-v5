"""
PROJECT: [V5-Tenable Health Check API Automation]
VERSION: 5.1.1
LAYER: Business / Modules
DESCRIPTION: Identity Hygiene with Evidence Grouping (Brute Force, Stale, SSO).
AUTHOR: Senior Software Architect
"""

from core.models import Finding
from typing import List, Dict, Any
from datetime import datetime, timezone

def run_audit(master_data: Dict[str, Any]) -> List[Finding]:
    """
    Evaluates Governance and Ecosystem via Identity Hygiene with grouped evidence.
    """
    all_findings: List[Finding] = []
    source_tag = "api"
    base_score_d5 = 5.0
    
    # Listas de evidencia
    brute_force_users = []
    stale_users = []
    stale_api_keys = []
    local_users = []

    try:
        users = master_data.get('users', [])
        if not isinstance(users, list) or not users:
            return []

        total_users = len(users)
        now = datetime.now(timezone.utc)

        for user in users:
            u_name = user.get('username') or user.get('name') or "Unknown"
            
            # 1. Evidencia de Fuerza Bruta
            if user.get('login_fail_total', 0) > 5:
                brute_force_users.append(u_name)

            # 2. Evidencia de Cuentas Stale (> 90 días)
            last_login_str = user.get('last_login')
            if not last_login_str:
                stale_users.append(u_name)
            else:
                try:
                    last_login_dt = datetime.fromisoformat(last_login_str.replace('Z', '+00:00'))
                    if (now - last_login_dt).days > 90:
                        stale_users.append(u_name)
                except: stale_users.append(u_name)

            # 3. Evidencia de API Keys Antiguas (> 180 días)
            last_api_str = user.get('last_api_key_access')
            if last_api_str:
                try:
                    last_api_dt = datetime.fromisoformat(last_api_str.replace('Z', '+00:00'))
                    if (now - last_api_dt).days > 180:
                        stale_api_keys.append(u_name)
                except: pass

            # 4. Evidencia de Falta de SSO
            if user.get('type') == 'local':
                local_users.append(u_name)

        # --- Consolidación de Hallazgos Grouped ---

        if brute_force_users:
            all_findings.append(Finding(
                title="Consolidated Brute Force Alert",
                domain=5, source=source_tag,
                metrics={"affected_accounts": ", ".join(brute_force_users)},
                score=1.0, confidence="High",
                recommendations=["Lock listed accounts", "Force password reset", "Review source logs"]
            ))
            base_score_d5 -= 1.0

        if len(stale_users) / total_users > 0.20:
            all_findings.append(Finding(
                title="Bulk Stale Accounts (Zombies)",
                domain=5, source=source_tag,
                metrics={"affected_accounts": ", ".join(stale_users)},
                score=1.0, confidence="High",
                recommendations=["Deprovision listed users", "Implement 90-day inactivity policy"]
            ))
            base_score_d5 -= 1.0

        if local_users:
            all_findings.append(Finding(
                title="Non-Federated Identity Risk (Local Users)",
                domain=5, source=source_tag,
                metrics={"affected_accounts": ", ".join(local_users)},
                score=3.0, confidence="High",
                recommendations=["Migrate listed users to SAML/SSO", "Enforce MFA for locals"]
            ))

        if stale_api_keys:
            all_findings.append(Finding(
                title="Stale Integration Credentials (API Keys)",
                domain=6, source=source_tag,
                metrics={"affected_accounts": ", ".join(stale_api_keys)},
                score=3.0, confidence="Medium",
                recommendations=["Rotate keys for listed accounts", "Disable unused integrations"]
            ))

    except Exception as e:
        all_findings.append(Finding(
            title="Evidence Aggregator Error",
            domain=5, source="system",
            metrics={"exception": str(e)},
            score=1.0, confidence="High",
            recommendations=["Verify user metadata structure"]
        ))

    return all_findings
