"""
PROJECT: [V5-Tenable Health Check API Automation]
VERSION: 5.1.1
LAYER: Core / Scoring
DESCRIPTION: Maturity calculation engine. Supports override_score logic.
AUTHOR: Senior Software Architect
"""
from typing import List, Dict
from core.models import Finding

def calculate_maturity(findings: List[Finding]) -> Dict[int, float]:
    domain_scores = {1: 5.0, 2: 5.0, 3: 5.0, 4: 5.0, 5: 5.0, 6: 5.0}
    
    for f in findings:
        if f.domain in domain_scores:
            penalty = f.score if f.override_score is None else f.override_score
            domain_scores[f.domain] -= penalty
            
    for domain in domain_scores:
        domain_scores[domain] = max(1.0, min(5.0, domain_scores[domain]))
        
    return domain_scores
