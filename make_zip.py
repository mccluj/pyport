#!/usr/bin/env python

from __future__ import annotations

import fnmatch
import sys
import zipfile
from pathlib import Path


REPO_NAME = "trading-tools"

EXCLUDED_DIRS = {
    ".git",
    ".venv",
    ".idea",
    ".vscode",
    ".test-tmp",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "__pycache__",
    "htmlcov",
    "build",
    "dist",
}

EXCLUDED_DIR_PREFIXES = (
    ".test-tmp-",
    ".test-cache-",
)

EXCLUDED_FILES = {
    ".coverage",
    ".DS_Store",
    "Thumbs.db",
}

EXCLUDED_PATTERNS = (
    "*.pyc",
    "*.pyo",
    "*.log",
    "*.tmp",
    "*.bak",
    "*~",
)


def is_excluded_dir(name: str) -> bool:
    return (
        name in EXCLUDED_DIRS
        or any(name.startswith(prefix) for prefix in EXCLUDED_DIR_PREFIXES)
        or name.endswith(".egg-info")
    )


def should_exclude(path: Path, root: Path) -> bool:
    rel = path.relative_to(root)

    if any(is_excluded_dir(part) for part in rel.parts[:-1]):
        return True

    if path.is_dir():
        return is_excluded_dir(path.name)

    if path.name in EXCLUDED_FILES:
        return True

    if any(fnmatch.fnmatch(path.name, pattern) for pattern in EXCLUDED_PATTERNS):
        return True

    return False


def make_zip(root: Path, output: Path) -> int:
    root = root.resolve()
    output = output.resolve()

    if output.exists():
        output.unlink()

    count = 0

    with zipfile.ZipFile(
        output,
        mode="w",
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=9,
    ) as archive:
        for path in root.rglob("*"):
            if path.is_file() and not should_exclude(path, root):
                archive.write(path, path.relative_to(root))
                count += 1

    size_mb = output.stat().st_size / (1024 * 1024)

    print(f"Created: {output}")
    print(f"Files:   {count}")
    print(f"Size:    {size_mb:.1f} MB")

    return count


def main() -> int:
    root = Path.cwd().resolve()

    if root.name != REPO_NAME:
        print(
            f"Error: run this from the '{REPO_NAME}' repository root.",
            file=sys.stderr,
        )
        print(f"Current directory: {root}", file=sys.stderr)
        return 2

    output = root.parent / f"{REPO_NAME}.zip"

    make_zip(root, output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
