"""Tests for the source evaluation logic in research_skills.evaluator."""

import pytest
from datetime import date

from research_skills.core import CredibilityLevel, ResearchSource, SourceType
from research_skills.evaluator import (
    EvaluationResult,
    _credibility_from_score,
    _score_for_tiers,
    evaluate_source,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def peer_reviewed_source():
    return ResearchSource(
        title="Deep Learning for NLP",
        url="https://doi.org/10.1000/xyz123",
        source_type=SourceType.PEER_REVIEWED,
        publication_date=date(2022, 6, 15),
        author="Jane Doe",
        domain="doi.org",
        citation_count=120,
        is_open_access=True,
    )


@pytest.fixture
def blog_source():
    return ResearchSource(
        title="10 Tips for Better Research",
        url="https://randomblog.example.com/tips",
        source_type=SourceType.BLOG,
        publication_date=date(2019, 3, 1),
        author=None,
        domain="randomblog.example.com",
        citation_count=0,
        is_open_access=True,
    )


@pytest.fixture
def government_source():
    return ResearchSource(
        title="National Science Report 2023",
        url="https://science.gov/report2023",
        source_type=SourceType.GOVERNMENT,
        publication_date=date(2023, 1, 10),
        author="Federal Science Agency",
        domain="science.gov",
        citation_count=5,
        is_open_access=True,
    )


# ---------------------------------------------------------------------------
# _score_for_tiers
# ---------------------------------------------------------------------------

class TestScoreForTiers:
    def test_value_below_all_tiers_returns_zero(self):
        assert _score_for_tiers(-1, [(0, 1), (5, 2), (10, 3)]) == 0

    def test_value_at_first_threshold(self):
        assert _score_for_tiers(0, [(0, 1), (5, 2), (10, 3)]) == 1

    def test_value_at_middle_threshold(self):
        assert _score_for_tiers(5, [(0, 1), (5, 2), (10, 3)]) == 2

    def test_value_above_all_thresholds(self):
        assert _score_for_tiers(100, [(0, 1), (5, 2), (10, 3)]) == 3

    # Edge case: empty tiers list should return 0
    def test_empty_tiers_returns_zero(self):
        assert _score_for_tiers(10, []) == 0


# ---------------------------------------------------------------------------
# _credibility_from_score
# ---------------------------------------------------------------------------

class TestCredibilityFromScore:
    def test_low_score_returns_low(self):
        assert _credibility_from_score(0) == CredibilityLevel.LOW

    def test_medium_boundary(self):
        result = _credibility_from_score(40)
        assert result in (CredibilityLevel.LOW, CredibilityLevel.MEDIUM)

    def test_high_score_returns_high(self):
        assert _credibility_from_score(90) == CredibilityLevel.HIGH

    def test_score_above_max_clamps_to_high(self):
        assert _credibility_from_score(200) == CredibilityLevel.HIGH

    # Negative scores should also be treated as LOW
    def test_negative_score_returns_low(self):
        assert _credibility_from_score(-10) == CredibilityLevel.LOW


# ------
