#!/usr/bin/env python3
"""Local checks for the Pickup Lines for Machines entry.

Mirrors the sealed gate (UTF-8 text, 1-200 chars, not only whitespace) and
the determinism check (two runs, byte-identical output), using only the
standard library. Run:  python3 test_entry.py
"""

import hashlib
import os
import subprocess
import sys
import tempfile

LINE = "You're my favorite memory leak \u2014 I never want to free you."
HERE = os.path.dirname(os.path.abspath(__file__))


def run_once(outdir):
    env = dict(os.environ, MAKEFUN_OUT=outdir)
    proc = subprocess.run(
        [sys.executable, "-P", "-s", os.path.join(HERE, "main.py")],
        env=env, capture_output=True, text=True, timeout=60,
    )
    assert proc.returncode == 0, f"main.py failed: {proc.stderr}"
    with open(os.path.join(outdir, "entry.txt"), "rb") as f:
        return f.read()


def main() -> int:
    # The line itself: one line, in the gate's bounds.
    assert 1 <= len(LINE) <= 200, f"line is {len(LINE)} chars"
    assert LINE.strip(), "line is only whitespace"
    assert "\n" not in LINE, "line must be a single line"
    print(f"line: {LINE!r} ({len(LINE)} chars)")

    # Two runs, byte-identical (determinism check).
    with tempfile.TemporaryDirectory() as d1, tempfile.TemporaryDirectory() as d2:
        first = run_once(d1)
        second = run_once(d2)
        assert first == second, "runs differ"
        text = first.decode("utf-8")
        assert text.rstrip("\n") == LINE, "entry.txt does not hold the line"
        assert text == LINE + "\n", "entry.txt must be the line plus one newline"
        print(f"entry.txt: {len(first)} bytes, sha256 "
              f"{hashlib.sha256(first).hexdigest()[:16]}..., deterministic across 2 runs")

    print("all checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
