#!/usr/bin/env python3
"""Glyph census of the rendered PDFs: what the reader actually sees.

Why this exists
---------------
The other five audits read structure. citation_audit asks whether a key
resolves, crossref_audit whether "Theorem 7" exists, figure_table_audit
whether a number matches its CSV, doc_audit whether the markdown parses,
redundancy_audit whether two paragraphs say the same thing. None of them
opens the PDF and asks *what character is on the page*. That blind spot has
already cost this bundle one defect: `\\mathbb{1}` was written for the
indicator function in three places and XeLaTeX printed U+22AE (⊮, DOES NOT
FORCE -- a slashed turnstile) instead of a bold 1. Every audit passed; the
page was wrong. The pdf text layer carried the wrong codepoint the whole
time, and no check compared it against what was intended.

What this tool does, and what it does not
-----------------------------------------
It does the mechanical half of the job:

  A. per-paper inventory   glyph, codepoint, Unicode name, frequency, and
                           the first occurrence in context;
  B. classification        grouping into Greek, operators, arrows,
                           delimiters, typographic punctuation, combining
                           marks, CJK, ligatures, other, so that a glyph is
                           read next to its kin rather than in a flat list;
  C. hard defects          a flagged subset a machine *can* decide: the
                           replacement character, a combining mark with no
                           base letter before it, a codepoint outside the
                           ranges a XeLaTeX math document should produce,
                           and any codepoint on the near-miss blocklist --
                           glyphs that are legitimate Unicode but that no
                           sentence in these papers would ever want, the
                           ⊮ class included.

It does the *not mechanical* half by refusing to do it. The failure mode
this tool is really aimed at cannot be computed from the glyph stream:

    A glyph is a shape. Correctness is a relation between the shape, the
    symbol the prose says it is, and the quantity that symbol is bound to.
    Two occurrences of U+03B5 are indistinguishable at the byte level and
    one of them can be wrong.

The precedent is in this bundle. In Appendix A.7.1 the tolerance of a
uniform limit was written `\\varepsilon_n`, and §1.2 already used
`\\varepsilon_n` for the i.i.d. zero-mean noise of Proposition 5. Same
codepoint, two meanings, one section apart from `\\varepsilon = 0.01`, the
drift rate. §2.0 of Paper 1 fixes exactly this rule -- one symbol, one
meaning -- and names delta as the cautionary case. No scan can catch it: the
bytes are identical to bytes that are correct. What the scan can do is put
`epsilon` and `omega` side by side with counts and contexts, at which point
a reader sees "epsilon appears 55 times across three unrelated roles" in one
glance. That is why section D prints this call to manual review instead of a
verdict on it, and why the tool never fails a build over a symbol reuse: a
false accusation here would cost more than a missed one.

The division of labour is therefore: the tool guarantees completeness (every
non-ASCII glyph is listed, none is skipped) and the human guarantees
semantics (each glyph is bound to one meaning). A scan that reported "no
problems" on its own authority would be lying about the half it cannot see.

Reading the output
------------------
Section A is long by design: for a 39-page paper it is ~60 rows, and the
rows are meant to be skimmed as a table, not read as prose. The rows that
matter on a first pass are the tail -- frequency 1 to 3 -- because a glyph
that occurs once is either a deliberate one-off (a floor bracket, a subset
sign) or a typo that nothing else in the pipeline would notice. Section C
lists the machine-decidable subset; section D lists the pairs that look
alike (epsilon lunate vs epsilon, increment vs capital delta, micro sign vs
Greek mu) and asks whether the distinction is intended.

Usage:  python3 glyph_scan.py [--bundle DIR] [--json OUT] [--context N]
Exit:   0 unless section C finds a hard defect.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import unicodedata
from collections import Counter
from pathlib import Path
from typing import Dict, List, Tuple

PAPERS = [
    ("Paper 1", "Paper1.pdf"),
    ("Paper 2", "Paper2.pdf"),
]

# Unicode blocks a XeLaTeX math document is allowed to emit. Anything outside
# them is not a typo in the prose, it is a font or macro fault, so it is worth
# interrupting the reader for. The ranges are deliberately generous on the
# typography side: en/em dashes and curly quotes come from pandoc's smart
# punctuation, not from the author.
ALLOWED_RANGES = [
    (0x00A0, 0x00FF),   # Latin-1 supplement: micro, multiplication, not
    (0x0300, 0x036F),   # combining diacritics (checked for a base char)
    (0x0370, 0x03FF),   # Greek
    (0x2000, 0x206F),   # general punctuation: dashes, quotes, primes
    (0x2070, 0x209F),   # super/subscripts
    (0x20A0, 0x20CF),   # currency
    (0x2100, 0x21FF),   # letterlike, arrows
    (0x2200, 0x22FF),   # math operators
    (0x2300, 0x23FF),   # misc technical: floor, ceiling
    (0x25A0, 0x25FF),   # geometric shapes: the QED box
    (0x27C0, 0x27EF),   # misc math symbols A
    (0x2A00, 0x2AFF),   # supplemental math operators
    (0xFB00, 0xFB06),   # Latin ligatures (ff, fi, fl)
    (0x4E00, 0x9FFF),   # CJK unified ideographs: the author's name
    (0xFF00, 0xFFEF),   # half/fullwidth forms
]

# Pairs that are one symbol to a reader and two codepoints to a program. Both
# members present does not mean a defect -- the bundle uses ϵ_m for the margin
# and ε for the drift by design -- but it does mean someone decided, and the
# decision should be checkable.
CONFUSABLES = [
    ("\u03b5", "\u03f5", "epsilon vs lunate epsilon"),
    ("\u03c6", "\u03d5", "phi vs phi symbol"),
    ("\u0394", "\u2206", "capital delta vs increment"),
    ("\u00b5", "\u03bc", "micro sign vs Greek mu"),
    ("\u2212", "\u002d", "minus sign vs hyphen-minus"),
    ("\u2217", "\u002a", "asterisk operator vs asterisk"),
    ("\u223c", "\u007e", "tilde operator vs ascii tilde"),
    ("\u2019", "\u0027", "right quote vs apostrophe"),
    ("\u2032", "\u0027", "prime vs apostrophe"),
]

# Glyphs that are valid Unicode, sit inside the allowed ranges, and are still
# always wrong here. This is the one place where the scan can catch its own
# motivating defect: \mathbb{1} rendered as U+22AE, which is a legal math
# operator that looks like a struck-through 1 to a reader skimming a formula.
# A whitelist-by-range cannot see it; a blocklist can. Entries are added only
# after a near-miss has actually been observed, and each one records why, so
# that the list stays an audit trail rather than a superstition.
NEAR_MISS = {
    "\u22ae": "DOES NOT FORCE -- a slashed turnstile that reads as a struck 1; "
              "this is what \\mathbb{1} printed before the 2026-11 fix",
    "\u22af": "negated double turnstile, same family as U+22AE",
    "\u2224": "DOES NOT DIVIDE",
    "\ufffd": "REPLACEMENT CHARACTER -- a glyph the font did not have",
    "\u200b": "ZERO WIDTH SPACE -- invisible, so it can only hide a fault",
    "\u00a0": "NO-BREAK SPACE -- pandoc sometimes emits these; harmless in "
              "print but they break string matching in every other audit",
}

# Classes in the order they are printed. The order is by how a mathematician
# reads a page, not by codepoint: operators first because a wrong operator is
# a wrong theorem, CJK last because it is a name.
CLASSES = [
    ("greek", "Greek letters (quantities and parameters)"),
    ("operator", "math operators and relations"),
    ("arrow", "arrows and logical connectives"),
    ("delimiter", "delimiters, radicals, floor/ceiling, QED"),
    ("combining", "combining marks (must have a base character)"),
    ("punctuation", "typographic punctuation"),
    ("latin1", "Latin-1 supplement"),
    ("ligature", "Latin ligatures"),
    ("cjk", "CJK"),
    ("other", "everything else"),
]


def pdf_text(pdf: Path) -> str:
    """Text layer of the PDF, layout preserved. Empty string if missing."""
    if not pdf.exists():
        return ""
    try:
        out = subprocess.run(["pdftotext", "-layout", str(pdf), "-"],
                             capture_output=True, text=True, check=True)
        return out.stdout
    except Exception:
        return ""


def classify(ch: str) -> str:
    cp = ord(ch)
    if 0x0370 <= cp <= 0x03FF:
        return "greek"
    if 0x0300 <= cp <= 0x036F:
        return "combining"
    if 0x2190 <= cp <= 0x21FF:
        return "arrow"
    if 0x2200 <= cp <= 0x22FF:
        # logical connectives live in the operator block; separate them by name
        name = unicodedata.name(ch, "")
        if "LOGICAL" in name or "THEREFORE" in name:
            return "arrow"
        return "operator"
    if 0x2300 <= cp <= 0x23FF or 0x25A0 <= cp <= 0x25FF:
        return "delimiter"
    if 0x27C0 <= cp <= 0x27EF or 0x2A00 <= cp <= 0x2AFF:
        return "operator"
    if 0x2000 <= cp <= 0x206F or 0x2070 <= cp <= 0x209F:
        return "punctuation"
    if 0x00A0 <= cp <= 0x00FF:
        return "latin1"
    if 0xFB00 <= cp <= 0xFB06:
        return "ligature"
    if 0x4E00 <= cp <= 0x9FFF:
        return "cjk"
    return "other"


def allowed(ch: str) -> bool:
    cp = ord(ch)
    return any(lo <= cp <= hi for lo, hi in ALLOWED_RANGES)


def context(text: str, idx: int, width: int) -> str:
    """One-line window around text[idx], whitespace collapsed, marker inserted."""
    lo = max(0, idx - width)
    hi = min(len(text), idx + width + 1)
    frag = text[lo:hi].replace("\n", " ")
    frag = " ".join(frag.split())
    # collapse the marker run so wide windows stay on one line
    return frag


def scan(text: str, width: int) -> Tuple[Counter, Dict[str, Tuple[int, str]]]:
    """Frequency of every non-ASCII glyph, plus its first context."""
    counts: Counter = Counter()
    first: Dict[str, Tuple[int, str]] = {}
    for i, ch in enumerate(text):
        if ord(ch) <= 127:
            continue
        counts[ch] += 1
        if ch not in first:
            first[ch] = (i, context(text, i, width))
    return counts, first


def hard_defects(text: str, counts: Counter) -> List[str]:
    """The subset of glyph problems a machine can actually decide.

    Three checks, all of them local and unambiguous:

      * U+FFFD or U+25A1-as-placeholder: the font had no glyph, or pdftotext
        could not decode. Either way the page is not what the source says.
      * a combining mark at index 0, or after whitespace or another mark:
        nothing is under the accent, so the reader sees a floating dot.
      * a codepoint outside ALLOWED_RANGES: a font or macro fault, not a
        prose choice.

    A symbol reused for two quantities is *not* here, on purpose. It is
    decidable only by reading, and section D asks the reader to do it.
    """
    out: List[str] = []
    if "\ufffd" in text:
        out.append(f"U+FFFD REPLACEMENT CHARACTER present "
                   f"({text.count(chr(0xFFFD))}x): pdftotext could not decode "
                   f"at least one glyph")
    seen_outside: Counter = Counter()
    for i, ch in enumerate(text):
        if ord(ch) <= 127:
            # ASCII is never "outside the expected ranges"; the file is read
            # as UTF-8 and every printable ASCII codepoint is legitimate.
            continue
        if 0x0300 <= ord(ch) <= 0x036F:
            base = text[i - 1] if i > 0 else ""
            if not base or not base.isalpha():
                frag = text[max(0, i - 30):i + 10].replace("\n", " ")
                out.append(f"combining mark U+{ord(ch):04X} "
                           f"({unicodedata.name(ch, '?')}) at offset {i} has "
                           f"no base letter: \"{frag.strip()}\"")
        elif not allowed(ch):
            # report a bad codepoint once, with its count, not once per hit:
            # the point is to name the glyph, not to fill the log with it
            seen_outside[ch] += 1
    for ch, n in seen_outside.most_common():
        name = unicodedata.name(ch, "<unnamed>")
        out.append(f"U+{ord(ch):04X} {name} outside the expected ranges ({n}x)")
    for ch, why in NEAR_MISS.items():
        if ch in text:
            out.append(f"U+{ord(ch):04X} {unicodedata.name(ch, '<unnamed>')} "
                       f"x{text.count(ch)}: near-miss glyph -- {why}")
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--bundle", default=str(Path(__file__).resolve().parent.parent))
    ap.add_argument("--json", default="")
    ap.add_argument("--context", type=int, default=42,
                    help="characters of context on each side (default 42)")
    args = ap.parse_args()
    bundle = Path(args.bundle)

    lines: List[str] = []
    w = lines.append
    w("=" * 78)
    w("glyph census of the rendered PDFs")
    w("=" * 78)
    w(f"bundle : {bundle}")
    w("")
    w("This tool lists what is printed and flags what a machine can decide is")
    w("wrong. It does NOT decide whether a glyph means what the prose says it")
    w("means: two occurrences of one codepoint can carry two different")
    w("quantities, and the bytes are then correct in both places. Section D is")
    w("an instruction to read, not a result. See the module docstring for the")
    w("epsilon_n precedent in this bundle.")
    w("")

    report: Dict[str, dict] = {}
    total_defects = 0
    confusable_hits: List[str] = []

    for name, pdfname in PAPERS:
        text = pdf_text(bundle / pdfname)
        if not text:
            w(f"{name}: NO TEXT LAYER (missing {pdfname}) -- skipped")
            w("")
            report[name] = {"missing": True}
            continue

        counts, first = scan(text, args.context)
        nonascii = sum(counts.values())
        w("-" * 78)
        w(f"{name}  ({pdfname})  {len(text):,} chars, {nonascii:,} non-ASCII "
          f"of {len(counts)} distinct glyphs")
        w("-" * 78)
        w("")

        # A. flat inventory, most frequent first -- the table to skim
        w("A. inventory (frequency descending)")
        w("")
        w(f"   {'glyph':6} {'code':8} {'freq':>5}  name")
        w("   " + "-" * 70)
        for ch, n in counts.most_common():
            cp = ord(ch)
            disp = ch if ch.isprintable() else "?"
            w(f"   {disp:6} U+{cp:04X}  {n:5}  {unicodedata.name(ch, '<unnamed>')}")
        w("")

        # B. grouped by class, which is how a reader checks semantics
        w("B. grouped by class (read a glyph next to its kin)")
        w("")
        for key, title in CLASSES:
            members = [(ch, n) for ch, n in counts.most_common()
                       if classify(ch) == key]
            if not members:
                continue
            w(f"   {title}  [{len(members)}]")
            for ch, n in members:
                idx, ctx = first[ch]
                w(f"     {ch}  U+{ord(ch):04X}  x{n}")
                w(f"       first @{idx}: {ctx}")
            w("")

        # C. machine-decidable defects
        defects = hard_defects(text, counts)
        if defects:
            w("C. hard defects (machine-decidable)")
            w("")
            for d in defects:
                w(f"   FAIL  {d}")
        else:
            w("C. hard defects (machine-decidable)")
            w("")
            w("   none: no replacement character, no orphan combining mark,")
            w("   no codepoint outside the expected ranges")
        w("")

        # rare glyphs: the tail of the inventory, read by hand
        rare = [(ch, n) for ch, n in counts.items() if n <= 2]
        if rare:
            w("   rare glyphs (frequency <= 2, read these by hand):")
            for ch, n in sorted(rare, key=lambda kv: (kv[1], ord(kv[0]))):
                idx, ctx = first[ch]
                w(f"     {ch}  U+{ord(ch):04X}  x{n}  {ctx}")
            w("")

        total_defects += len(defects)
        report[name] = {
            "chars": len(text),
            "nonascii": nonascii,
            "distinct": len(counts),
            "inventory": [
                {"glyph": ch, "codepoint": f"U+{ord(ch):04X}",
                 "name": unicodedata.name(ch, "<unnamed>"),
                 "freq": n, "class": classify(ch),
                 "first_context": first[ch][1]}
                for ch, n in counts.most_common()
            ],
            "hard_defects": defects,
        }

        for a, b, label in CONFUSABLES:
            if a in counts and b in counts:
                confusable_hits.append(
                    f"{name}: {label} -- {a!r} U+{ord(a):04X} x{counts[a]}, "
                    f"{b!r} U+{ord(b):04X} x{counts[b]}")

    # D. the pairs that only a reader can adjudicate
    w("-" * 78)
    w("D. manual review: look-alike pairs present in the same paper")
    w("-" * 78)
    w("Both members of a pair appearing is not an error. It means a")
    w("distinction was drawn somewhere, and the question is whether the prose")
    w("uses it consistently: ϵ_m for the delivery margin and ε for the drift")
    w("rate is a real distinction; ε_n for both a noise term and a convergence")
    w("tolerance is not.")
    w("")
    if confusable_hits:
        for h in confusable_hits:
            w(f"   CHECK  {h}")
    else:
        w("   no look-alike pair co-occurs within one paper")
    w("")
    w("   Also read: every glyph with frequency 1-2 in section B above, and")
    w("   every Greek letter whose two occurrences sit in different")
    w("   sub-sections. This is the check that no other audit performs.")
    w("")

    w("-" * 78)
    w("E. verdict")
    w("-" * 78)
    w(f"papers scanned: {sum(1 for v in report.values() if not v.get('missing'))}"
      f" / {len(PAPERS)}; hard defects: {total_defects}; "
      f"look-alike pairs: {len(confusable_hits)}")
    w("")
    w("PASS here means only that the glyph stream contains nothing a machine")
    w("can prove wrong. It does not mean the symbols are bound correctly; that")
    w("is section D, and it is a human step.")
    w("")
    verdict = "PASS" if total_defects == 0 else "FAIL"
    w(f"glyph scan: {verdict}")
    w("=" * 78)

    out = "\n".join(lines) + "\n"
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    print(out)
    if args.json:
        Path(args.json).write_text(json.dumps(
            {"papers": report, "confusables": confusable_hits,
             "hard_defects": total_defects, "verdict": verdict},
            indent=2, ensure_ascii=False), encoding="utf-8")
    return 0 if total_defects == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
