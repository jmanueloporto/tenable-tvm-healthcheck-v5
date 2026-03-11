"""
PROJECT: [V5-Tenable Health Check API Automation]
VERSION: 5.1.1
LAYER: Business / Modules
DESCRIPTION: Re-engineered Domain 1 with Shadow IT Inventory Gap Analysis.
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
        context = master_data.get('context', {})
        connectors = infra.get('connectors', [])
        
        total_assets = len(assets)

        # --- Check 2.1.1: Inventory Gap (Shadow IT) ---
        expected_assets = context.get('expected_assets', 0)
        if expected_assets > 0 and expected_assets > total_assets:
            gap_count = expected_assets - total_assets
            gap_pct = (gap_count / expected_assets) * 100
            
            if gap_pct > 10:
                score_val = 5.0 if gap_pct > 20 else 3.0
                base_score -= 2.0
                all_findings.append(Finding(
                    title=f"{'Critical' if score_val == 5.0 else 'Moderate'} Risk: Shadow IT Gap",
                    domain=domain_id,
                    score=score_val,
                    observation=f"Brecha de visibilidad del {gap_pct:.1f}% detectada. Expected: {expected_assets} | Detected: {total_assets} | Gap: {gap_count}",
                    recommendations=["Ejecutar Discovery Scans", "Revisar alcance de escaneo y despliegue de agentes"]
                ))

        if not assets:
            if expected_assets > 0:
                return all_findings # Retorna el gap detectado si no hay nada más
            return [Finding(title="Zero Assets Discovered", domain=domain_id, score=1.0, observation="No assets returned by API.", recommendations=["Check network scan ranges"])]

        # --- Validaciones Base de Fase 1 ---
        stale = []
        agents_count = 0
        tagged_count = 0
        custom_acr_count = 0

        for a in assets:
            # Stale Assets (> 90 días)
            last_seen_str = a.get('last_authenticated_scan_date') or a.get('last_scan_time')
            if last_seen_str:
                try:
                    dt = datetime.fromisoformat(last_seen_str.replace('Z', '+00:00'))
                    if (now - dt).days > 90:
                        stale.append(a)
                except: pass
            else:
                stale.append(a)

            # Agent Count
            if a.get('has_agent') is True: agents_count += 1

            # Tagging & ACR
            if a.get('tags'): tagged_count += 1
            if a.get('acr_score', 7) != 7: custom_acr_count += 1

        # Finding 1.1: Stale Assets
        if (len(stale) / total_assets) > 0.15:
            base_score -= 1.0
            all_findings.append(Finding(title="Stale Asset Inventory", domain=domain_id, score=1.0, observation=f"Stale assets detected: {len(stale)}", recommendations=["Decommission or rescan stale assets"]))

        # Finding 1.2: Agent Deployment
        agent_ratio = agents_count / total_assets
        if agent_ratio < 0.10:
            base_score -= 0.5
            all_findings.append(Finding(title="Agent Deployment Gap", domain=domain_id, score=2.0, observation=f"Low agent coverage: {agents_count}/{total_assets}", recommendations=["Deploy Nessus Agents"]))

        # Finding 1.4: Tagging & ACR
        if (tagged_count / total_assets) < 0.50:
            base_score -= 1.0
            all_findings.append(Finding(title="Lack of Asset Classification", domain=domain_id, score=1.0, observation=f"Tagged assets: {tagged_count}/{total_assets}", recommendations=["Implement Tagging"]))

        # Finding 1.5: Cloud Connectors
        if not connectors:
            base_score -= 0.5
            all_findings.append(Finding(title="Missing Cloud Connectors", domain=domain_id, score=2.5, observation="No Cloud Connectors detected.", recommendations=["Configure AWS/Azure/GCP connectors"]))

    except Exception as e:
        all_findings.append(Finding(title="Domain 1 Audit Error", domain=domain_id, score=1.0, observation=str(e)))

    return all_findings
