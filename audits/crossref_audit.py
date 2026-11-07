#!/usr/bin/env python3
"""Cross-reference audit for the two papers.

The document audit checks structure; this checks *naming*. Every claim of the
form "Theorem N", "Corollary N", "Proposition N", "Lemma N", "equation (a.b.c)"
or "section §a.b" is resolved against the set of objects the manuscript actually
defines, and anything that does not resolve is reported as FAIL rather than
warned about. A dangling "Corollary 5" is the cheapest way for a rewrite to
embarrass a paper, so it gets the same four-valued verdict as everything else.

Usage:
    python3 crossref_audit.py --paper1-dir DIR --paper2-dir DIR
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

PASS, FAIL = "PASS", "FAIL"

KINDS = ("Theorem", "Corollary", "Proposition", "Lemma")

# "**Theorem 3.**", "**Corollary 3$'$ (the uptake peak ...)**"
DEF_RE = re.compile(
    r"\*\*(" + "|".join(KINDS) + r")\s+(\d+)(\$'\$|\$''\$|['′]{0,2})"
)
TAG_RE = re.compile(r"\\tag\{([^}]+)\}")
# Many displays carry a hand-typed number on their own line: "\qquad (2.8.9)".
BARE_TAG_RE = re.compile(r"^\s*(?:\\qquad|\\quad)?\s*\((\d+(?:\.\d+){1,2})\)\s*$", re.M)
HEADING_RE = re.compile(r"^##\s+(\d+(?:\.\d+)*)\s", re.M)

# In-text references, primes included.
REF_RE = re.compile(
    r"\b(" + "|".join(KINDS) + r")\s+(\d+)(\$'\$|\$''\$|['′]{0,2})(?!s\b)"
)
EQREF_RE = re.compile(r"\((\d+\.\d+(?:\.\d+)?)(\$'\$|\$''\$|['′]{0,2})\)")
SECREF_RE = re.compile(r"§\s*(\d+(?:\.\d+)*)")

# Sections of *other* documents that the text cites by number. §6.2 of Paper 1
# is the section of the code-verification report where the audited implementation
# commits the factor-f error; it is not a section of the paper and cannot resolve
# against this manuscript's headings.
EXTERNAL_SECTIONS = {"6.2"}


def normalise(num: str, prime: str) -> str:
    p = prime.replace("$", "").replace("′", "'")
    return f"{num}{p}"


def scan(paths: list[Path]) -> tuple[set[str], set[str], set[str], str]:
    text = "\n".join(p.read_text(encoding="utf-8") for p in paths)
    defs = {f"{k} {normalise(n, pr)}" for k, n, pr in DEF_RE.findall(text)}
    tags = {normalise(t, "") for t in TAG_RE.findall(text)}
    tags |= set(BARE_TAG_RE.findall(text))
    heads = set(HEADING_RE.findall(text))
    return defs, tags, heads, text


def audit(name: str, paths: list[Path]) -> list[tuple[str, str, str]]:
    defs, tags, heads, text = scan(paths)
    out: list[tuple[str, str, str]] = []

    missing = []
    for kind, num, prime in REF_RE.findall(text):
        key = f"{kind} {normalise(num, prime)}"
        if key not in defs:
            missing.append(key)
    missing = sorted(set(missing))
    out.append((
        f"{name}: named results resolve",
        FAIL if missing else PASS,
        f"{len(defs)} defined; unresolved: {', '.join(missing) if missing else 'none'}",
    ))

    bad_eq = sorted({normalise(n, p) for n, p in EQREF_RE.findall(text)
                     if normalise(n, p) not in tags
                     and n.split(".")[0] in heads})
    out.append((
        f"{name}: equation numbers resolve",
        FAIL if bad_eq else PASS,
        f"{len(tags)} tags; unresolved: {', '.join(bad_eq) if bad_eq else 'none'}",
    ))

    def known(section: str) -> bool:
        return (section in heads
                or any(h.startswith(section + ".") for h in heads))

    bad_sec = sorted({s for s in SECREF_RE.findall(text)
                      if not known(s) and s not in EXTERNAL_SECTIONS})
    out.append((
        f"{name}: section references resolve",
        FAIL if bad_sec else PASS,
        f"{len(heads)} numbered sections; unresolved: {', '.join(bad_sec) if bad_sec else 'none'}",
    ))

    # Every definition should be referenced at least once beyond its own line.
    unreferenced = []
    refs = [f"{k} {normalise(n, pr)}" for k, n, pr in REF_RE.findall(text)]
    for d in sorted(defs):
        if refs.count(d) < 2:
            unreferenced.append(d)
    out.append((
        f"{name}: every named result is used",
        FAIL if unreferenced else PASS,
        f"orphans: {', '.join(unreferenced) if unreferenced else 'none'}",
    ))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--paper1-dir", required=True)
    ap.add_argument("--paper2-dir", required=True)
    a = ap.parse_args()

    rows = []
    for name, d in (("Paper 1", a.paper1_dir), ("Paper 2", a.paper2_dir)):
        paths = sorted(Path(d).glob("*.md"))
        if not paths:
            sys.exit(f"no markdown in {d}")
        rows += audit(name, paths)

    failed = [r for r in rows if r[1] == FAIL]
    print("=" * 78)
    print(f"cross-reference audit | checks: {len(rows)}   PASS: {len(rows)-len(failed)}   FAIL: {len(failed)}")
    print("=" * 78)
    for name, verdict, detail in rows:
        print(f"  {verdict:4}  {name:44} {detail}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
