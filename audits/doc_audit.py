#!/usr/bin/env python3
"""Document-level consistency audit for the two papers.

Every check below is a claim about the manuscript that a machine can settle.
The verdicts are the four-valued ones the papers themselves use, because an
audit that invents its own scale has audited nothing:

    PASS     the check ran against a witness and the claim holds
    FAIL     the check ran against a witness and the claim fails
    INVALID  no witness could be obtained -- nothing to examine, which is not
             the same finding as refuted

A check that cannot run is never reported as PASS.

Usage:
    python3 doc_audit.py --paper1-dir DIR --paper2-dir DIR [--json OUT]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

PASS, FAIL, INVALID = "PASS", "FAIL", "INVALID"


@dataclass
class Check:
    name: str
    verdict: str
    detail: str
    items: list = field(default_factory=list)


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def strip_comments(tex: str) -> str:
    return re.sub(r"(?<!\\)%.*", "", tex)


# --------------------------------------------------------------------------
# LaTeX structural checks
# --------------------------------------------------------------------------

def check_braces(tex: str, label: str) -> Check:
    body = strip_comments(tex)
    o, c = body.count("{"), body.count("}")
    if o == c:
        return Check(f"{label}: brace balance", PASS, f"{o} open / {c} close")
    return Check(f"{label}: brace balance", FAIL, f"{o} open / {c} close")


def check_display_math(tex: str, label: str) -> Check:
    body = strip_comments(tex)
    # `\\[2pt]` is a row break with an optional argument, not display math.
    opens = len(re.findall(r"(?<!\\)\\\[", body)) + body.count(r"\begin{equation}")
    closes = len(re.findall(r"(?<!\\)\\\]", body)) + body.count(r"\end{equation}")
    if opens == closes:
        return Check(f"{label}: display-math pairing", PASS,
                     f"{opens} open / {closes} close")
    return Check(f"{label}: display-math pairing", FAIL,
                 f"{opens} open / {closes} close")


def check_duplicate_tags(tex: str, label: str) -> Check:
    tags = re.findall(r"\\tag\{([^}]*)\}", tex)
    if not tags:
        return Check(f"{label}: equation tag uniqueness", INVALID,
                     "no \\tag in this document")
    seen, dup = set(), []
    for t in tags:
        if t in seen and t not in dup:
            dup.append(t)
        seen.add(t)
    if dup:
        return Check(f"{label}: equation tag uniqueness", FAIL,
                     f"{len(tags)} tags, {len(dup)} duplicated", dup)
    return Check(f"{label}: equation tag uniqueness", PASS,
                 f"{len(tags)} tags, all unique")


def check_labels(tex: str, label: str) -> Check:
    body = strip_comments(tex)
    defined = [m for m in re.findall(r"\\label\{([^}]*)\}", body)]
    refs = re.findall(r"\\(?:ref|eqref|autoref)\{([^}]*)\}", body)
    if not refs:
        return Check(f"{label}: label/ref resolution", INVALID,
                     f"{len(defined)} labels defined, 0 references: nothing to resolve")
    undefined = sorted({r for r in refs if r not in defined})
    if undefined:
        return Check(f"{label}: label/ref resolution", FAIL,
                     f"{len(undefined)} undefined", undefined)
    return Check(f"{label}: label/ref resolution", PASS,
                 f"{len(refs)} references resolve")


def check_undefined_marker(tex: str, label: str) -> Check:
    body = strip_comments(tex)
    hits = body.count("??")
    if hits == 0:
        return Check(f"{label}: no '??' placeholder", PASS, "0 occurrences")
    return Check(f"{label}: no '??' placeholder", FAIL, f"{hits} occurrences")


def manual_titles(tex: str) -> dict:
    """Numbered float titles typed as prose rather than typeset by LaTeX."""
    body = strip_comments(tex)
    out = {}
    for kind in ("Figure", "Table"):
        for n in re.findall(rf"^\\?(?:textbf\{{)?{kind}\s+(\d+)[.:]", body, re.M):
            out.setdefault(kind, set()).add(int(n))
    return out


def check_floats(tex: str, label: str) -> Check:
    body = strip_comments(tex)
    figs = len(re.findall(r"\\begin\{figure\}", body))
    longs = len(re.findall(r"\\begin\{longtable\}", body))
    tabs = len(re.findall(r"\\begin\{table\}", body))
    unnumbered = len(re.findall(r"LTcaptype\{none\}", body))
    caps = len(re.findall(r"\\caption\{", body))
    manual = manual_titles(body)
    numbered_tabs = tabs + len(manual.get("Table", ()))

    detail = (f"{figs} figure env with {caps} \\caption; "
              f"{tabs + longs} table env, of which {numbered_tabs} carry a number "
              f"(hand-typed title) and {tabs + longs - numbered_tabs} carry none")
    return Check(f"{label}: float numbering apparatus", INVALID, detail)


def float_occurrences(pdf_text: str, kind: str, n: int) -> int:
    """How many times float `n` of `kind` is named in the page text."""
    return len(re.findall(rf"\b{kind}s?\s+{n}\b", pdf_text))


def check_float_references(tex: str, pdf_text: str, label: str) -> Check:
    """Every numbered float must be spoken of in the prose, not only titled."""
    body = strip_comments(tex)
    manual = manual_titles(body)
    figs = len(re.findall(r"\\begin\{figure\}", body))
    tabs = len(re.findall(r"\\begin\{table\}", body))
    text = pdf_text.replace("\f", "\n")
    missing = []

    for kind, auto_count in (("Figure", figs), ("Table", tabs)):
        nums = set(range(1, auto_count + 1)) | set(manual.get(kind, ()))
        for n in sorted(nums):
            # one hit == the title itself; a reference adds at least one more
            if float_occurrences(text, kind, n) < 2:
                missing.append(f"{kind} {n}")

    if figs == 0 and tabs == 0 and not manual:
        return Check(f"{label}: float references", INVALID, "no numbered floats")
    if missing:
        return Check(f"{label}: float references", FAIL,
                     f"{len(missing)} numbered float(s) never referenced in prose",
                     missing)
    return Check(f"{label}: float references", PASS,
                 "every numbered float is named in the prose")


def check_float_numbering(pdf_text: str, label: str) -> Check:
    text = pdf_text.replace("\f", "\n")
    problems, summary = [], []
    for kind in ("Figure", "Table"):
        seq = [int(n) for n in re.findall(
            rf"^[ \t]*{kind}\s+(\d+)[.:]", text, re.M)]
        if not seq:
            continue
        uniq = sorted(set(seq))
        summary.append(f"{kind} 1..{len(uniq)}")
        if uniq != list(range(1, len(uniq) + 1)):
            problems.append(f"{kind} numbers {uniq} are not 1..{len(uniq)}")
    if not summary:
        return Check(f"{label}: float numbering", INVALID,
                     "no captions or titles detected in the PDF text")
    if problems:
        return Check(f"{label}: float numbering", FAIL, "; ".join(problems))
    return Check(f"{label}: float numbering", PASS,
                 ", ".join(summary) + ", contiguous")


# --------------------------------------------------------------------------
# Citation checks
# --------------------------------------------------------------------------

def bib_keys(bib: str) -> set:
    return set(re.findall(r"^@\w+\{([^,]+),", bib, re.M))


def check_citations(tex: str, bib_path: Path, label: str) -> Check:
    body = strip_comments(tex)
    cited = set()
    for group in re.findall(r"\\cite[a-zA-Z]*\*?\{([^}]*)\}", body):
        for k in group.split(","):
            cited.add(k.strip())
    if not bib_path.exists():
        return Check(f"{label}: citation coverage", INVALID,
                     f"no .bib at {bib_path.name}: {len(cited)} \\cite keys, "
                     f"no witness to resolve them against")
    keys = bib_keys(read(bib_path))
    missing = sorted(cited - keys)
    orphans = sorted(keys - cited)
    if missing or orphans:
        detail = (f"{len(cited)} cited / {len(keys)} in bib"
                  f"; {len(missing)} missing, {len(orphans)} orphan")
        return Check(f"{label}: citation coverage", FAIL, detail,
                     ([f"missing:{k}" for k in missing] +
                      [f"orphan:{k}" for k in orphans]))
    return Check(f"{label}: citation coverage", PASS,
                 f"{len(cited)} cited = {len(keys)} in bib, no orphans, no gaps")


def check_citation_presence(tex: str, label: str) -> Check:
    body = strip_comments(tex)
    n = len(re.findall(r"\\cite[a-zA-Z]*\*?\{", body))
    if n == 0:
        return Check(f"{label}: has literature", INVALID,
                     "0 citations and no bibliography: no prior work is engaged")
    return Check(f"{label}: has literature", PASS, f"{n} citation call(s)")


# --------------------------------------------------------------------------
# Markdown source checks (paper 2 is generated from markdown)
# --------------------------------------------------------------------------

def check_md_math(md: str, label: str) -> Check:
    fences = len(re.findall(r"^\$\$", md, re.M))
    if fences % 2 == 0:
        return Check(f"{label}: markdown math fences", PASS, f"{fences} $$ (even)")
    return Check(f"{label}: markdown math fences", FAIL, f"{fences} $$ (odd)")


def check_md_tables(md: str, label: str) -> Check:
    bad = []
    lines = md.split("\n")
    i = 0
    while i < len(lines):
        if lines[i].startswith("|"):
            j, block = i, []
            while j < len(lines) and lines[j].startswith("|"):
                block.append(lines[j])
                j += 1
            counts = {l.count("|") for l in block}
            if len(counts) > 1:
                bad.append(f"line {i+1}: pipe counts {sorted(counts)}")
            i = j
        else:
            i += 1
    if bad:
        return Check(f"{label}: markdown table shape", FAIL,
                     f"{len(bad)} malformed block(s)", bad)
    return Check(f"{label}: markdown table shape", PASS, "all blocks rectangular")


def check_placeholders(md: str, label: str) -> Check:
    pats = ["TODO", "FIXME", "XXX", "TKTK", "[ref]", "PLACEHOLDER"]
    hits = [(p, md.count(p)) for p in pats if md.count(p)]
    if hits:
        return Check(f"{label}: no placeholder text", FAIL,
                     ", ".join(f"{p}x{n}" for p, n in hits))
    return Check(f"{label}: no placeholder text", PASS, "0 placeholders")


# --------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--paper1-dir", required=True, type=Path)
    ap.add_argument("--paper2-dir", required=True, type=Path)
    ap.add_argument("--json", type=Path, default=None)
    args = ap.parse_args()

    p1, p2 = args.paper1_dir, args.paper2_dir
    checks: list[Check] = []

    t1 = read(p1 / "paper.tex")
    t2 = read(p2 / "paper.tex")
    pdf1 = read(p1 / "_audit_p1.txt") if (p1 / "_audit_p1.txt").exists() else ""
    pdf2 = read(p2 / "_audit_p2.txt") if (p2 / "_audit_p2.txt").exists() else ""

    checks += [check_braces(t1, "Paper 1"), check_display_math(t1, "Paper 1"),
               check_duplicate_tags(t1, "Paper 1"), check_labels(t1, "Paper 1"),
               check_undefined_marker(t1, "Paper 1"), check_floats(t1, "Paper 1")]
    if pdf1:
        checks += [check_float_references(t1, pdf1, "Paper 1"),
                   check_float_numbering(pdf1, "Paper 1")]
    else:
        checks.append(Check("Paper 1: float references", INVALID, "no PDF text extracted"))
    checks += [check_citation_presence(t1, "Paper 1"),
               check_citations(t1, p1 / "references.bib", "Paper 1")]

    checks += [check_braces(t2, "Paper 2"), check_display_math(t2, "Paper 2"),
               check_duplicate_tags(t2, "Paper 2"), check_labels(t2, "Paper 2"),
               check_undefined_marker(t2, "Paper 2"), check_floats(t2, "Paper 2")]
    if pdf2:
        checks += [check_float_references(t2, pdf2, "Paper 2"),
                   check_float_numbering(pdf2, "Paper 2")]
    else:
        checks.append(Check("Paper 2: float references", INVALID, "no PDF text extracted"))
    checks += [check_citation_presence(t2, "Paper 2"),
               check_citations(t2, p2 / "references.bib", "Paper 2")]

    for src in ("00_Abstract.md", "01_Introduction.md", "02_Method.md",
                "03_Results.md", "04_Discussion.md"):
        f = p2 / src
        if not f.exists():
            checks.append(Check(f"Paper 2: {src} present", FAIL, "missing"))
            continue
        md = read(f)
        checks += [check_md_math(md, f"Paper 2 / {src}"),
                   check_md_tables(md, f"Paper 2 / {src}"),
                   check_placeholders(md, f"Paper 2 / {src}")]

    counts = {PASS: 0, FAIL: 0, INVALID: 0}
    for c in checks:
        counts[c.verdict] += 1

    print("=" * 78)
    print(f"document audit | checks: {len(checks)}   "
          f"PASS: {counts[PASS]}   FAIL: {counts[FAIL]}   INVALID: {counts[INVALID]}")
    print("=" * 78)
    for verdict in (FAIL, INVALID, PASS):
        subset = [c for c in checks if c.verdict == verdict]
        if not subset:
            continue
        print(f"\n{verdict} ({len(subset)})")
        for c in subset:
            print(f"  {c.name:<52} {c.detail}")
            for it in c.items[:8]:
                print(f"      - {it}")
            if len(c.items) > 8:
                print(f"      ... {len(c.items) - 8} more")

    if args.json:
        args.json.write_text(json.dumps(
            [{"check": c.name, "verdict": c.verdict, "detail": c.detail,
              "items": c.items} for c in checks], indent=2), encoding="utf-8")

    return 1 if counts[FAIL] else 0


if __name__ == "__main__":
    sys.exit(main())
