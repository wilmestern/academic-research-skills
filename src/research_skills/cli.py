"""Command-line interface for the academic research skills evaluator.

Provides a CLI entry point for evaluating research sources from the terminal.
Supports plain text, markdown, and CSV output formats.
"""

import argparse
import sys
from datetime import datetime
from typing import Optional

from .core import ResearchSource, SourceType
from .evaluator import evaluate_source
from .formatter import format_result_plain, format_result_markdown, format_results_csv


def parse_args(argv: Optional[list] = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        prog="research-skills",
        description="Evaluate the credibility of academic research sources.",
    )

    parser.add_argument("title", help="Title of the source")
    parser.add_argument("url", help="URL of the source")

    parser.add_argument(
        "--type",
        dest="source_type",
        choices=[t.value for t in SourceType],
        default=SourceType.WEBSITE.value,
        help="Type of source (default: website)",
    )
    parser.add_argument(
        "--author",
        default=None,
        help="Author of the source",
    )
    parser.add_argument(
        "--year",
        type=int,
        default=None,
        help="Publication year of the source",
    )
    parser.add_argument(
        "--peer-reviewed",
        action="store_true",
        default=False,
        help="Mark the source as peer-reviewed",
    )
    parser.add_argument(
        "--citations",
        type=int,
        default=0,
        help="Number of citations the source has received (default: 0)",
    )
    parser.add_argument(
        "--format",
        dest="output_format",
        choices=["plain", "markdown", "csv"],
        default="plain",
        help="Output format (default: plain)",
    )

    return parser.parse_args(argv)


def build_source(args: argparse.Namespace) -> ResearchSource:
    """Construct a ResearchSource from parsed CLI arguments."""
    pub_date: Optional[datetime] = None
    if args.year is not None:
        pub_date = datetime(args.year, 1, 1)

    return ResearchSource(
        title=args.title,
        url=args.url,
        source_type=SourceType(args.source_type),
        author=args.author,
        publication_date=pub_date,
        peer_reviewed=args.peer_reviewed,
        citation_count=args.citations,
    )


def main(argv: Optional[list] = None) -> int:
    """Main entry point for the CLI.

    Returns:
        Exit code (0 for success, 1 for error).
    """
    args = parse_args(argv)

    try:
        source = build_source(args)
    except ValueError as exc:
        print(f"Error building source: {exc}", file=sys.stderr)
        return 1

    result = evaluate_source(source)

    if args.output_format == "plain":
        print(format_result_plain(result))
    elif args.output_format == "markdown":
        print(format_result_markdown(result))
    elif args.output_format == "csv":
        # CSV includes a header row; write directly to stdout
        print(format_results_csv([result]))
    else:
        print(f"Unknown format: {args.output_format}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
