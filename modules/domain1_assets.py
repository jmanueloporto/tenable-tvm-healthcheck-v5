"""
PROJECT: [V5-Tenable Health Check API Automation]
VERSION: 5.0.19
LAYER: Business / Modules
DESCRIPTION: Re-engineered Domain 1 (Asset Visibility) with detailed evidence injection.
AUTHOR: Senior Software Architect
"""

from core.models import Finding
from typing import List, Dict, Any
from datetime import datetime, timezone

def run_audit(master_data: Dict[str, Any]) -> List[Finding]:
    all_findings: List[Finding] = []
    domain_id = 1
    source_tag = "api"
    base_score = 5.0
    now = datetime.now(timezone.utc)

    try:
        assets = master_data.get('assets', [])
        infra = master_data.get('infrastructure', {})
        connectors = infra.get('connectors', [])
        
        if not assets:
            return [Finding(title="Zero Assets Discovered", domain=domain_id, score=1.0, observation="No assets returned by asynchronous export API.", recommendations=["Check network scan ranges"])]

        total_assets = len(assets)
        stale = []
        agents_count = 0
        tagged_count = 0
        custom_acr_count = 0

        for a in assets:
            # 1.1 Stale Assets (> 90 días)
            last_seen_str = a.get('last_authenticated_scan_date') or a.get('last_scan_time')
            is_stale = True
            if last_seen_str:
                try:
                    dt = datetime.fromisoformat(last_seen_str.replace('Z', '+00:00'))
                    if (now - dt).days <= 90:
                        is_stale = False
                except: pass
            if is_stale: stale.append(a)

            # 1.2 Agent Count
            if a.get('has_agent') is True: agents_count += 1

            # 1.4 Tagging & ACR
            if a.get('tags'): tagged_count += 1
            if a.get('acr_score', 7) != 7: custom_acr_count += 1

        # --- Evaluación de Hallazgos ---

        # Finding 1.1: Stale Assets
        if (len(stale) / total_assets) > 0.15:
            base_score -= 1.0
            evidence = f"Stale assets ({len(stale)}): " + ", ".join([str(a.get('name', a.get('ipv4', 'Unknown'))) for a in stale][:10])
            all_findings.append(Finding(title="Stale Asset Inventory", domain=domain_id, score=1.0, observation=evidence, recommendations=["Decommission or rescan stale assets"]))

        # Finding 1.2: Agent Deployment
        agent_ratio = agents_count / total_assets
        if agent_ratio < 0.10:
            base_score -= 0.5
            evidence = f"Only {agents_count} out of {total_assets} assets have agents deployed."
            all_findings.append(Finding(title="Agent Deployment Gap", domain=domain_id, score=2.0, observation=evidence, recommendations=["Deploy Nessus Agents for deeper visibility"]))

        # Finding 1.4: Tagging & ACR
        if (tagged_count / total_assets) < 0.50 or custom_acr_count == 0:
            base_score -= 1.0
            evidence = f"Tagged assets: {tagged_count}/{total_assets}. Assets with custom ACR: {custom_acr_count}/{total_assets}."
            all_findings.append(Finding(title="Lack of Asset Classification", domain=domain_id, score=1.0, observation=evidence, recommendations=["Implement Tagging and tune ACR scores"]))

        # Finding 1.5: Cloud Connectors
        if not connectors:
            base_score -= 0.5
            evidence = "No Cloud Connectors detected or API returned 405 (Method Not Allowed)."
            all_findings.append(Finding(title="Missing Cloud Connectors", domain=domain_id, score=2.5, observation=evidence, recommendations=["Configure AWS/Azure/GCP connectors"]))

    except Exception as e:
        base_score = 1.0
        all_findings.append(Finding(title="Domain 1 Audit Error", domain=domain_id, score=1.0, observation=str(e)))

    return all_findings
