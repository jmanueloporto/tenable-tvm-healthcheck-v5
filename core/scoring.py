"""
PROJECT: [V5-Tenable Health Check API Automation]
VERSION: 5.1.3
LAYER: Core / Scoring
DESCRIPTION: Maturity engine with Contextual Override logic.
AUTHOR: Senior Software Architect
"""
from typing import List, Dict, Tuple, Optional
from core.models import Finding

def calculate_maturity(findings: List[Finding], context: Optional[Dict] = None) -> Tuple[Dict[int, float], float]:
    domain_scores = {1: 5.0, 2: 5.0, 3: 5.0, 4: 5.0, 5: 5.0, 6: 5.0}
    context = context or {}
    is_maintenance = context.get('maintenance_windows', False)
    
    for f in findings:
        if f.domain in domain_scores:
            # Lógica de Override Contextual (v5.1.3)
            if is_maintenance and f.domain in [2, 4] and f.score > 2.0:
                f.override_score = 1.0
                f.observation = f"[OVERRIDE MANTENIMIENTO] {f.observation}"
            
            penalty = f.override_score if f.override_score is not None else f.score
            domain_scores[f.domain] -= penalty
    
    # Normalización de límites
    for domain in domain_scores:
        domain_scores[domain] = max(1.0, min(5.0, domain_scores[domain]))
    
    global_score = sum(domain_scores.values()) / len(domain_scores)
    return domain_scores, global_score
