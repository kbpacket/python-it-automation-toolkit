#!/usr/bin/env python3
"""Summarize logs formatted as YYYY-MM-DD HH:MM:SS LEVEL message."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any, Iterable

LOG_PATTERN = re.compile(
    r"^(?P<date>\d{4}-\d{2}-\d{2}) "
    r"(?P<time>\d{2}:\d{2}:\d{2}) "
    r"(?P<level>DEBUG|INFO|WARNING|ERROR|CRITICAL) "
    r"(?P<message>.+)$"
)


def summarize_lines(lines: Iterable[str], keyword: str | None = None) -> dict[str, Any]:
    levels: Counter[str] = Counter()
    parsed = 0
    invalid = 0
    keyword_matches = 0

    for raw_line in lines:
        line = raw_line.rstrip("\n")
        if not line:
            continue
        match = LOG_PATTERN.match(line)
        if not match:
            invalid += 1
            continue
        parsed += 1
        levels[match.group("level")] += 1
        if keyword and keyword.casefold() in match.group("message").casefold():
            keyword_matches += 1

    return {
        "parsed_lines": parsed,
        "invalid_lines": invalid,
        "levels": dict(sorted(levels.items())),
        "keyword": keyword,
        "keyword_matches": keyword_matches,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("log_file", type=Path)
    parser.add_argument("--keyword", help="Count case-insensitive message matches")
    args = parser.parse_args()

    if not args.log_file.is_file():
        parser.error(f"Log file not found: {args.log_file}")
    with args.log_file.open(encoding="utf-8") as handle:
        print(json.dumps(summarize_lines(handle, args.keyword), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
