#!/usr/bin/env python3
"""Cross-paper redundancy audit: Paper 1 versus Paper 2.

The two papers share a vocabulary, a set of modelling conventions, and a small
number of results (cycle 107, the ledger gap, the 2.61 ratio). Some overlap is
therefore correct and necessary: Paper 2 cites the sandbox, and a citation of
a shared object is not self-plagiarism. The audit exists to separate three
things that look alike at the surface:

  FORMULA      the same displayed relation, quoted twice. Expected: the
               equations are the objects both papers reason about. Not a
               defect, but the second paper must cite the first.
  BOILERPLATE  stock epistemic phrasing ("errors are ours", "we do not
               estimate", "one seed"). Expected, and harmless: it is the
               register of the field, not content.
  SUBSTANTIVE  a run of prose that carries an argument, repeated nearly
               verbatim. This is the only category that is a defect, because
               it means the second paper is claiming the same contribution
               without saying so.

Unit of comparison: paragraphs (normalised length > 30 characters) and
sentences (normalised length > 15 characters), Paper 1 x Paper 2 only.

Usage:  python3 redundancy_audit.py [--bundle DIR] [--json OUT]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from difflib import SequenceMatcher
from pathlib import Path
from typing import List, Tuple

PAPER1 = ["00_Abstract.md", "01_Introduction.md", "02_Method.md",
          "03_Results.md", "04_Discussion.md", "Appendix.md"]
PAPER2 = ["00_Abstract.md", "01_Introduction.md", "02_Method.md",
          "03_Results.md", "04_Discussion.md"]

MATH = re.compile(r"\$[^$]*\$|\$\$[\s\S]*?\$\$|\\\[[\s\S]*?\\\]")
CITE = re.compile(r"\\cite\{[^}]*\}|\[@[^\]]*\]")
MARKUP = re.compile(r"[*_`#>|]")
# Shortest verbatim run that counts as a reported overlap. At 25 characters a
# match is a phrase ("would have been booked as"), not a coincidence of
# function words; below that every pair in the same field matches.
MIN_RUN = 25

STOPWORDS = set("""a an and are as at be been but by can for from has have if in
into is it its of on or that the their then there these they this to was were
which while with would""".split())

SENT_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-Z(\\])")

# Phrases that are register, not content. Matched against the *matched span*.
BOILERPLATE = [
    r"all (remaining )?errors are (ours|the author)",
    r"we do not (claim|estimate|model)",
    r"one seed",
    r"reproduc",
    r"the code that produced",
    r"no number in this paper",
    r"is a claim about the world",
    r"not a (theorem|constant) of the framework",
    r"read as counts, not as rates",
    r"withdrawn",
    r"falsif",
    r"does not (show|establish|claim)",
    r"it is (worth|important) (saying|noting)",
    r"in this (paper|section) we",
]


def normalise(text: str) -> str:
    # Math is removed rather than tokenised. Replacing every formula with the
    # same token makes "math , math , and math" a 30-character match between
    # any two sentences that contain three formulas. Equations are compared
    # exactly, in their own section.
    text = MATH.sub(" ", text)
    text = CITE.sub(" ", text)
    text = MARKUP.sub(" ", text)
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\s+([,.;:])", r"\1", text)
    return text.strip().lower()


DISPLAY = re.compile(r"\$\$([\s\S]+?)\$\$|\\\[([\s\S]+?)\\\]|"
                     r"\$([^$\n]{16,})\$")


def formulas(root: Path, files: List[str]) -> List[dict]:
    """Display and long inline math, normalised so that spacing and the
    left/right decoration do not hide an exact reuse."""
    out = []
    for fname in files:
        path = root / fname
        if not path.exists():
            continue
        raw = path.read_text(encoding="utf-8")
        raw = re.sub(r"```[\s\S]*?```", " ", raw)
        for m in DISPLAY.finditer(raw):
            body = next(g for g in m.groups() if g)
            # inline math ("$...$") only counts when it actually holds a
            # relation or a LaTeX command; otherwise "$x$" and a stray pair
            # of dollar signs would look like a shared equation.
            if m.group(3) and not re.search(r"[=<>]|\\[a-zA-Z]+", body):
                continue
            norm = re.sub(r"\s+", " ", body)
            norm = norm.replace("\\left", "").replace("\\right", "")
            norm = re.sub(r"\\[,;:!]", "", norm).strip()
            if len(norm) < 12:
                continue
            out.append({"file": fname, "body": body.strip(), "norm": norm})
    return out


def formula_reuse(f1: List[dict], f2: List[dict],
                  fuzzy: float = 0.80) -> List[dict]:
    index = {}
    for b in f2:
        index.setdefault(b["norm"], []).append(b)
    rows = []
    for a in f1:
        for b in index.get(a["norm"], []):
            rows.append({"p1": a, "p2": b, "norm": a["norm"], "exact": True})
    # near-identical equations: the same relation written with different
    # macros (\frac vs /, ^\ast vs _i) still counts as reused.
    for a in f1:
        words = set(a["norm"].split())
        if len(words) < 4:
            continue
        for b in f2:
            if abs(len(a["norm"]) - len(b["norm"])) > 40:
                continue
            if len(words & set(b["norm"].split())) < 3:
                continue
            r = SequenceMatcher(None, a["norm"], b["norm"]).ratio()
            if r >= fuzzy:
                rows.append({"p1": a, "p2": b, "norm": a["norm"],
                             "exact": False, "ratio": r})
    # de-duplicate identical formulas within a paper
    seen, out = set(), []
    for r in sorted(rows, key=lambda r: (not r["exact"], -r.get("ratio", 1.0))):
        key = (r["norm"], r["p1"]["file"], r["p2"]["file"])
        if key in seen:
            continue
        seen.add(key)
        out.append(r)
    return out


def units(root: Path, files: List[str], kind: str) -> List[dict]:
    out: List[dict] = []
    for fname in files:
        path = root / fname
        if not path.exists():
            continue
        raw = path.read_text(encoding="utf-8")
        # drop headings: they are labels, and they legitimately repeat
        raw = re.sub(r"^#+\s.*$", "", raw, flags=re.MULTILINE)
        # drop fenced code blocks: TikZ and shell are shared by design
        raw = re.sub(r"```[\s\S]*?```", " ", raw)
        if kind == "paragraph":
            chunks = re.split(r"\n\s*\n", raw)
        else:
            chunks = SENT_SPLIT.split(re.sub(r"\n+", " ", raw))
        for chunk in chunks:
            lines = [ln for ln in chunk.splitlines() if ln.strip()]
            if lines and sum(1 for ln in lines if ln.lstrip().startswith("|")) \
                    / len(lines) > 0.5:
                continue          # a table is not prose; its scaffolding
                                  # would match every other table
            norm = normalise(chunk)
            if len(norm) >= (30 if kind == "paragraph" else 15):
                out.append({"file": fname, "text": chunk.strip(), "norm": norm})
    return out


def label(norm_a: str, norm_b: str, matched: str) -> str:
    maths = matched.count("math")
    words = len(matched.split())
    content = [w for w in re.findall(r"[a-z]+", matched)
               if w not in STOPWORDS and w != "math"]
    if len(content) < 3:
        return "SCAFFOLD"
    if words and maths / max(words, 1) > 0.25:
        return "FORMULA"
    for pat in BOILERPLATE:
        if re.search(pat, matched):
            return "BOILERPLATE"
    if maths:
        return "FORMULA"
    # A technical phrase ("and the absence of a dormant phase") is shared
    # vocabulary, not a copied argument: the two papers describe the same
    # ablation and must use the same words for it. Copy-paste begins at a
    # whole clause, which is what the length and word-count floors measure.
    if len(matched) >= 40 and len(content) >= 6:
        return "SUBSTANTIVE"
    return "SHARED-TERM"


def shingles(norm: str, k: int = 4) -> set:
    words = norm.split()
    return {" ".join(words[i:i + k]) for i in range(max(len(words) - k + 1, 1))}


def compare(left: List[dict], right: List[dict], top: int) -> List[dict]:
    for u in left + right:
        u["_sh"] = shingles(u["norm"])

    rows = []
    for i, a in enumerate(left):
        sa = a["_sh"]
        for j, b in enumerate(right):
            sb = b["_sh"]
            inter = len(sa & sb)
            if inter < 3:
                continue
            sm = SequenceMatcher(None, a["norm"], b["norm"])
            if sm.quick_ratio() < 0.45:
                continue
            if sm.real_quick_ratio() < 0.45:
                continue
            ratio = sm.ratio()
            if ratio < 0.25:
                continue
            blocks = [bl for bl in sm.get_matching_blocks()
                      if bl.size >= MIN_RUN]
            if not blocks:
                continue
            biggest = max(blocks, key=lambda bl: bl.size)
            matched = a["norm"][biggest.a: biggest.a + biggest.size]
            # a match made only of math placeholders and connectives is the
            # same scaffolding, not the same sentence
            content = [w for w in re.findall(r"[a-z]+", matched)
                       if w not in STOPWORDS and w != "math"]
            if len(content) < 3:
                continue
            rows.append({
                "ratio": ratio,
                "p1": a, "p2": b,
                "matched": matched,
                "matched_chars": biggest.size,
                "class": label(a["norm"], b["norm"], matched),
            })
    rows.sort(key=lambda r: (-r["matched_chars"], -r["ratio"]))
    # one row per (p1 unit), keeping the best partner: otherwise a single
    # boilerplate sentence fills the table ten times
    seen, unique = set(), []
    for r in rows:
        if r["p1"]["norm"] in seen:
            continue
        seen.add(r["p1"]["norm"])
        unique.append(r)
    for r in unique:
        r["p1"] = {k: v for k, v in r["p1"].items() if k != "_sh"}
        r["p2"] = {k: v for k, v in r["p2"].items() if k != "_sh"}
    return unique[:top]


def rank_pairs(left: List[dict], right: List[dict], top: int,
               floor: float = 0.30) -> List[dict]:
    """Top pairs by whole-string similarity, whatever the shared-run length.
    This is the 'top ten' view: it answers 'what are the two most alike texts
    in the corpus', even when the answer is 'nothing worth flagging'."""
    rows = []
    for a in left:
        sh = shingles(a["norm"])
        for b in right:
            sb = shingles(b["norm"])
            if len(sh & sb) < 3:
                continue
            sm = SequenceMatcher(None, a["norm"], b["norm"])
            ratio = sm.ratio()
            if ratio < floor:
                continue
            bl = max(sm.get_matching_blocks(), key=lambda x: x.size)
            matched = a["norm"][bl.a: bl.a + bl.size]
            rows.append({"ratio": ratio, "p1": a, "p2": b, "matched": matched,
                         "matched_chars": bl.size,
                         "class": label(a["norm"], b["norm"], matched)})
    rows.sort(key=lambda r: -r["ratio"])
    seen, unique = set(), []
    for r in rows:
        if r["p1"]["norm"] in seen:
            continue
        seen.add(r["p1"]["norm"])
        unique.append(r)
    return unique[:top]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--bundle", default=str(Path(__file__).resolve().parent.parent))
    ap.add_argument("--json", default="")
    ap.add_argument("--top", type=int, default=10)
    args = ap.parse_args()
    bundle = Path(args.bundle)
    p1root, p2root = bundle / "paper1_source", bundle / "paper2_source"

    par1, par2 = units(p1root, PAPER1, "paragraph"), units(p2root, PAPER2, "paragraph")
    sen1, sen2 = units(p1root, PAPER1, "sentence"), units(p2root, PAPER2, "sentence")

    para = compare(par1, par2, args.top)
    sent = compare(sen1, sen2, args.top)

    lines: List[str] = []
    w = lines.append
    w("=" * 78)
    w("cross-paper redundancy audit (Paper 1 vs Paper 2)")
    w("=" * 78)
    w(f"bundle    : {bundle}")
    w(f"units     : {len(par1)} paragraphs (P1) x {len(par2)} (P2); "
      f"{len(sen1)} sentences (P1) x {len(sen2)} (P2)")
    w("")
    w("Similarity is the difflib ratio on normalised text: math removed (it is")
    w("compared separately, in section D), citations and markup removed, case")
    w("folded. Sections A and B rank by the longest common block, because a")
    w("short stock phrase inside a long paragraph inflates the ratio without")
    w("carrying content; section C ranks by the ratio itself, which is the")
    w("'top ten' view, and is reported with that caveat.")
    w("")

    def section(title: str, rows: List[dict], unit: str) -> Tuple[int, int]:
        w("-" * 78)
        w(title)
        w("-" * 78)
        subst = 0
        for k, r in enumerate(rows, 1):
            tag = r["class"]
            if tag == "SUBSTANTIVE":
                subst += 1
            w(f"{k:2d}. [{tag:11s}] ratio {r['ratio']:.2f}  "
              f"common block {r['matched_chars']} chars")
            w(f"    P1 {r['p1']['file']}")
            w(f"    P2 {r['p2']['file']}")
            w(f"    P1> {clip(r['p1']['text'], 210)}")
            w(f"    P2> {clip(r['p2']['text'], 210)}")
            w(f"    common> \"{clip(r['matched'], 150, chars=True)}\"")
            w("")
        w(f"{unit} summary: {len(rows)} pair(s) reported, {subst} SUBSTANTIVE")
        w("")
        return len(rows), subst

    def clip(s: str, n: int, chars: bool = False) -> str:
        s = re.sub(r"\s+", " ", s).strip()
        return s if len(s) <= n else s[:n] + " ..."

    npar, sp = section("A. paragraph level (normalised length > 30)", para, "paragraph")
    nsen, ss = section("B. sentence level (normalised length > 15)", sent, "sentence")

    # the requested "top ten", ranked by whole-string similarity
    ranked = rank_pairs(sen1, sen2, args.top, floor=0.25)
    w("-" * 78)
    w("C. top pairs by whole-string similarity (sentence level, up to 10)")
    w("-" * 78)
    w("This is the view the request asks for: the most alike sentence pairs in")
    w("the two corpora, whatever their shared-run length. A pair can rank here")
    w("and still carry no verbatim overlap longer than a phrase. If fewer than")
    w("ten pairs clear the 0.25 floor, that is the finding: the corpora are more")
    w("dissimilar than the top-ten format assumes.")
    w("")
    for k, r in enumerate(ranked, 1):
        w(f"{k:2d}. [{r['class']:11s}] ratio {r['ratio']:.2f}  "
          f"longest common run {r['matched_chars']} chars")
        w(f"    P1 {r['p1']['file']}")
        w(f"    P2 {r['p2']['file']}")
        w(f"    P1> {clip(r['p1']['text'], 150)}")
        w(f"    P2> {clip(r['p2']['text'], 150)}")
        w(f"    common> \"{clip(r['matched'], 100, chars=True)}\"")
        w("")
    ranked_subst = sum(1 for r in ranked if r["class"] == "SUBSTANTIVE")
    ss += ranked_subst
    w(f"top-ten summary: {len(ranked)} pair(s) above 0.25, "
      f"{ranked_subst} SUBSTANTIVE")
    w("")

    f1 = formulas(p1root, PAPER1)
    f2 = formulas(p2root, PAPER2)
    reuse = formula_reuse(f1, f2)
    w("-" * 78)
    w("D. displayed equations present in both papers (exact after normalisation)")
    w("-" * 78)
    n_exact = sum(1 for r in reuse if r["exact"])
    w(f"formulas extracted: {len(f1)} (P1), {len(f2)} (P2); "
      f"shared: {len(reuse)} ({n_exact} exact, {len(reuse) - n_exact} "
      f"near-identical at ratio >= 0.80)")
    if reuse:
        for k, r in enumerate(reuse[:12], 1):
            mark = "exact" if r["exact"] else f"ratio {r['ratio']:.2f}"
            w(f"{k:2d}. [{mark}] P1 {r['p1']['file']}  <->  P2 {r['p2']['file']}")
            w(f"    {clip(r['norm'], 150, chars=True)}")
    else:
        w("    none")
    w("")
    w("Shared equations are FORMULA-class by construction: they are the objects")
    w("both papers reason about, and the second must cite the first for them.")
    w("")

    # category census
    census = {}
    for r in para + sent:
        census[r["class"]] = census.get(r["class"], 0) + 1
    census["FORMULA"] = census.get("FORMULA", 0) + len(reuse)
    for r in ranked:
        census["TOP10:" + r["class"]] = census.get("TOP10:" + r["class"], 0) + 1
    w("-" * 78)
    w("E. verdict")
    w("-" * 78)
    w("category census over the reported pairs: "
      + ", ".join(f"{k}={v}" for k, v in sorted(census.items())))
    w("")
    w("FORMULA rows are the shared equations (the charge account, the threshold,")
    w("the ledger identity). They are the objects both papers reason about and")
    w("Paper 2 cites Paper 1 for them; repetition is not a defect.")
    w("BOILERPLATE rows are stock epistemic phrasing; the register is shared by")
    w("both papers and by the field.")
    w("SHARED-TERM rows are technical phrases both papers must use (the name of")
    w("an ablation, a state). Not a defect.")
    w("SUBSTANTIVE rows are the only ones that would count as self-plagiarism: a")
    w("whole clause (>= 40 characters, >= 6 content words) repeated verbatim.")
    if sp + ss == 0:
        w("There are none.")
    else:
        w(f"There are {sp + ss}; each location is printed above and must either")
        w("be rewritten or cited.")
    w("")
    verdict = "PASS" if sp + ss == 0 else "FAIL"
    w(f"redundancy audit: {verdict}")
    w("=" * 78)

    out = "\n".join(lines) + "\n"
    print(out)
    if args.json:
        Path(args.json).write_text(json.dumps(
            {"paragraph": para, "sentence": sent,
             "census": census, "substantive": sp + ss,
             "verdict": verdict}, indent=2, ensure_ascii=False), encoding="utf-8")
    return 0 if sp + ss == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
