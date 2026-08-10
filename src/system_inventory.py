#!/usr/bin/env python3
"""Collect a small, shareable system inventory using the Python standard library."""

from __future__ import annotations

import argparse
import json
import os
import platform
import shutil
import socket
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def total_memory_bytes() -> int | None:
    """Return physical memory when the operating system exposes it."""
    meminfo = Path("/proc/meminfo")
    if meminfo.exists():
        for line in meminfo.read_text(encoding="utf-8").splitlines():
            if line.startswith("MemTotal:"):
                return int(line.split()[1]) * 1024

    page_size = getattr(os, "sysconf", lambda _key: None)("SC_PAGE_SIZE")
    page_count = getattr(os, "sysconf", lambda _key: None)("SC_PHYS_PAGES")
    if isinstance(page_size, int) and isinstance(page_count, int):
        return page_size * page_count
    return None


def collect_inventory(disk_path: str = ".") -> dict[str, Any]:
    """Collect non-secret operating-system and capacity information."""
    disk = shutil.disk_usage(disk_path)
    return {
        "collected_at_utc": datetime.now(timezone.utc).isoformat(),
        "hostname": socket.gethostname(),
        "operating_system": {
            "name": platform.system(),
            "release": platform.release(),
            "architecture": platform.machine(),
        },
        "python_version": platform.python_version(),
        "logical_processors": os.cpu_count(),
        "memory_total_bytes": total_memory_bytes(),
        "disk": {
            "path": str(Path(disk_path).resolve()),
            "total_bytes": disk.total,
            "used_bytes": disk.used,
            "free_bytes": disk.free,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--disk-path", default=".", help="Path whose disk usage is reported")
    parser.add_argument("--output", type=Path, help="Optional JSON output file")
    args = parser.parse_args()

    rendered = json.dumps(collect_inventory(args.disk_path), indent=2)
    if args.output:
        args.output.write_text(rendered + "\n", encoding="utf-8")
        print(f"Inventory written to {args.output}")
    else:
        print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
