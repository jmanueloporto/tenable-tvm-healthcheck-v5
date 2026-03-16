# VERSION: 5.3.4-FINAL-ADJUSTED
from core.models import Finding
from typing import List, Dict, Any

def run_audit(master_data: Dict[str, Any]) -> List[Finding]:
    all_findings = []
    domain_id = 1
    context = master_data.get('context', {})
    assets = master_data.get('assets', [])
    
    expected = context.get('expected_assets', 0)
    detected = len(assets)
    
    if expected > 0:
        gap_pct = ((expected - detected) / expected) * 100
        # Umbral ajustado: solo penaliza fuerte si la brecha es > 70%
        score_val = 2.0 if gap_pct > 70 else (1.0 if gap_pct > 30 else 0.0)
            
        if score_val > 0:
            all_findings.append(Finding(
                title="Asset Visibility Gap",
                domain=domain_id,
                score=score_val,
                observation=f"Visibilidad del {100-gap_pct:.1f}%.",
                evidence=f"Expected: {expected} | Detected: {detected}",
                recommendations=["Revisar inventario en data/context_input.json"]
            ))
    return all_findings
