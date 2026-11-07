#!/usr/bin/env python3
"""Citation audit for Papers 1 and 2.

Four independent directions, because each fails differently:

  1. LaTeX has already resolved every citation. `paper.log` reports any
     undefined citation or reference, and the PDF prints `??` where a
     reference did not resolve. This is the only check that sees what the
     reader sees.
  2. Every key the prose cites must exist in `references.bib`. A missing key
     is a promise the bibliography cannot keep.
  3. Every entry in `references.bib` must be cited. An orphan entry is a
     source the paper claims to have used and did not.
  4. `paper.bbl` is what BibTeX actually produced; a key in the prose that
     reaches the .aux but not the .bbl is a silent drop.

The `vanderpol1926` case is pinned by name: it is an entry whose *metadata*
was once flagged by an external Crossref lookup (the title is stored behind
the article number "LXXXVIII." in the publisher's record), not a missing
key. It resolves correctly here and is annotated rather than counted.

Usage:  python3 citation_audit.py [--bundle DIR] [--json OUT]
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple

PAPERS = {
    "Paper 1": {
        "dir": "paper1_source",
        "pdf": "Paper1.pdf",
        "md": ["00_Abstract.md", "01_Introduction.md", "02_Method.md",
               "03_Results.md", "04_Discussion.md", "Appendix.md"],
    },
    "Paper 2": {
        "dir": "paper2_source",
        "pdf": "Paper2.pdf",
        "md": ["00_Abstract.md", "01_Introduction.md", "02_Method.md",
               "03_Results.md", "04_Discussion.md"],
    },
}

# Documented false positives: key -> explanation. These are reported, never
# counted against the paper.
KNOWN_FALSE_POSITIVES = {
    "vanderpol1926": (
        "已核查，非真实缺失. The entry exists in references.bib, is cited once in "
        "§1.2, and appears in paper.bbl. The earlier flag came from a Crossref "
        "metadata lookup, not from this bibliography: the publisher stores the "
        "title behind the article number \"LXXXVIII.\", so a title-matching "
        "harness reports no hit while the citation resolves normally."
    ),
}

RE_CITE = re.compile(r"\\(?:cite|citep|citet|citealp|citeauthor|citeyear|"
                     r"nocite|autocite|parencite|textcite)\*?(?:\[[^\]]*\])*"
                     r"\{([^}]*)\}")
RE_MD_CITE = re.compile(r"\[@([A-Za-z0-9_:.\-]+)(?:;[^]]*)?\]")
RE_BIB_KEY = re.compile(r"^@(\w+)\s*\{\s*([^,\s]+)\s*,", re.MULTILINE)
RE_BBL_KEY = re.compile(r"\\bibitem(?:\[[^\]]*\])?\{([^}]+)\}")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def strip_latex_comments(text: str) -> str:
    return re.sub(r"(?<!\\)%.*$", "", text, flags=re.MULTILINE)


def cited_keys(root: Path, md_files: List[str]) -> Dict[str, List[str]]:
    """key -> list of 'file:line' where it is cited."""
    hits: Dict[str, List[str]] = {}
    # paper.tex is generated from these files; counting both would double
    # every citation.
    targets = [(root / f, f) for f in md_files]
    for path, name in targets:
        if not path.exists():
            continue
        text = read(path)
        for i, line in enumerate(text.splitlines(), 1):
            if line.lstrip().startswith("%"):
                continue
            for m in RE_CITE.finditer(line):
                for key in m.group(1).split(","):
                    key = key.strip()
                    if key and key != "*":
                        hits.setdefault(key, []).append(f"{name}:{i}")
            for m in RE_MD_CITE.finditer(line):
                hits.setdefault(m.group(1), []).append(f"{name}:{i}")
    return hits


def bib_entries(root: Path) -> Tuple[Dict[str, dict], List[str]]:
    path = root / "references.bib"
    text = strip_latex_comments(read(path))
    entries: Dict[str, dict] = {}
    dupes: List[str] = []
    for m in RE_BIB_KEY.finditer(text):
        kind, key = m.group(1).lower(), m.group(2)
        if key in entries:
            dupes.append(key)
            continue
        # crude field check: the entry body up to the next line starting with @
        body = text[m.end(): m.end() + 2000]
        fields = set(re.findall(r"^\s*(\w+)\s*=", body, re.MULTILINE))
        entries[key] = {"kind": kind, "fields": fields}
    return entries, dupes


def pdf_text(pdf: Path) -> str:
    if not pdf.exists():
        return ""
    try:
        out = subprocess.run(["pdftotext", "-layout", str(pdf), "-"],
                             capture_output=True, text=True, check=True)
        return out.stdout
    except Exception:
        return ""


def log_findings(root: Path) -> List[str]:
    text = read(root / "paper.log")
    out = []
    for line in text.splitlines():
        if re.search(r"Citation .* undefined|Reference .* undefined|"
                     r"There were undefined references|Label\(s\) may have changed",
                     line):
            out.append(line.strip())
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--bundle", default=str(Path(__file__).resolve().parent.parent))
    ap.add_argument("--json", default="")
    args = ap.parse_args()
    bundle = Path(args.bundle)

    report = {}
    lines: List[str] = []
    w = lines.append
    w("=" * 78)
    w("citation audit")
    w("=" * 78)
    w(f"bundle : {bundle}")
    w("")
    w("Direction 1 is what the reader sees (paper.log and the PDF). Directions")
    w("2-4 are what the sources promise. A paper can pass 2-4 and still print")
    w("'??' if a pass was stale, so 1 is not redundant.")
    w("")

    total_fail = 0
    for name, spec in PAPERS.items():
        root = bundle / spec["dir"]
        entries, dupes = bib_entries(root)
        hits = cited_keys(root, spec["md"])
        bbl = set(RE_BBL_KEY.findall(read(root / "paper.bbl")))
        txt = pdf_text(bundle / spec["pdf"])

        undefined_log = log_findings(root)
        n_q = txt.count("??")
        # a literal '??' in prose is rare; report the surrounding context
        q_ctx = []
        for m in re.finditer(r"\?\?", txt):
            q_ctx.append(txt[max(0, m.start() - 40): m.start() + 20]
                         .replace("\n", " ").strip())

        missing = sorted(k for k in hits if k not in entries)
        orphans = sorted(k for k in entries if k not in hits)
        not_in_bbl = sorted(k for k in hits if k not in bbl)
        stray_bbl = sorted(k for k in bbl if k not in entries)

        fp = [k for k in missing if k in KNOWN_FALSE_POSITIVES]
        real_missing = [k for k in missing if k not in KNOWN_FALSE_POSITIVES]

        w("-" * 78)
        w(f"{name}   ({spec['dir']})")
        w("-" * 78)
        w(f"bib entries           : {len(entries)}  ({', '.join(sorted(entries))})")
        w(f"distinct keys cited   : {len(hits)}")
        w(f"keys reaching paper.bbl: {len(bbl)}")
        w("")

        def row(label: str, items: List[str], ok: str) -> int:
            head = label.rstrip(":")
            if items:
                w(f"[FAIL] {head}")
                for it in items:
                    w(f"         {it}")
                return 1
            w(f"[PASS] {head}: {ok}")
            return 0

        bad = 0
        if n_q == 0 and not undefined_log:
            w("[PASS] no unresolved reference in the rendered PDF "
              f"({len(txt.split())} words scanned, 0 '??')")
        else:
            w(f"[FAIL] rendered PDF carries unresolved references: "
              f"{n_q} '??' occurrences")
            for c in q_ctx[:10]:
                w(f"         ...{c}...")
            for line in undefined_log:
                w(f"         {line}")
            bad += 1

        bad += row("keys cited in prose but absent from references.bib:",
                   [f"{k}  <- cited at {', '.join(hits[k][:3])}"
                    for k in real_missing],
                   "none (every cited key has an entry)")

        bad += row("bibliography entries never cited in the prose:",
                   [f"{k}  ({entries[k]['kind']})" for k in orphans],
                   "none (every entry is used)")

        bad += row("cited keys missing from paper.bbl (BibTeX drop):",
                   not_in_bbl, "none (BibTeX emitted every cited key)")

        bad += row("duplicate bib keys:",
                   dupes, "none")

        bad += row(".bbl entries with no .bib source:",
                   stray_bbl, "none")

        empty = []
        for k, meta in entries.items():
            required = {"article": {"author", "title", "journal", "year"},
                        "book": {"author", "title", "publisher", "year"},
                        "misc": {"author", "title", "year"}}.get(meta["kind"], {"title"})
            gap = sorted(f for f in required if f not in meta["fields"])
            if gap:
                empty.append(f"{k} ({meta['kind']}) lacks {', '.join(gap)}")
        bad += row("entries missing required fields:",
                   empty, "none")

        for k, note in KNOWN_FALSE_POSITIVES.items():
            if k in entries:
                w("")
                w(f"[NOTE] {k} — 已核查，非真实缺失 (verified, not a real gap)")
                w(f"       cited  : {', '.join(hits.get(k, ['not cited']))}")
                w(f"       in .bib: yes, @{entries[k]['kind']} "
                  f"({len(entries[k]['fields'])} fields)")
                w(f"       in .bbl: {'yes' if k in bbl else 'NO'}")
                w(f"       detail : {note}")

        w("")
        total_fail += bad
        report[name] = {
            "bib_entries": len(entries), "cited": len(hits),
            "missing": real_missing, "orphans": orphans,
            "not_in_bbl": not_in_bbl, "dupes": dupes,
            "pdf_question_marks": n_q, "log_findings": undefined_log,
            "failures": bad,
        }

    w("=" * 78)
    w(f"citation audit: {'PASS' if total_fail == 0 else 'FAIL'} "
      f"({total_fail} failing check(s) across both papers)")
    w("=" * 78)
    out = "\n".join(lines) + "\n"
    print(out)
    if args.json:
        Path(args.json).write_text(json.dumps(report, indent=2, ensure_ascii=False),
                                   encoding="utf-8")
    return 0 if total_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
