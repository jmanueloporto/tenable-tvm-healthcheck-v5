# VERSION: 5.3.4-FINAL
"""
PROJECT: [V5-Tenable Health Check API Automation]
VERSION: 5.3.4
LAYER: Business / Modules
DESCRIPTION: Re-engineered Domain 2 (Scanning Operations) with scan quality metrics.
AUTHOR: Senior Software Architect
"""

from core.models import Finding
from typing import List, Dict, Any
from datetime import datetime, timezone

def run_audit(master_data: Dict[str, Any]) -> List[Finding]:
    all_findings: List[Finding] = []
    domain_id = 2
    source_tag = "api"
    base_score = 5.0
    now = datetime.now(timezone.utc)

    try:
        assets = master_data.get('assets', [])
        policies = master_data.get('infrastructure', {}).get('policies', [])
        
        if not assets: return []

        total_assets = len(assets)
        auth_count = 0
        recent_gaps = []

        for a in assets:
            # 2.1 Auth Rate (Agent or Authenticated Date)
            last_auth_str = a.get('last_authenticated_scan_date')
            if a.get('has_agent') is True or last_auth_str:
                auth_count += 1

            # 2.2 Scan Recency (30 días)
            last_seen_str = a.get('last_scan_time')
            is_recent = False
            if last_seen_str:
                try:
                    dt = datetime.fromisoformat(last_seen_str.replace('Z', '+00:00'))
                    if (now - dt).days <= 30:
                        is_recent = True
                except: pass
            if not is_recent: recent_gaps.append(a)

        # --- Evaluación de Hallazgos ---

        # Finding 2.1: Auth vs Unauth
        auth_rate = round((auth_count / total_assets) * 100, 1)
        if auth_rate < 85:
            impact = 2.0 if auth_rate < 50 else 1.0
            base_score -= impact
            evidence = f"Authenticated scan rate is {auth_rate}%. ({auth_count}/{total_assets} assets)."
            all_findings.append(Finding(title="Low Credentialed Scan Coverage", domain=domain_id, score=impact, observation=evidence, recommendations=["Configure scan credentials or deploy agents"]))

        # Finding 2.2: Scan Recency
        gap_ratio = len(recent_gaps) / total_assets
        if gap_ratio > 0.20:
            base_score -= 1.0
            evidence = f"Assets not scanned in 30 days ({len(recent_gaps)}): " + ", ".join([str(a.get('name', a.get('ipv4', 'Unknown'))) for a in recent_gaps][:10])
            all_findings.append(Finding(title="Scanning Frequency Gap", domain=domain_id, score=1.0, observation=evidence, recommendations=["Increase scan frequency to at least every 30 days"]))

        # Finding 2.4: Custom Policies
        if not policies:
            base_score -= 0.5
            evidence = "0 custom policies detected. Environment relies entirely on default Tenable templates."
            all_findings.append(Finding(title="Lack of Scan Customization", domain=domain_id, score=2.5, observation=evidence, recommendations=["Create custom scan policies for optimized vulnerability detection"]))

    except Exception as e:
        base_score = 1.0
        all_findings.append(Finding(title="Domain 2 Audit Error", domain=domain_id, score=1.0, observation=str(e)))

    return all_findings
