"""
PROJECT: [V5-Tenable Health Check API Automation]
VERSION: 5.0.0
LAYER: Core / Scoring
DESCRIPTION: Logic for calculating maturity scores per domain and overall platform maturity.
AUTHOR: Senior Software Architect
"""

from typing import List, Dict
from core.models import Finding

class ScoringEngine:
    """
    Engine responsible for aggregating findings into domain scores and
    calculating the final maturity level using configurable weights.
    """

    def __init__(self, custom_weights: Dict[int, float] = None):
        """
        Initializes the engine with Phase 1 default weights.
        """
        # Weights: D1(25%), D2(25%), D3(20%), D4(25%), D5(3%), D6(2%)
        self.domain_weights = custom_weights or {
            1: 0.25,
            2: 0.25,
            3: 0.20,
            4: 0.25,
            5: 0.03,
            6: 0.02
        }
        self._validate_weights()

    def _validate_weights(self):
        """Ensures that the sum of weights equals 100%."""
        total = sum(self.domain_weights.values())
        if not (0.99 <= total <= 1.01):
            raise ValueError(f"Weights must sum to 1.0. Current sum: {total}")

    def calculate_domain_scores(self, findings: List[Finding]) -> Dict[int, float]:
        """
        Groups findings by domain and calculates average score.
        IMPORTANT: If no findings exist for a domain, it returns 5.0 (Healthy).
        """
        domain_data: Dict[int, List[float]] = {d: [] for d in self.domain_weights.keys()}
        
        for f in findings:
            if f.domain in domain_data:
                # Priority: Override Score (Phase 3) > Base Score
                val = f.override_score if f.override_score is not None else f.score
                domain_data[f.domain].append(val)

        domain_scores = {}
        for d_id, scores in domain_data.items():
            # Logic: If domain has findings, average them. If empty, it's a 5.0 (Maturity Max).
            if scores:
                domain_scores[d_id] = round(sum(scores) / len(scores), 2)
            else:
                domain_scores[d_id] = 5.0
            
        return domain_scores

    def calculate_overall_score(self, domain_scores: Dict[int, float]) -> float:
        """Applies weights to domain scores to find the final 1-5 result."""
        overall = 0.0
        for d_id, score in domain_scores.items():
            weight = self.domain_weights.get(d_id, 0.0)
            overall += score * weight
            
        return round(overall, 2)
