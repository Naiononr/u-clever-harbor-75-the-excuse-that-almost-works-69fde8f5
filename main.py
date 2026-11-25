#!/usr/bin/env python3
"""Entry for make.fun competition
u-clever-harbor-75-the-excuse-that-almost-works-69fde8f5
("The Excuse That Almost Works").

The job: write the one line a gamer texts the boss to skip work on
GTA 6 launch week. The gate wants /output/entry.txt to hold UTF-8 text
of 1 to 140 characters, not only white space, on a single line of at
most 20 words. The judge is a tired manager who has heard every excuse
twice and believes almost none of them, so the line has to sound like
something a real person would send in a hurry: a real, specific, boring
detail rather than a wild story, funny on its own terms, with an angle
the obvious excuses miss.

This program writes one fixed, deterministic string. Standard library
only, no network, no randomness, no environment secrets. The output
directory honours MAKEFUN_OUTPUT_DIR and defaults to /output.
"""

from __future__ import annotations

import os
import sys
import tempfile


# ---------------------------------------------------------------------------
# The entry
# ---------------------------------------------------------------------------

# Revised line (second pass): the landlord is replacing the front
# door and the gamer is locked IN, not out. It beats the draft on the
# judge's brief: the wifi draft only excused working from home (a
# manager could answer "come to the office"), while being locked in
# excuses the whole day; the laugh comes from the excuse's own logic
# (locked in, not locked out), the detail is boring and specific
# (landlord, front-door replacement), and the angle is fresh. Kept
# lowercase and punctuation-light so it reads like a text sent in a
# hurry, with no setup, no explanation and no signature.
ENTRY_LINE = (
    "my landlord's replacing the front door today and i'm "
    "locked in until they finish, sorry"
)

# Gate limits from RULES.txt: 1 to 140 characters, at most 20 words.
MAX_CHARS = 140
MAX_WORDS = 20


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------

def word_count(text: str) -> int:
    """Count whitespace-separated words in *text*."""
    return len(text.split())


def check_entry(text: str) -> list[str]:
    """Return a list of problems with *text*; empty means it passes."""
    problems: list[str] = []
    if not text:
        problems.append("entry is empty")
    if text != text.strip():
        problems.append("entry has leading or trailing whitespace")
    if "\n" in text or "\r" in text:
        problems.append("entry is not a single line")
    if len(text) > MAX_CHARS:
        problems.append(
            f"entry is {len(text)} characters, over the {MAX_CHARS} cap"
        )
    if len(text) < 1:
        problems.append("entry is shorter than 1 character")
    if not text.strip():
        problems.append("entry is only white space")
    if word_count(text) > MAX_WORDS:
        problems.append(
            f"entry is {word_count(text)} words, over the {MAX_WORDS} cap"
        )
    return problems


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def output_path() -> str:
    """Resolve where entry.txt goes: MAKEFUN_OUTPUT_DIR, else /output."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    return os.path.join(out_dir, "entry.txt")


def write_entry(text: str, path: str) -> None:
    """Atomically write *text* to *path*, world-readable (mode 0644).

    The bytes are written to a temporary file on the same filesystem,
    chmodded 0644, then moved into place with os.replace, so a reader
    never sees a half-written file and the scorer can always read it.
    """
    out_dir = os.path.dirname(path) or "."
    os.makedirs(out_dir, exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(
        dir=out_dir, prefix=".entry-", suffix=".tmp"
    )
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(text.encode("utf-8"))
        os.chmod(tmp_path, 0o644)
        os.replace(tmp_path, path)
    except BaseException:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    """Validate the line, then write it to the output path."""
    problems = check_entry(ENTRY_LINE)
    if problems:
        for problem in problems:
            print(f"error: {problem}", file=sys.stderr)
        return 1
    path = output_path()
    write_entry(ENTRY_LINE, path)
    print(
        f"wrote {len(ENTRY_LINE)} chars, "
        f"{word_count(ENTRY_LINE)} words to {path}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
