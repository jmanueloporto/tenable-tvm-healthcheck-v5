"""
PROJECT: [V5-Tenable Health Check API Automation]
VERSION: 5.0.7
LAYER: Core / Models
DESCRIPTION: Universal data structure (Finding) for audit results across all project phases.
AUTHOR: Senior Software Architect
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any

@dataclass
class Finding:
    """
    The universal data contract for any security finding or health check result.
    Designed for scalability from Phase 1 (API) to Phase 3 (ML/Manual Overrides).
    """
    title: str
    domain: int  # 1 to 6
    source: str  # e.g., 'api', 'questionnaire', 'custom'
    metrics: Dict[str, Any]
    score: float  # Maturity scale 1.0 to 5.0
    confidence: str  # 'High', 'Medium', 'Low'
    recommendations: List[str]
    annotations: List[Dict] = field(default_factory=list)  # Placeholder for Phase 3 metadata
    override_score: Optional[float] = None  # Placeholder for Phase 3 overrides

    def __post_init__(self):
        """Validates the score is within the allowed maturity scale."""
        if not (1.0 <= self.score <= 5.0):
            raise ValueError(f"Score must be between 1.0 and 5.0. Got: {self.score}")
