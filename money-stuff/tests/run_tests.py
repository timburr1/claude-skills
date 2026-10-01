"""Regression test for convert.py: convert each saved email (<name>.json) and compare with the
hand-made <name>.md. Spacing is normalized (the hand-made files have stray trailing/double spaces),
but line structure, indentation and text must match. Exit code 1 on any mismatch.

Usage: python run_tests.py
"""
import difflib, re, subprocess, sys, tempfile
from pathlib import Path

HERE = Path(__file__).parent
CONVERT = HERE.parent / "convert.py"


def norm(text):
    lines = text.replace("\r\n", "\n").split("\n")
    return [re.sub(r"(?<=\S) {2,}", " ", l).rstrip() for l in lines]


failed = 0
with tempfile.TemporaryDirectory() as out:
    for src in sorted(HERE.glob("*.json")):
        expected = src.with_suffix(".md")
        r = subprocess.run([sys.executable, str(CONVERT), str(src), "--outdir", out, "--force"],
                           capture_output=True, text=True)
        got = Path(out) / expected.name
        if r.returncode or not got.exists():
            print(f"FAIL {src.stem}: convert.py error\n{r.stdout}{r.stderr}")
            failed += 1
            continue
        raw = got.read_bytes()
        problems = []
        if b"\r\n" not in raw or raw.endswith(b"\n") or raw.startswith(b"\xef\xbb\xbf"):
            problems.append("file format (want CRLF, no trailing newline, no BOM)")
        diff = list(difflib.unified_diff(norm(expected.read_text(encoding="utf-8")),
                                         norm(raw.decode("utf-8")), "expected", "got", lineterm="", n=1))
        if diff:
            problems.append("content differs:\n" + "\n".join(diff[:40]))
        if problems:
            print(f"FAIL {src.stem}: " + "\n".join(problems))
            failed += 1
        else:
            print(f"ok   {src.stem}")

sys.exit(1 if failed else 0)
