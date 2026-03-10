"""
PROJECT: [V5-Tenable Health Check API Automation]
VERSION: 5.1.1
LAYER: Audit Modules / Domain 1
DESCRIPTION: Shadow IT Detection Engine.
AUTHOR: Senior Software Architect
"""
from core.models import Finding
from typing import List, Dict, Any

def run_audit(master_data: Dict[str, Any]) -> List[Finding]:
    all_findings = []
    domain_id = 1
    context = master_data.get('context', {})
    assets = master_data.get('assets', [])
    
    expected = context.get('expected_assets', 0)
    detected = len(assets)
    
    if expected > 0 and expected > detected:
        gap_count = expected - detected
        gap_pct = (gap_count / expected) * 100
        
        if gap_pct > 10:
            score_val = 5.0 if gap_pct > 20 else 3.0
            all_findings.append(Finding(
                title=f"{'Critical' if score_val == 5.0 else 'Moderate'} Risk: Shadow IT Gap",
                domain=domain_id,
                score=score_val,
                observation=f"Brecha de visibilidad del {gap_pct:.1f}% detectada.",
                evidence=f"Expected: {expected} | Detected: {detected} | Gap: {gap_count}",
                source="Business Context vs API",
                recommendations=["Ejecutar Discovery Scans", "Revisar despliegue de agentes"]
            ))
    return all_findings
