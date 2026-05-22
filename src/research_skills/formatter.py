"""Formatting utilities for research source evaluation results.

Provides human-readable output for ResearchSource objects and
EvaluationResult summaries in various formats (plain text, markdown, CSV).
"""

from __future__ import annotations

from typing import List, Sequence

from .core import ResearchSource, CredibilityLevel
from .evaluator import EvaluationResult


# Emoji indicators for credibility levels in markdown output
_CREDIBILITY_ICONS = {
    CredibilityLevel.HIGH: "✅",
    CredibilityLevel.MEDIUM: "⚠️",
    CredibilityLevel.LOW: "❌",
    CredibilityLevel.UNKNOWN: "❓",
}


def format_result_plain(result: EvaluationResult) -> str:
    """Return a plain-text summary of an EvaluationResult.

    Args:
        result: The evaluation result to format.

    Returns:
        A multi-line string suitable for console output.
    """
    source = result.source
    lines = [
        f"Source : {source.title}",
        f"Author : {source.author or 'Unknown'}",
        f"Year   : {source.year or 'Unknown'}",
        f"Type   : {source.source_type.value}",
        f"Score  : {result.score:.2f} / 1.00",
        f"Level  : {result.credibility_level.value}",
    ]
    if result.flags:
        lines.append("Flags  : " + "; ".join(result.flags))
    lines.append(f"Summary: {result.summary}")
    return "\n".join(lines)


def format_result_markdown(result: EvaluationResult) -> str:
    """Return a Markdown-formatted summary of an EvaluationResult.

    Args:
        result: The evaluation result to format.

    Returns:
        A Markdown string with headers and bullet points.
    """
    source = result.source
    icon = _CREDIBILITY_ICONS.get(result.credibility_level, "❓")
    lines = [
        f"### {icon} {source.title}",
        "",
        f"| Field | Value |",
        f"|-------|-------|",
        f"| Author | {source.author or '_Unknown_'} |",
        f"| Year | {source.year or '_Unknown_'} |",
        f"| Type | {source.source_type.value} |",
        f"| Score | `{result.score:.2f}` / `1.00` |",
        f"| Credibility | **{result.credibility_level.value}** |",
    ]
    if source.url:
        lines.append(f"| URL | <{source.url}> |")
    lines.append("")
    lines.append(f"> {result.summary}")
    if result.flags:
        lines.append("")
        lines.append("**Flags:**")
        for flag in result.flags:
            lines.append(f"- {flag}")
    return "\n".join(lines)


def format_results_csv(results: Sequence[EvaluationResult]) -> str:
    """Serialize a list of EvaluationResults to CSV format.

    The CSV includes a header row followed by one row per result.
    Fields with commas are quoted automatically.

    Args:
        results: Sequence of evaluation results to serialize.

    Returns:
        A CSV string (including header) representing all results.
    """
    import csv
    import io

    fieldnames = [
        "title",
        "author",
        "year",
        "source_type",
        "score",
        "credibility_level",
        "flags",
        "url",
    ]

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=fieldnames, quoting=csv.QUOTE_MINIMAL)
    writer.writeheader()

    for result in results:
        src = result.source
        writer.writerow(
            {
                "title": src.title,
                "author": src.author or "",
                "year": src.year or "",
                "source_type": src.source_type.value,
                "score": f"{result.score:.4f}",
                "credibility_level": result.credibility_level.value,
                "flags": " | ".join(result.flags),
                "url": src.url or "",
            }
        )

    return output.getvalue()


def format_batch_summary(results: Sequence[EvaluationResult]) -> str:
    """Print a concise batch summary showing counts per credibility level.

    Args:
        results: Sequence of evaluation results.

    Returns:
        A short plain-text summary string.
    """
    counts: dict[str, int] = {level.value: 0 for level in CredibilityLevel}
    total_score = 0.0

    for result in results:
        counts[result.credibility_level.value] += 1
        total_score += result.score

    n = len(results)
    avg = total_score / n if n else 0.0

    lines = [f"Evaluated {n} source(s) — average score: {avg:.2f}"]
    for level in CredibilityLevel:
        icon = _CREDIBILITY_ICONS.get(level, "")
        lines.append(f"  {icon} {level.value}: {counts[level.value]}")
    return "\n".join(lines)
