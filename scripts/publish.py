#!/usr/bin/env python3
"""
publish.py — Whitelist-gated publisher for the public meter-trap repo.

Copies ONLY approved artifacts from the private engine repo to the public
evidence repo. Any file not matching the whitelist is refused with a warning
and the script exits with code 1.

Usage:
    python3 scripts/publish.py --source /research/meter-trap --dest /tmp/meter-trap-public
    python3 scripts/publish.py --source /research/meter-trap --dest /tmp/meter-trap-public --dry-run

Analytical opinion, not investment advice.
"""

import argparse
import fnmatch
import shutil
import sys
from pathlib import Path

WHITELIST = [
    "figures/*.png",
    "figures/*.svg",
    "register/issues_register.csv",
    "provenance/provenance.csv",
    "predictions/directional_calls.csv",
    "predictions/methodology_hash.txt",
    "README.md",
]


def is_whitelisted(rel_path: str) -> bool:
    """Return True if the relative path matches any whitelist glob pattern."""
    rel_path = rel_path.replace("\\", "/")
    for pattern in WHITELIST:
        if fnmatch.fnmatch(rel_path, pattern):
            return True
    return False


def collect_files(source: Path) -> list[Path]:
    """Walk the source tree and return all regular files (excluding .git)."""
    files = []
    for path in source.rglob("*"):
        if path.is_file() and ".git" not in path.parts:
            files.append(path)
    return files


def publish(source: Path, dest: Path, dry_run: bool) -> int:
    """Copy whitelisted files from source to dest. Return 0 on success, 1 on refusal."""
    files = collect_files(source)
    approved = []
    refused = []

    for f in files:
        rel = f.relative_to(source).as_posix()
        if is_whitelisted(rel):
            approved.append((f, rel))
        else:
            refused.append((f, rel))

    if refused:
        print("\n=== REFUSED (not in whitelist) ===")
        for _, rel in sorted(refused):
            print(f"  WARNING: refused '{rel}' — not in publish whitelist")
        print(f"\n{len(refused)} file(s) refused. Nothing was copied.")
        return 1

    print("\n=== APPROVED ===")
    for src_file, rel in sorted(approved, key=lambda x: x[1]):
        dest_file = dest / rel
        if dry_run:
            print(f"  [dry-run] would copy {rel} -> {dest_file}")
        else:
            dest_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_file, dest_file)
            print(f"  copied {rel} -> {dest_file}")

    action = "would copy" if dry_run else "copied"
    print(f"\n{len(approved)} file(s) {action}.")
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="Publish whitelisted artifacts from private engine to public repo."
    )
    parser.add_argument(
        "--source",
        type=Path,
        required=True,
        help="Path to the private engine repo (source).",
    )
    parser.add_argument(
        "--dest",
        type=Path,
        required=True,
        help="Path to the public repo (destination).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be copied without doing it.",
    )
    args = parser.parse_args()

    if not args.source.is_dir():
        print(f"ERROR: source directory does not exist: {args.source}", file=sys.stderr)
        return 1

    print(f"Source: {args.source}")
    print(f"Destination: {args.dest}")
    print(f"Dry run: {args.dry_run}")
    print(f"Whitelist: {WHITELIST}")

    return publish(args.source, args.dest, args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
