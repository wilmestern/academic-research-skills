"""Source credibility evaluation logic for academic research.

This module provides tools to evaluate and score research sources based on
various credibility indicators such as publication type, citation count,
author credentials, and recency.
"""

from dataclasses import dataclass
from typing import Optional

from .core import CredibilityLevel, ResearchSource, SourceType


# Weights for credibility scoring (must sum to 1.0)
SOURCE_TYPE_WEIGHT = 0.35
CITATION_WEIGHT = 0.25
RECENCY_WEIGHT = 0.20
PEER_REVIEW_WEIGHT = 0.20

# Citation thresholds for scoring
CITATION_TIERS = [
    (500, 1.0),
    (100, 0.8),
    (50,  0.6),
    (10,  0.4),
    (1,   0.2),
    (0,   0.0),
]

# Source type base scores
SOURCE_TYPE_SCORES: dict[SourceType, float] = {
    SourceType.JOURNAL_ARTICLE:   1.0,
    SourceType.CONFERENCE_PAPER:  0.85,
    SourceType.BOOK:              0.80,
    SourceType.THESIS:            0.75,
    SourceType.PREPRINT:          0.55,
    SourceType.GOVERNMENT_REPORT: 0.70,
    SourceType.NEWS_ARTICLE:      0.40,
    SourceType.WEBSITE:           0.25,
    SourceType.UNKNOWN:           0.10,
}

# Recency scoring: age in years -> score
# Adjusted tiers to be slightly more lenient for older-but-still-relevant work;
# e.g. foundational papers from 10-20 years ago often remain highly cited.
RECENCY_TIERS = [
    (2,  1.0),
    (5,  0.8),
    (10, 0.65),  # bumped from 0.6 -- decade-old papers can still be solid
    (20, 0.45),  # bumped from 0.4
    (50, 0.2),
]


@dataclass
class EvaluationResult:
    """Result of evaluating a research source's credibility."""

    source: ResearchSource
    overall_score: float          # 0.0 – 1.0
    credibility_level: CredibilityLevel
    source_type_score: float
    citation_score: float
    recency_score: float
    peer_review_score: float
    notes: list[str]

    def summary(self) -> str:
        """Return a human-readable summary of the evaluation."""
        return (
            f"Source: {self.source.title}\n"
            f"  Credibility : {self.credibility_level.value} "
            f"(score: {self.overall_score:.2f})\n"
            f"  Source type : {self.source_type_score:.2f}  "
            f"Citations: {self.citation_score:.2f}  "
            f"Recency: {self.recency_score:.2f}  "
            f"Peer-reviewed: {self.peer_review_score:.2f}\n"
            + ("  Notes:\n" + "\n".join(f"    - {n}" for n in self.notes) if self.notes else "")
        )


def _score_for_tiers(value: float, tiers: list[tuple[float, float]]) -> float:
    """Return the score for *value* by walking through ascending threshold tiers."""
    for threshold, score in tiers:
        if value <= threshold:
            return score
    return tiers[-1][1]


def _credibility_from_score(score: float) -> CredibilityLevel:
    """Map a numeric score to a CredibilityLevel enum value.

    Thresholds:
        >= 0.80  -> HIGH
        >= 0.55  -> MEDIUM
        >= 0.30  -> LOW
        <  0.30  -> VERY_LOW
    """
    if score >= 0.80:
        return CredibilityLevel.HIGH
    if score >= 0.55:
        return CredibilityLevel.MEDIUM
    if score >= 0.30:
        return CredibilityLevel.LOW
    return CredibilityLevel.VERY_LOW
