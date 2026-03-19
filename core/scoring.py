""" VERSION: 5.4.2 | STATUS: STABLE - PURE API """ VERSION: 5.4.2 | STATUS: STABLE - PURE API """ VERSION: 5.4.2 | STATUS: STABLE - PURE API """ VERSION: 5.4.2 | STATUS: STABLE - PURE API """ VERSION: 5.4.2 | STATUS: STABLE - PURE API """ VERSION: 5.4.2 | STATUS: STABLE - PURE API """ VERSION: 5.4.0 | STATUS: Stable """ MTTR ENGINE """ MTTR ENGINE """ MTTR ENGINE """ MTTR ENGINE """ MTTR ENGINE """ MTTR ENGINE """
# VERSION: 5.3.4-FINAL
"""
LAYER: Core / Scoring
DESCRIPTION: Robust maturity calculation engine.
"""
from typing import List, Dict
from core.models import Finding

def calculate_maturity(findings: List[Finding], context: Dict = None):
    # Base de madurez perfecta (5.0) para cada dominio
    domain_scores = {1: 5.0, 2: 5.0, 3: 5.0, 4: 5.0, 5: 5.0, 6: 5.0}
    
    for f in findings:
        # Validamos que f sea un objeto Finding y tenga el atributo domain
        if hasattr(f, 'domain') and f.domain in domain_scores:
            # Restamos la penalización del hallazgo
            penalty = f.score if getattr(f, 'override_score', None) is None else f.override_score
            domain_scores[f.domain] -= penalty
    
    # Normalizar entre 1.0 y 5.0
    for domain in domain_scores:
        domain_scores[domain] = max(1.0, min(5.0, domain_scores[domain]))
        
    global_score = sum(domain_scores.values()) / len(domain_scores)
    return domain_scores, global_score
