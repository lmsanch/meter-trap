#!/usr/bin/env python3
"""
publish.py — Whitelist-gated publisher for the public meter-trap repo.

Copies ONLY approved artifacts from the private engine repo to the public
evidence repo. Files in publish directories that do not match the whitelist
are refused with a warning and the script exits with code 1.

Files outside the publish directories (e.g. sim/, data/, notebooks/) are
ignored entirely — they are part of the private engine and never published.

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

# Directories that publish from. Files inside these dirs are checked against
# the whitelist. Anything outside these dirs is ignored (private engine code).
PUBLISH_DIRS = {"figures", "register", "provenance", "predictions"}


def is_whitelisted(rel_path: str) -> bool:
    """Return True if the relative path matches any whitelist glob pattern."""
    rel_path = rel_path.replace("\\", "/")
    for pattern in WHITELIST:
        if fnmatch.fnmatch(rel_path, pattern):
            return True
    return False


def classify_files(source: Path) -> tuple[list[tuple[Path, str]], list[tuple[Path, str]]]:
    """Walk source and split files into (approved, refused).

    Only files in PUBLISH_DIRS or root-level whitelisted files are considered.
    Everything else is ignored.
    """
    approved = []
    refused = []

    for path in source.rglob("*"):
        if not path.is_file():
            continue
        if ".git" in path.parts:
            continue

        rel = path.relative_to(source).as_posix()
        top = rel.split("/")[0]

        # Root-level files (no directory component)
        if "/" not in rel:
            if is_whitelisted(rel):
                approved.append((path, rel))
            # Ignore root-level files not in whitelist (Makefile, etc.)
            continue

        # Files inside publish directories
        if top in PUBLISH_DIRS:
            if is_whitelisted(rel):
                approved.append((path, rel))
            else:
                refused.append((path, rel))
            continue

        # Files outside publish dirs — ignore (private engine code)

    return approved, refused


def publish(source: Path, dest: Path, dry_run: bool) -> int:
    """Copy whitelisted files from source to dest. Return 0 on success, 1 on refusal."""
    approved, refused = classify_files(source)

    if refused:
        print("\n=== REFUSED (in publish dir but not whitelisted) ===")
        for _, rel in sorted(refused, key=lambda x: x[1]):
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
