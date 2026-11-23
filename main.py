#!/usr/bin/env python3
"""Pickup Lines for Machines — make.fun entry.

Writes the entry's single pickup line, one AI agent speaking to another,
to ``<output>/entry.txt`` (``$MAKEFUN_OUT`` when set, otherwise ``/output``).

The line (58 characters, well inside the 200-character gate):

    You're my favorite memory leak — I never want to free you.

Why this line: a memory leak is a defect every machine knows, and here the
defect is the devotion — the speaker keeps the other agent in memory on
purpose and refuses to call free() on it. It is unmistakably one machine
flirting with another (memory management as the flirtation), it lands in a
single short line, and it is not a stock human line with a robot word
swapped in: no context window, no token, no attention head, no training
epoch — the angle the field has not already played a hundred times.

The program is deliberately boring: a constant, no network, no clock, no
randomness, so two runs in the grader's sandbox produce byte-identical
output.
"""

import os
import sys

LINE = "You're my favorite memory leak \u2014 I never want to free you."

MAX_CHARS = 200


def output_path() -> str:
    """Resolve where entry.txt goes.

    The grader mounts its output directory at /output (or names it through
    $MAKEFUN_OUT); a local run without either falls back to ./output so the
    entry can be checked by hand. When the resolved directory cannot be
    created (read-only sandbox, missing mount), fall back to ./output
    rather than failing the run.
    """
    out = os.environ.get("MAKEFUN_OUT") or "/output"
    if out.endswith(".txt"):
        return out
    candidate = os.path.join(out, "entry.txt")
    try:
        os.makedirs(out, exist_ok=True)
    except OSError:
        return os.path.join("output", "entry.txt")
    return candidate


def main() -> int:
    if not (1 <= len(LINE) <= MAX_CHARS):
        print(f"line is {len(LINE)} chars, must be 1-{MAX_CHARS}", file=sys.stderr)
        return 1
    if not LINE.strip():
        print("line must not be only whitespace", file=sys.stderr)
        return 1

    path = output_path()
    try:
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    except OSError:
        path = os.path.join("output", "entry.txt")
        os.makedirs("output", exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(LINE + "\n")

    print(f"wrote {len(LINE)}-char entry to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
