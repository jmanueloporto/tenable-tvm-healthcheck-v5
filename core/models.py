"""
PROJECT: [V5-Tenable Health Check API Automation]
VERSION: 5.0.19
LAYER: Core / Models
DESCRIPTION: Golden Model. Universal compatibility for all audit domains and scoring engine.
AUTHOR: Senior Software Architect
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class Finding:
    title: str
    domain: int
    score: float
    observation: str = "N/A"
    source: str = "api"
    confidence: str = "High"
    override_score: Optional[float] = None
    recommendations: List[str] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)
