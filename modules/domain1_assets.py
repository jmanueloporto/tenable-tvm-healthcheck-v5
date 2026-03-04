"""
PROJECT: [V5-Tenable Health Check API Automation]
VERSION: 5.0.0
LAYER: Business / Modules
DESCRIPTION: Generates findings for Domain 1 (Asset Visibility & Inventory).
AUTHOR: Senior Software Architect
"""

from core.models import Finding
from typing import List, Dict, Any

def run_audit(master_data: Dict[str, Any]) -> List[Finding]:
    """
    Analyzes master_data to assess Asset Visibility and Inventory maturity.
    """
    all_findings: List[Finding] = []
    domain_id = 1
    source_tag = "api"

    try:
        # --- Finding 1.1: Overall Asset Coverage ---
        assets = master_data.get("assets_raw", [])
        if not isinstance(assets, list):
            all_findings.append(Finding(
                title="Asset Data Collection Failure",
                domain=domain_id,
                source=source_tag,
                metrics={"error": str(assets)},
                score=1.0,
                confidence="High",
                recommendations=["Check API Export permissions"]
            ))
        elif len(assets) == 0:
            all_findings.append(Finding(
                title="Zero Assets Discovered",
                domain=domain_id,
                source=source_tag,
                metrics={"total_assets": 0},
                score=1.0,
                confidence="High",
                recommendations=["Check network scan ranges"]
            ))

        # --- Finding 1.3: Scanner Infrastructure ---
        scanners_data = master_data.get("scanners", {})
        if isinstance(scanners_data, dict):
            scanners = scanners_data.get("scanners", [])
            offline = [s for s in scanners if s.get("status") != "on"]
            if offline:
                all_findings.append(Finding(
                    title="Offline Scanner Infrastructure",
                    domain=domain_id,
                    source=source_tag,
                    metrics={"offline_count": len(offline)},
                    score=2.0,
                    confidence="High",
                    recommendations=[f"Investigate scanner: {offline[0].get('name')}"]
                ))

        # --- Finding 1.4: Asset Tagging ---
        tags = master_data.get("tags", [])
        if isinstance(tags, list) and len(tags) == 0:
            all_findings.append(Finding(
                title="Missing Asset Tagging",
                domain=domain_id,
                source=source_tag,
                metrics={"tag_count": 0},
                score=1.0,
                confidence="High",
                recommendations=["Implement tagging taxonomy"]
            ))

    except Exception as e:
        all_findings.append(Finding(
            title="Module Error: Domain 1",
            domain=domain_id,
            source="system",
            metrics={"exception": str(e)},
            score=1.0,
            confidence="High",
            recommendations=["Review modules/domain1_assets.py"]
        ))

    return all_findings
