"""Tests for the formatter module."""

import csv
import io
import pytest

from research_skills.core import CredibilityLevel, ResearchSource, SourceType
from research_skills.evaluator import EvaluationResult
from research_skills.formatter import (
    format_result_markdown,
    format_result_plain,
    format_results_csv,
)


@pytest.fixture
def sample_source() -> ResearchSource:
    """A peer-reviewed journal source for testing."""
    return ResearchSource(
        title="Deep Learning for NLP",
        authors=["Smith, J.", "Doe, A."],
        year=2022,
        source_type=SourceType.PEER_REVIEWED_JOURNAL,
        url="https://doi.org/10.1000/example",
        citation_count=150,
    )


@pytest.fixture
def sample_result(sample_source: ResearchSource) -> EvaluationResult:
    """An evaluation result for testing."""
    return EvaluationResult(
        source=sample_source,
        credibility=CredibilityLevel.HIGH,
        score=0.88,
        notes=["Recent publication", "High citation count"],
    )


@pytest.fixture
def low_score_result() -> EvaluationResult:
    """An evaluation result with low credibility."""
    source = ResearchSource(
        title="My Opinion Blog Post",
        authors=["Anonymous"],
        year=2015,
        source_type=SourceType.BLOG,
        url="https://example-blog.com/post",
        citation_count=0,
    )
    return EvaluationResult(
        source=source,
        credibility=CredibilityLevel.LOW,
        score=0.21,
        notes=["Blog source", "No citations", "Outdated"],
    )


class TestFormatResultPlain:
    """Tests for the plain-text formatter."""

    def test_contains_title(self, sample_result: EvaluationResult) -> None:
        output = format_result_plain(sample_result)
        assert "Deep Learning for NLP" in output

    def test_contains_credibility_label(self, sample_result: EvaluationResult) -> None:
        output = format_result_plain(sample_result)
        assert "HIGH" in output or "high" in output.lower()

    def test_contains_score(self, sample_result: EvaluationResult) -> None:
        output = format_result_plain(sample_result)
        assert "0.88" in output

    def test_contains_notes(self, sample_result: EvaluationResult) -> None:
        output = format_result_plain(sample_result)
        assert "Recent publication" in output
        assert "High citation count" in output

    def test_low_credibility_result(self, low_score_result: EvaluationResult) -> None:
        output = format_result_plain(low_score_result)
        assert "My Opinion Blog Post" in output
        assert "LOW" in output or "low" in output.lower()


class TestFormatResultMarkdown:
    """Tests for the Markdown formatter."""

    def test_contains_heading(self, sample_result: EvaluationResult) -> None:
        output = format_result_markdown(sample_result)
        # Markdown headings start with #
        assert "#" in output

    def test_contains_title(self, sample_result: EvaluationResult) -> None:
        output = format_result_markdown(sample_result)
        assert "Deep Learning for NLP" in output

    def test_contains_bold_or_emphasis(self, sample_result: EvaluationResult) -> None:
        output = format_result_markdown(sample_result)
        # Markdown uses ** or * for emphasis
        assert "**" in output or "*" in output

    def test_notes_rendered_as_list(self, sample_result: EvaluationResult) -> None:
        output = format_result_markdown(sample_result)
        # Markdown lists use - or *
        assert "- " in output or "* " in output

    def test_url_present(self, sample_result: EvaluationResult) -> None:
        output = format_result_markdown(sample_result)
        assert "https://doi.org/10.1000/example" in output


class TestFormatResultsCsv:
    """Tests for the CSV batch formatter."""

    def test_csv_has_header_row(self, sample_result, low_score_result) -> None:
        output = format_results_csv([sample_result, low_score_result])
        reader = csv.reader(io.StringIO(output))
        header = next(reader)
        assert len(header) > 0
        # Header should contain recognisable column names
        header_lower = [h.lower() for h in header]
        assert any("title" in h for h in header_lower)

    def test_csv_row_count_matches_input(self, sample_result, low_score_result) -> None:
        output = format_results_csv([sample_result, low_score_result])
        reader = csv.reader(io.StringIO(output))
        rows = list(reader)
        # 1 header + 2 data rows
        assert len(rows) == 3

    def test_csv_contains_scores(self, sample_result, low_score_result) -> None:
        output = format_results_csv([sample_result, low_score_result])
        assert "0.88" in output
        assert "0.21" in output

    def test_empty_list_returns_header_only(self) -> None:
        output = format_results_csv([])
        reader = csv.reader(io.StringIO(output))
        rows = list(reader)
        assert len(rows) == 1  # header only
