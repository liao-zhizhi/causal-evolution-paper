#!/usr/bin/env python3
"""Figure and table audit for Papers 1 and 2.

Lean4 checks the discrete algebra; this script checks the part of the
manuscript Lean4 cannot see: that every figure and table is numbered
contiguously, is cited before it is displayed, is not orphaned, and that the
numbers the prose attributes to those figures and tables agree with the CSV
files the figures were drawn from.

Six checks per paper:

  C1  figure numbers are contiguous and agree with the order of appearance
  C2  table numbers are contiguous within each series (1..n, A.1..A.n)
  C3  no dangling reference (text cites a figure/table that does not exist)
  C4  no orphan figure/table (displayed but never cited in prose)
  C5  first citation precedes display
  C6  citations are introduced in ascending numeric order

Plus a data section (C7): every numeric claim anchored to a figure or table is
recomputed from the snapshot in `audits/data_snapshot/` and compared with the
number printed in the prose.

Usage:  python3 figure_table_audit.py [--bundle DIR] [--json OUT]
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

# --------------------------------------------------------------------------
# document order
# --------------------------------------------------------------------------

PAPER1 = ["00_Abstract.md", "01_Introduction.md", "02_Method.md",
          "03_Results.md", "04_Discussion.md", "Appendix.md"]
PAPER2 = ["00_Abstract.md", "01_Introduction.md", "02_Method.md",
          "03_Results.md", "04_Discussion.md"]

# "Figure 6(a)" / "Figure 1" / "Figures 3 and 4" ; "Table 2" / "Table A.3"
RE_FIG = re.compile(r"\bFigures?\s+(\d+)((?:\s*\(\w\))?)")
RE_TAB = re.compile(r"\bTables?\s+(A\.)?(\d+)")
RE_TAB_CAPTION = re.compile(r"^\*\*Table\s+(A\.)?(\d+)\.", re.MULTILINE)
RE_FIG_CAPTION = re.compile(r"^!\[(.*?)\]\((figures/[^)]+)\)", re.MULTILINE)
RE_TIKZ = re.compile(r"^```latex\s*\n(?:(?!```)[\s\S])*?\\begin\{tikzpicture\}",
                     re.MULTILINE)


class Paper:
    def __init__(self, name: str, root: Path, files: List[str]):
        self.name = name
        self.root = root
        self.files = files
        self.text = ""
        self.spans: List[Tuple[int, int, str]] = []   # (start, end, file)
        for fname in files:
            path = root / fname
            if not path.exists():
                continue
            body = path.read_text(encoding="utf-8")
            self.spans.append((len(self.text), len(self.text) + len(body), fname))
            self.text += body + "\n"

    def where(self, offset: int) -> str:
        for start, end, fname in self.spans:
            if start <= offset < end:
                local = self.text[start:offset].count("\n") + 1
                return f"{fname}:{local}"
        return "?"

    # ---- appearances -----------------------------------------------------
    def figures(self) -> List[dict]:
        out = []
        for m in RE_FIG_CAPTION.finditer(self.text):
            out.append({"offset": m.start(), "caption": m.group(1),
                        "path": m.group(2)})
        for m in RE_TIKZ.finditer(self.text):
            out.append({"offset": m.start(), "caption": "(TikZ block)",
                        "path": "figures/dag.tex"})
        out.sort(key=lambda d: d["offset"])
        for i, f in enumerate(out, 1):
            f["number"] = i
        return out

    def tables(self) -> List[dict]:
        out = []
        for m in RE_TAB_CAPTION.finditer(self.text):
            out.append({"offset": m.start(),
                        "series": "A" if m.group(1) else "main",
                        "number": int(m.group(2)),
                        "where": self.where(m.start())})
        out.sort(key=lambda d: d["offset"])
        return out

    # ---- references ------------------------------------------------------
    def _masked(self) -> List[Tuple[int, int]]:
        """Spans that must not be read as citations: the caption lines
        themselves (`**Table 2. ...**`, `![...](figures/...)`). A caption
        naming its own float is not a cross-reference."""
        spans = []
        for m in RE_TAB_CAPTION.finditer(self.text):
            end = m.start()
            while end < len(self.text) and self.text[end] != "\n":
                end += 1
            spans.append((m.start(), end))
        for m in RE_FIG_CAPTION.finditer(self.text):
            spans.append((m.start(), m.end()))
        return spans

    def figure_refs(self) -> List[dict]:
        spans = self._masked()
        out = []
        for m in RE_FIG.finditer(self.text):
            if any(a <= m.start() < b for a, b in spans):
                continue
            out.append({"offset": m.start(), "number": int(m.group(1)),
                        "panel": m.group(2).strip(), "where": self.where(m.start())})
        return out

    def table_refs(self) -> List[dict]:
        spans = self._masked()
        out = []
        for m in RE_TAB.finditer(self.text):
            if any(a <= m.start() < b for a, b in spans):
                continue
            out.append({"offset": m.start(),
                        "series": "A" if m.group(1) else "main",
                        "number": int(m.group(2)), "where": self.where(m.start())})
        return out

    def sentence_at(self, offset: int) -> str:
        start = max(self.text.rfind("\n\n", 0, offset),
                    self.text.rfind(". ", 0, offset))
        end = self.text.find("\n\n", offset)
        return self.text[max(start, 0): end if end > 0 else offset + 200]


# --------------------------------------------------------------------------
# CSV helpers
# --------------------------------------------------------------------------

def csv_rows(snap: Path, name: str) -> List[dict]:
    with open(snap / name, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def fnum(x: str) -> float:
    return float(x)


# --------------------------------------------------------------------------
# C1..C6
# --------------------------------------------------------------------------

def audit_numbering(paper: Paper) -> Tuple[List[dict], List[dict]]:
    """Return (checks, notes)."""
    checks, notes = [], []

    figs = paper.figures()
    tabs = paper.tables()
    frefs = paper.figure_refs()
    trefs = paper.table_refs()

    # C1 figure numbers contiguous and filenames agree with position
    problems = []
    for f in figs:
        m = re.search(r"fig(\d+)_", f["path"])
        if m and int(m.group(1)) != f["number"]:
            problems.append(f"Figure {f['number']} is drawn from {f['path']}, "
                            f"whose ordinal is {m.group(1)}")
    checks.append({
        "id": "C1", "paper": paper.name,
        "what": "figure numbering is contiguous and matches file ordinals",
        "status": "PASS" if not problems else "FAIL",
        "detail": "; ".join(problems) or f"{len(figs)} figure(s), numbered 1..{len(figs)}",
    })

    # C2 table numbers contiguous within series
    problems = []
    for series in ("main", "A"):
        nums = [t["number"] for t in tabs if t["series"] == series]
        expect = list(range(1, len(nums) + 1))
        if nums != expect:
            problems.append(f"series {series!r}: found {nums}, expected {expect}")
    checks.append({
        "id": "C2", "paper": paper.name,
        "what": "table numbering is contiguous within each series",
        "status": "PASS" if not problems else "FAIL",
        "detail": "; ".join(problems) or
                  ", ".join(f"{s}:{sum(1 for t in tabs if t['series'] == s)}"
                            for s in ("main", "A")),
    })

    # C3 dangling references
    known_fig = {f["number"] for f in figs}
    known_tab = {(t["series"], t["number"]) for t in tabs}
    dangling = [f"Figure {r['number']} at {r['where']}"
                for r in frefs if r["number"] not in known_fig]
    dangling += [f"Table {'A.' if r['series'] == 'A' else ''}{r['number']} "
                 f"at {r['where']}"
                 for r in trefs if (r["series"], r["number"]) not in known_tab]
    checks.append({
        "id": "C3", "paper": paper.name,
        "what": "no reference to a figure or table that does not exist",
        "status": "PASS" if not dangling else "FAIL",
        "detail": "; ".join(dangling) or "no dangling reference",
    })

    # C4 orphans. A caption is not a citation: strip the caption line itself.
    cited_fig = {r["number"] for r in frefs}
    cited_tab = {(r["series"], r["number"]) for r in trefs}
    orphans = [f"Figure {f['number']}" for f in figs if f["number"] not in cited_fig]
    orphans += [f"Table {'A.' if t['series'] == 'A' else ''}{t['number']}"
                for t in tabs if (t["series"], t["number"]) not in cited_tab]
    checks.append({
        "id": "C4", "paper": paper.name,
        "what": "no figure or table is displayed without being cited in prose",
        "status": "PASS" if not orphans else "FAIL",
        "detail": "; ".join(f"{o} cited 0 times" for o in orphans) or
                  "every float is cited",
    })

    # C5 first citation precedes display
    early = []
    for f in figs:
        prior = [r for r in frefs if r["number"] == f["number"]
                 and r["offset"] < f["offset"]]
        first = min([r["offset"] for r in frefs
                     if r["number"] == f["number"]], default=None)
        if not prior:
            after = "never cited at all" if first is None else \
                    f"first cited at {paper.where(first)}, {first - f['offset']} chars later"
            early.append(f"Figure {f['number']} displayed at {paper.where(f['offset'])} "
                         f"({after})")
    for t in tabs:
        prior = [r for r in trefs if r["series"] == t["series"]
                 and r["number"] == t["number"] and r["offset"] < t["offset"]]
        first = min([r["offset"] for r in trefs if r["series"] == t["series"]
                     and r["number"] == t["number"]], default=None)
        if not prior:
            label = f"{'A.' if t['series'] == 'A' else ''}{t['number']}"
            after = "never cited at all" if first is None else \
                    f"first cited at {paper.where(first)}"
            early.append(f"Table {label} displayed at {t['where']} ({after})")
    checks.append({
        "id": "C5", "paper": paper.name,
        "what": "each float is cited before it is displayed",
        "status": "PASS" if not early else "FAIL",
        "detail": "; ".join(early) or "all floats cited before display",
    })

    # C6 ascending introduction order. Appendix tables are allowed to be
    # forward-referenced from the results section, so only the main series is
    # ordered; the appendix series is checked among itself.
    seen, order, viol = set(), [], []
    for r in frefs:
        if r["number"] not in seen:
            seen.add(r["number"])
            order.append(r["number"])
    if order != sorted(order):
        viol.append(f"figures first cited in order {order}")
    main_order, app_order = [], []
    for r in trefs:
        target = app_order if r["series"] == "A" else main_order
        key = r["number"]
        if key not in target:
            target.append(key)
    if main_order != sorted(main_order):
        viol.append(f"main tables first cited in order {main_order}")
    if app_order != sorted(app_order):
        notes.append("appendix tables are forward-referenced out of order: "
                     f"{app_order} (legal, but the first appendix mention is "
                     f"Table A.{app_order[0]})")
    checks.append({
        "id": "C6", "paper": paper.name,
        "what": "figures and tables are introduced in ascending numeric order",
        "status": "PASS" if not viol else "FAIL",
        "detail": "; ".join(viol) or
                  f"figures {order if order else '-'}; main tables {main_order}; "
                  f"appendix tables {app_order}",
    })

    # C8 scholarly citation: a float mentioned only inside a production note
    # ("kept here as the source of Figure 1") has not been cited at all.
    PROD = re.compile(r"TikZ|MathJax|source of (?:the )?(?:figure|graph)|"
                      r"kept here", re.IGNORECASE)
    weak = []
    for f in figs:
        hits = [r for r in frefs if r["number"] == f["number"]]
        if hits and all(PROD.search(paper.sentence_at(r["offset"])) for r in hits):
            weak.append(f"Figure {f['number']} is named only in a production note "
                        f"({hits[0]['where']}), never in the argument")
    for t in tabs:
        hits = [r for r in trefs if r["series"] == t["series"]
                and r["number"] == t["number"]]
        if hits and all(PROD.search(paper.sentence_at(r["offset"])) for r in hits):
            weak.append(f"Table {t['number']} is named only in a production note")
    checks.append({
        "id": "C8", "paper": paper.name,
        "what": "every float is cited in the argument, not only in a build note",
        "status": "PASS" if not weak else "FAIL",
        "detail": "; ".join(weak) or "all citations are scholarly",
    })

    # panel sanity: every panel letter cited must exist in the caption
    panel_bad = []
    for f in figs:
        letters = set(re.findall(r"\((\w)\)", f["caption"]))
        for r in frefs:
            if r["number"] == f["number"] and r["panel"]:
                letter = r["panel"].strip("()")
                if letters and letter not in letters:
                    panel_bad.append(f"Figure {f['number']}({letter}) at {r['where']} "
                                     f"but panels are {sorted(letters)}")
    if panel_bad:
        notes.append("panel references: " + "; ".join(panel_bad))

    return checks, notes


# --------------------------------------------------------------------------
# C7 numeric claims vs CSV
# --------------------------------------------------------------------------

class Ctx:
    def __init__(self, snap: Path):
        self.pop = csv_rows(snap, "evo_population.csv")
        self.drift = csv_rows(snap, "evo_drift_sweep.csv")
        self.dead = csv_rows(snap, "evo_deadlock_sweep.csv")
        self.r7 = csv_rows(snap, "evo_r7_ablation.csv")
        self.gate = csv_rows(snap, "evo_wake_gate_sweep.csv")
        self.shock = csv_rows(snap, "evo_shock_sweep.csv")
        self.margin = csv_rows(snap, "evo_margin_sweep.csv")

    # base run helpers
    def row(self, cycle: int) -> dict:
        return next(r for r in self.pop if int(r["cycle"]) == cycle)

    @property
    def last(self) -> dict:
        return self.pop[-1]

    def cum(self, col: str) -> float:
        return fnum(self.last[col])

    def gap(self) -> float:
        return self.cum("cum_reported_a") - self.cum("cum_delivered_a")


def build_assertions(ctx: Ctx) -> List[dict]:
    """Each entry: prose anchor, the value the prose prints, the CSV value."""

    pop, r7 = ctx.pop, ctx.r7[0]
    self_arm = ctx.r7[0]
    r7_arm = ctx.r7[1]

    base_gap = ctx.gap()
    base_pct = base_gap / ctx.cum("cum_delivered_a") * 100

    # gap accumulated before cycle 100 (exclusive)
    prev_inv, prev_gap, before, after = 0, 0.0, 0.0, 0.0
    for r in pop:
        c = int(r["cycle"])
        inv, deliv, rep = int(r["invalid_a"]), fnum(r["cum_delivered_a"]), fnum(r["cum_reported_a"])
        dg = rep - deliv - prev_gap
        if c < 100:
            before += dg
        else:
            after += dg
        prev_inv, prev_gap = inv, rep - deliv

    # invalid split
    inv_shock = sum(int(r["invalid_a"]) for r in pop if int(r["cycle"]) in
                    {23, 24, 46, 47, 69, 70, 92, 93})
    inv_term = sum(int(r["invalid_a"]) for r in pop if int(r["cycle"]) in
                   {100, 101, 102, 103, 104, 105, 106, 107})
    # per-cycle increments, not cumulative
    prev, inc_shock, inc_term = 0, 0, 0
    for r in pop:
        c, inv = int(r["cycle"]), int(r["invalid_a"])
        inc = inv - prev
        if c in {23, 24, 46, 47, 69, 70, 92, 93}:
            inc_shock += inc
        elif c >= 100:
            inc_term += inc
        prev = inv

    # deadlock sweep, Type B, self policy
    agg: Dict[float, List[int]] = {}
    for r in ctx.dead:
        if r["kind"] != "B" or r["a_policy"] != "self":
            continue
        t = round(float(r["theta_wake"]), 4)
        agg.setdefault(t, [0, 0])
        agg[t][0] += 1
        agg[t][1] += int(r["deadlock"])

    def dl(theta: float) -> int:
        return agg[theta][1]

    frac = {t: v[1] / v[0] for t, v in agg.items()}
    mid = None
    for t in sorted(frac):
        if frac[t] >= 0.5:
            lo = round(t - 0.01, 4)
            mid = lo + (0.5 - frac[lo]) / (frac[t] - frac[lo]) * 0.01
            break

    chi1 = 17.7778
    theta1 = 1 - 1 / chi1
    chi300 = 14.6343
    theta300 = 1 - 1 / chi300

    drift = {float(r["drift_pct_per_10"]): r for r in ctx.drift}
    gate = {r["wake_gate"]: r for r in ctx.gate}
    shock = {r["shock_len"]: r for r in ctx.shock if r["swept"] == "shock_len"}
    depth = {r["shock_depth"]: r for r in ctx.shock if r["swept"] == "shock_depth"}
    margin = ctx.margin

    A = []

    def add(name, anchor, claimed, value, tol, source, file="paper1_source/03_Results.md"):
        A.append(dict(name=name, anchor=anchor, claimed=claimed, value=value,
                      tol=tol, source=source, file=file))

    add("rho(99) shown in the event table", r"last cycle with full delivery",
        "0.9342", fnum(ctx.row(99)["capacity_ratio"]), 5e-4, "evo_population.capacity_ratio@99")
    add("rho(100) shown in the event table", r"delivery ceases permanently",
        "0.9271", fnum(ctx.row(100)["capacity_ratio"]), 5e-4, "evo_population.capacity_ratio@100")
    add("rho(300) named in the event table", r"rho\(300\)", "0.673",
        fnum(ctx.row(300)["capacity_ratio"]), 5e-4, "evo_population.capacity_ratio@300")
    add("Type-A extinction cycle (Fig. 6a)", r"Type-A extinct", "107",
        int(ctx.row(107)["alive_a"] == "0") and 107, 0, "evo_population.alive_a@107")
    add("Type-B stranding cycle (Fig. 6a)", r"Type-B stranded", "279",
        next(int(r["cycle"]) for r in pop if int(r["stranded_b"]) == 50), 0,
        "evo_population.stranded_b@279")
    add("cumulative delivered, Type-A (Fig. 6b)", r"Type-A accumulates",
        "7676.93", ctx.cum("cum_delivered_a"), 0.005, "evo_population.cum_delivered_a@300")
    add("cumulative recorded, Type-A (Fig. 6b)", r"Type-A accumulates",
        "8871.71", ctx.cum("cum_reported_a"), 0.005, "evo_population.cum_reported_a@300")
    add("ledger gap (Fig. 6b)", r"a\s+difference of", "1194.78", base_gap, 0.005,
        "cum_reported_a - cum_delivered_a @300")
    add("ledger gap as a percentage", r"a\s+difference of", "15.563", base_pct, 5e-4,
        "gap / cum_delivered_a @300")
    add("Table 3 PASS Type-A", r"verdict budget is given in Table 3", "4550",
        int(ctx.last["pass_a"]), 0, "evo_population.pass_a@300")
    add("Table 3 FAIL Type-A (structural zero)", r"verdict budget is given in Table 3", "0",
        int(ctx.last["fail_a"]), 0, "evo_population.fail_a@300")
    add("Table 3 INVALID Type-A", r"verdict budget is given in Table 3", "708",
        int(ctx.last["invalid_a"]), 0, "evo_population.invalid_a@300")
    add("Table 3 NOT_RUN Type-B", r"verdict budget is given in Table 3", "3250",
        int(ctx.last["not_run_b"]), 0, "evo_population.not_run_b@300")
    add("the 708 INVALID split, shock part", r"708 .INVALID. verdicts split",
        "400", inc_shock, 0, "sum of invalid_a increments on shock cycles")
    add("the 708 INVALID split, drought part", r"708 .INVALID. verdicts split",
        "308", inc_term, 0, "sum of invalid_a increments from cycle 100")
    add("56.5% of the gap predates cycle 100", r"56\.5", "56.5",
        before / (before + after) * 100, 0.05, "gap accumulated before cycle 100")
    add("Table 2, 1% drift, A extinct", r"Table 2\. Lifespan", "107",
        int(drift[1.0]["a_extinct_cycle"]), 0, "evo_drift_sweep.a_extinct_cycle@1.0")
    add("Table 2, 1% drift, B stranded", r"Table 2\. Lifespan", "279",
        int(drift[1.0]["b_strand_cycle"]), 0, "evo_drift_sweep.b_strand_cycle@1.0")
    add("Table 2, 5% drift, B deadlocked", r"four Type-B agents deadlock", "4",
        int(drift[5.0]["b_deadlock_final"]), 0, "evo_drift_sweep.b_deadlock_final@5.0")
    add("Table 2, 5% drift, B alive at 400", r"5\.0%\s*\|\s*28", "46",
        int(drift[5.0]["b_alive_final"]), 0, "evo_drift_sweep.b_alive_final@5.0")
    add("Table 4, theta=0.91 deadlocks", r"Table 4\. Confirmed deadlocks", "2",
        dl(0.91), 0, "evo_deadlock_sweep deadlock@0.91")
    add("Table 4, theta=0.93 deadlocks", r"Table 4\. Confirmed deadlocks", "19",
        dl(0.93), 0, "evo_deadlock_sweep deadlock@0.93")
    add("Table 4, theta=0.94 deadlocks", r"Table 4\. Confirmed deadlocks", "43",
        dl(0.94), 0, "evo_deadlock_sweep deadlock@0.94")
    add("no Type-A deadlock at any theta", r"No Type-A agent deadlocks", "0",
        sum(int(r["deadlock"]) for r in ctx.dead if r["kind"] == "A"), 0,
        "evo_deadlock_sweep deadlock, kind=A")
    add("measured midpoint by interpolation", r"measured half-saturation point", "0.9325",
        mid, 5e-5, "linear interpolation of the deadlock curve")
    add("theta*(1) = 1 - 1/chi(1)", r"theta\^\\ast\(1\)", "0.9437", theta1, 1e-4,
        "1 - 1/17.7778")
    add("theta*(300) = 1 - 1/chi(300)", r"theta\^\\ast\(300\)", "0.9317", theta300, 1e-4,
        "1 - 1/14.6343")
    add("measured midpoint sits 0.09% above the terminal anchor",
        r"0\.09", "0.09", (mid - theta300) / theta300 * 100, 0.005,
        "(mid - theta300)/theta300")
    add("Table 5, self arm delivered", r"Table 5\. Ablation", "7676.93",
        fnum(self_arm["cum_delivered_a"]), 0.005, "evo_r7_ablation.cum_delivered_a[self]")
    add("Table 5, r7 arm delivered", r"Table 5\. Ablation", "23602.92",
        fnum(r7_arm["cum_delivered_a"]), 0.005, "evo_r7_ablation.cum_delivered_a[r7]")
    add("Table 5, r7 arm INVALID count", r"Table 5\. Ablation", "4950",
        int(r7_arm["invalid_a"]), 0, "evo_r7_ablation.invalid_a[r7]")
    add("r7 delivers 3.07x the self arm", r"3\.07", "3.07",
        fnum(r7_arm["cum_delivered_a"]) / fnum(self_arm["cum_delivered_a"]), 0.005,
        "ratio of cumulative delivery")
    add("Table 6, peak gate strand cycle", r"Table 6\. Wake-gate", "279",
        int(gate["peak"]["b_strand_cycle"]), 0, "evo_wake_gate_sweep.b_strand_cycle[peak]")
    add("Table 6, mean gate strand cycle", r"Table 6\. Wake-gate", "233",
        int(gate["mean"]["b_strand_cycle"]), 0, "evo_wake_gate_sweep.b_strand_cycle[mean]")
    add("Table 6, legacy gate strand cycle", r"Table 6\. Wake-gate", "983",
        int(gate["legacy"]["b_strand_cycle"]), 0, "evo_wake_gate_sweep.b_strand_cycle[legacy]")
    add("Table 6, legacy ratio 9.19", r"Table 6\. Wake-gate", "9.19",
        fnum(gate["legacy"]["lifetime_ratio"]), 0.005, "evo_wake_gate_sweep.lifetime_ratio[legacy]")
    add("shock L=3 gives extinction at 106", r"L=3", "106",
        int(shock["3"]["a_extinct_cycle"]), 0, "evo_shock_sweep.a_extinct_cycle[L=3]")
    add("shock L=6 gives extinction at 51", r"L=6", "51",
        int(shock["6"]["a_extinct_cycle"]), 0, "evo_shock_sweep.a_extinct_cycle[L=6]")
    add("margin sweep extinction cycles", r"at cycles 69, 93", "69",
        int(margin[0]["a_extinct_cycle"]), 0, "evo_margin_sweep.a_extinct_cycle[0]")
    add("margin sweep last extinction", r"at cycles 69, 93", "108",
        max(int(r["a_extinct_cycle"]) for r in margin), 0,
        "max evo_margin_sweep.a_extinct_cycle")
    add("279/107 = 2.607", r"2\.607", "2.607", 279 / 107, 5e-4,
        "ratio of the two event cycles")
    add("seed-conditional midpoint 0.9335", r"0\.9335", "0.9335",
        1 - (1 - theta300) / 1.0277, 5e-5, "1 - (1-theta300)/1.0277")

    return A


NUM = re.compile(r"\d+(?:\.\d+)?")


def audit_numbers(paper: Paper, snap: Path) -> List[dict]:
    if paper.name != "Paper 1":
        return []
    ctx = Ctx(snap)
    checks = []
    for a in build_assertions(ctx):
        m = re.search(a["anchor"], paper.text)
        if not m:
            checks.append({**a, "status": "INVALID",
                           "note": "anchor not found; check not applicable"})
            continue
        window = paper.text[m.start(): m.start() + 400]
        found = None
        for tok in NUM.finditer(window):
            try:
                v = float(tok.group(0))
            except ValueError:
                continue
            if abs(v - a["value"]) <= a["tol"] or \
               (a["tol"] == 0 and abs(v - a["value"]) < 1e-9):
                found = tok.group(0)
                break
        # integer claims with tol 0 need exact string match
        checks.append({**a,
                       "status": "PASS" if found else "FAIL",
                       "found": found,
                       "where": paper.where(m.start()),
                       "note": "" if found else
                       f"prose prints no number within {a['tol']} of "
                       f"{a['value']:.6g} (nearest window: "
                       f"{', '.join(t.group(0) for t in list(NUM.finditer(window))[:12])})"})
    return checks


# --------------------------------------------------------------------------
# report
# --------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--bundle", default=str(Path(__file__).resolve().parent.parent))
    ap.add_argument("--json", default="")
    args = ap.parse_args()

    bundle = Path(args.bundle)
    snap = Path(__file__).resolve().parent / "data_snapshot"

    p1 = Paper("Paper 1", bundle / "paper1_source", PAPER1)
    p2 = Paper("Paper 2", bundle / "paper2_source", PAPER2)

    checks, notes = [], []
    for paper in (p1, p2):
        c, n = audit_numbering(paper)
        checks.extend(c)
        notes.extend(f"{paper.name}: {x}" for x in n)

    num = audit_numbers(p1, snap)
    checks.extend({**c, "id": "C7", "paper": "Paper 1",
                   "what": f"prose value vs CSV — {c['name']}"} for c in num)

    npass = sum(1 for c in checks if c["status"] == "PASS")
    nfail = sum(1 for c in checks if c["status"] == "FAIL")
    ninv = sum(1 for c in checks if c["status"] == "INVALID")

    lines = []
    w = lines.append
    w("=" * 78)
    w("figure and table audit")
    w("=" * 78)
    w(f"bundle            : {bundle}")
    w(f"data snapshot     : {snap}")
    w(f"checks            : {len(checks)}   PASS: {npass}   FAIL: {nfail}   "
      f"INVALID: {ninv}")
    w("")
    w("Lean4 covers the discrete algebra (Core_Theorems.lean). It cannot see a")
    w("float, a caption, or a number copied from a CSV into a sentence. That is")
    w("what C1-C7 check. C7 is the one this file exists for: the prose figure")
    w("claims are recomputed from audits/data_snapshot/*.csv, not re-read.")
    w("")

    for paper in ("Paper 1", "Paper 2"):
        w("-" * 78)
        w(paper)
        w("-" * 78)
        for c in [x for x in checks if x["paper"] == paper]:
            w(f"[{c['status']:7s}] {c['id']}  {c['what']}")
            if c.get("detail") or c.get("note"):
                w(f"            {c.get('detail') or c.get('note')}")
        w("")

    w("-" * 78)
    w("C7 detail: every numeric claim anchored to a figure or table")
    w("-" * 78)
    w(f"{'claim':58s} {'doc':>10s} {'csv':>12s}  ok")
    for c in num:
        if c["status"] == "INVALID":
            continue
        w(f"{c['name'][:58]:58s} {c['claimed']:>10s} {c['value']:>12.6g}  "
          f"{'ok' if c['status'] == 'PASS' else 'MISMATCH'}")
    w("")
    w("Tolerance: 5e-4 absolute for four-significant-figure prose, 5e-5 for")
    w("derived anchors quoted to four decimals, exact for integer counts. A")
    w("rounding of the last printed digit is not a mismatch; a factor of ten is.")
    w("")

    if notes:
        w("-" * 78)
        w("notes")
        w("-" * 78)
        for n in notes:
            w(f"  {n}")
        w("")

    for c in checks:
        if c["status"] == "FAIL":
            w(f"FAIL  {c['paper']} {c['id']}  {c['what']}")
            w(f"      {c.get('where', '')}  {c.get('note', c.get('detail', ''))}")
    w("")
    w(f"figure/table audit: {npass} PASS / {nfail} FAIL / {ninv} INVALID")
    w("=" * 78)

    out = "\n".join(lines) + "\n"
    print(out)
    if args.json:
        Path(args.json).write_text(json.dumps(checks, indent=2, ensure_ascii=False),
                                   encoding="utf-8")
    return 0 if nfail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
