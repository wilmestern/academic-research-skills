"""Core module for academic research skills toolkit.

Provides foundational classes and utilities for managing research workflows,
source evaluation, citation handling, and research methodology guidance.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class SourceType(Enum):
    """Enumeration of academic source types."""

    JOURNAL_ARTICLE = "journal_article"
    BOOK = "book"
    BOOK_CHAPTER = "book_chapter"
    CONFERENCE_PAPER = "conference_paper"
    THESIS = "thesis"
    REPORT = "report"
    WEBSITE = "website"
    OTHER = "other"


class CredibilityLevel(Enum):
    """Credibility rating for academic sources."""

    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    UNVERIFIED = "unverified"


@dataclass
class ResearchSource:
    """Represents a single academic source with metadata and evaluation data."""

    title: str
    authors: list[str]
    year: int
    source_type: SourceType = SourceType.OTHER
    doi: Optional[str] = None
    url: Optional[str] = None
    journal: Optional[str] = None
    publisher: Optional[str] = None
    abstract: Optional[str] = None
    keywords: list[str] = field(default_factory=list)
    credibility: CredibilityLevel = CredibilityLevel.UNVERIFIED
    notes: str = ""
    added_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self) -> None:
        """Validate source data after initialisation."""
        if not self.title or not self.title.strip():
            raise ValueError("Source title cannot be empty.")
        if not self.authors:
            raise ValueError("At least one author must be provided.")
        current_year = datetime.now().year
        if not (1000 <= self.year <= current_year):
            raise ValueError(f"Year must be between 1000 and {current_year}.")

    @property
    def age_years(self) -> int:
        """Return how many years old the source is."""
        return datetime.now().year - self.year

    @property
    def is_recent(self) -> bool:
        """Return True if the source was published within the last 5 years."""
        return self.age_years <= 5

    def to_apa(self) -> str:
        """Generate a basic APA 7th edition citation string."""
        author_str = self._format_authors_apa()
        base = f"{author_str} ({self.year}). {self.title}."

        if self.source_type == SourceType.JOURNAL_ARTICLE and self.journal:
            base += f" *{self.journal}*."
        elif self.publisher:
            base += f" {self.publisher}."

        if self.doi:
            base += f" https://doi.org/{self.doi}"
        elif self.url:
            base += f" {self.url}"

        return base

    def _format_authors_apa(self) -> str:
        """Format author list in APA style (Last, F. I.)."""
        formatted: list[str] = []
        for author in self.authors:
            parts = author.strip().split()
            if len(parts) >= 2:
                last = parts[-1]
                initials = ". ".join(p[0].upper() for p in parts[:-1]) + "."
                formatted.append(f"{last}, {initials}")
            else:
                formatted.append(author)

        if len(formatted) == 1:
            return formatted[0]
        if len(formatted) == 2:
            return f"{formatted[0]}, & {formatted[1]}"
        return ", ".join(formatted[:-1]) + f", & {formatted[-1]}"


def evaluate_source_credibility(source: ResearchSource) -> CredibilityLevel:
    """Heuristically evaluate the credibility of a research source.

    Args:
        source: The ResearchSource to evaluate.

    Returns:
        A CredibilityLevel based on available metadata.
    """
    score = 0

    # Peer-reviewed source types score higher
    if source.source_type in (SourceType.JOURNAL_ARTICLE, SourceType.CONFERENCE_PAPER):
        score += 3
    elif source.source_type in (SourceType.BOOK, SourceType.BOOK_CHAPTER, SourceType.THESIS):
        score += 2
    elif source.source_type == SourceType.REPORT:
        score += 1

    # DOI presence suggests formal publication
    if source.doi and re.match(r"^10\.\d{4,}/", source.doi):
        score += 2

    # Recency adds credibility in fast-moving fields
    if source.is_recent:
        score += 1

    # Abstract and keywords indicate thorough metadata
    if source.abstract:
        score += 1
    if source.keywords:
        score += 1

    if score >= 6:
        return CredibilityLevel.HIGH
    if score >= 3:
        return CredibilityLevel.MEDIUM
    return CredibilityLevel.LOW
