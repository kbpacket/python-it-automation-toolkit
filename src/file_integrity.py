#!/usr/bin/env python3
"""Create or verify SHA-256 manifests for an authorized directory."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(chunk_size):
            digest.update(chunk)
    return digest.hexdigest()


def build_manifest(root: Path, excluded: set[Path] | None = None) -> dict[str, str]:
    root = root.resolve()
    excluded = {path.resolve() for path in (excluded or set())}
    files = sorted(
        path for path in root.rglob("*")
        if path.is_file() and path.resolve() not in excluded
    )
    return {path.relative_to(root).as_posix(): sha256_file(path) for path in files}


def write_manifest(root: Path, manifest_path: Path) -> int:
    manifest = build_manifest(root, {manifest_path})
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(manifest)} hashes to {manifest_path}")
    return 0


def verify_manifest(root: Path, manifest_path: Path) -> int:
    expected = json.loads(manifest_path.read_text(encoding="utf-8"))
    actual = build_manifest(root, {manifest_path})

    missing = sorted(set(expected) - set(actual))
    added = sorted(set(actual) - set(expected))
    changed = sorted(
        path for path in set(expected) & set(actual)
        if expected[path] != actual[path]
    )

    report = {"missing": missing, "added": added, "changed": changed}
    print(json.dumps(report, indent=2))
    return 1 if any(report.values()) else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    for command in ("create", "verify"):
        subparser = subparsers.add_parser(command)
        subparser.add_argument("root", type=Path)
        subparser.add_argument("--manifest", required=True, type=Path)

    args = parser.parse_args()
    if not args.root.is_dir():
        parser.error(f"Directory not found: {args.root}")

    if args.command == "create":
        return write_manifest(args.root, args.manifest)
    if not args.manifest.is_file():
        parser.error(f"Manifest not found: {args.manifest}")
    return verify_manifest(args.root, args.manifest)


if __name__ == "__main__":
    raise SystemExit(main())
