""" VERSION: 5.4.2 | STATUS: STABLE - PURE API """ VERSION: 5.4.2 | STATUS: STABLE - PURE API """ VERSION: 5.4.2 | STATUS: STABLE - PURE API """ VERSION: 5.4.2 | STATUS: STABLE - PURE API """ VERSION: 5.4.2 | STATUS: STABLE - PURE API """ VERSION: 5.4.2 | STATUS: STABLE - PURE API """ VERSION: 5.4.0 | STATUS: Stable """ MTTR ENGINE """ MTTR ENGINE """ MTTR ENGINE """ MTTR ENGINE """ MTTR ENGINE """ MTTR ENGINE """
# VERSION: 5.3.4-FINAL
"""
PROJECT: [V5-Tenable Health Check API Automation]
VERSION: 5.3.4
LAYER: Core / Models
DESCRIPTION: Universal Golden Model. Supports metrics, confidence and metadata.
AUTHOR: Senior Software Architect
"""
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

@dataclass
class Finding:
    title: str
    domain: int
    score: float
    observation: str = ""
    evidence: str = ""
    source: str = "Tenable API"
    confidence: str = "High"
    metrics: Dict[str, Any] = field(default_factory=dict)
    recommendations: List[str] = field(default_factory=list)
    override_score: Optional[float] = None
