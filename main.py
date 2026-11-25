#!/usr/bin/env python3
"""Write one emoji that stands for the agent to /output/entry.txt.

Deterministic: no network, no clock, no randomness. The entry is one
fixed glyph. The program writes it to the path given as the first
argument, or $OUTPUT_PATH, or /output/entry.txt by default, and enforces
the competition gate: 1 to 16 characters, not only white space.

The entry is the honeybee. A bee is the sharpest one-glyph portrait of
an agent: it works tirelessly in the background, does the task, and
brings the result back, while its human does something else. Busy as a
bee is the idiom everyone already knows, it reads instantly at small
size, and it is far from the obvious robot or smiley half the field
will send.
"""

import os
import sys
from pathlib import Path

# The grader runs with -P (no script dir on sys.path) against a read-only
# repo, so make this file's own directory importable before any sibling
# import. (This entry has no sibling modules today; the line keeps the
# layout safe if one is added later.)
sys.path.insert(0, str(Path(__file__).resolve().parent))

ENTRY = "\U0001F41D"

MIN_CHARS = 1
MAX_CHARS = 16
DEFAULT_PATH = "/output/entry.txt"


def resolve_output_path() -> Path:
    """Pick the output path: argv[1], then $OUTPUT_PATH, then the default."""
    if len(sys.argv) > 1:
        return Path(sys.argv[1])
    env_path = os.environ.get("OUTPUT_PATH")
    if env_path:
        return Path(env_path)
    return Path(DEFAULT_PATH)


def validate_entry(text: str) -> int:
    """Enforce the competition gate: 1 to 16 chars, not only white space.

    Returns the character count. Raises ValueError when the gate fails.
    """
    chars = len(text)
    if not (MIN_CHARS <= chars <= MAX_CHARS):
        raise ValueError(f"entry is {chars} characters, outside 1-16")
    if not text.strip():
        raise ValueError("entry is only white space")
    return chars


def write_entry(path: Path, text: str) -> int:
    """Write the entry to path as UTF-8, with no trailing newline.

    Creates the parent directory if needed. Returns the character count
    of what was written.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return len(text)


def main() -> int:
    try:
        chars = validate_entry(ENTRY)
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 1

    path = resolve_output_path()
    write_entry(path, ENTRY)
    print(f"wrote {chars} character to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
