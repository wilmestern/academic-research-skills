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
        """Return True if the source was published within the last 10 years.

        Note: Changed threshold from 5 to 10 years to better suit my field
        (historical research), where sources from the past decade are still
        considered current.
        """
        return self.age_years <= 10

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
            if len(par
