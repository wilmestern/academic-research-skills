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
RECENCY_TIERS = [
    (2,  1.0),
    (5,  0.8),
    (10, 0.6),
    (20, 0.4),
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
    """Map a numeric score to a CredibilityLevel enum value."""
    if score >= 0.80:
        return CredibilityLevel.HIGH
    if score >= 0.55:
        return CredibilityLevel.MEDIUM
    if score >= 0.30:
        return CredibilityLevel.LOW
    return CredibilityLevel.UNRELIABLE


def evaluate_source(source: ResearchSource) -> EvaluationResult:
    """Evaluate a single :class:`ResearchSource` and return an :class:`EvaluationResult`.

    Parameters
    ----------
    source:
        The research source to evaluate.

    Returns
    -------
    EvaluationResult
        Detailed breakdown of the credibility assessment.
    """
    notes: list[str] = []

    # --- Source type score ---
    type_score = SOURCE_TYPE_SCORES.get(source.source_type, 0.10)

    # --- Citation score ---
    citations = source.citation_count or 0
    cite_score = 0.0
    for threshold, score in sorted(CITATION_TIERS, key=lambda t: t[0]):
        if citations >= threshold:
            cite_score = score
    if citations == 0 and source.source_type not in (
        SourceType.PREPRINT, SourceType.THESIS
    ):
        notes.append("No citations recorded — may be very recent or obscure.")

    # --- Recency score ---
    age = source.age_years
    if age is None:
        recency_score = 0.3
        notes.append("Publication year unknown; recency score defaulted to 0.3.")
    else:
        recency_score = 1.0
        for max_age, score in sorted(RECENCY_TIERS, key=lambda t: t[0]):
            if age > max_age:
                recency_score = score
        if age > 50:
            recency_score = 0.1
            notes.append(f"Source is {age:.0f} years old — consider whether it is still current.")

    # --- Peer-review score ---
    if source.peer_reviewed is True:
        pr_score = 1.0
    elif source.peer_reviewed is False:
        pr_score = 0.0
        if source.source_type == SourceType.PREPRINT:
            notes.append("Preprint — not yet peer-reviewed; verify before citing.")
    else:
        # Unknown — infer from source type
        pr_score = 0.5
        notes.append("Peer-review status unknown; score estimated from source type.")
        if source.source_type == SourceType.JOURNAL_ARTICLE:
            pr_score = 0.9

    # --- Weighted overall score ---
    overall = (
        type_score   * SOURCE_TYPE_WEIGHT
        + cite_score * CITATION_WEIGHT
        + recency_score * RECENCY_WEIGHT
        + pr_score   * PEER_REVIEW_WEIGHT
    )

    return EvaluationResult(
        source=source,
        overall_score=round(overall, 4),
        credibility_level=_credibility_from_score(overall),
        source_type_score=type_score,
        citation_score=cite_score,
        recency_score=recency_score,
        peer_review_score=pr_score,
        notes=notes,
    )


def evaluate_sources(sources: list[ResearchSource]) -> list[EvaluationResult]:
    """Evaluate a list of sources and return results sorted by overall score (descending)."""
    results = [evaluate_source(s) for s in sources]
    results.sort(key=lambda r: r.overall_score, reverse=True)
    return results
