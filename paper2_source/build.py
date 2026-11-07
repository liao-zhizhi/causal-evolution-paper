#!/usr/bin/env python3
"""Build paper.pdf from the markdown sources in this directory.

The markdown stays the source of truth. This script only does what pandoc
cannot do by itself: turn the `latex` fenced block holding the TikZ graph into
a real figure, wrap the abstract in an abstract environment, and promote
display math that carries a tag into an equation environment so that amsmath
accepts it.

Usage:  python3 build.py [--keep]
"""

import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BUILD = HERE / "build"
DAG_MARK = "DAGFIGUREHERE"

SOURCES = [
    ("00_Abstract.md", "abs.tex"),
    ("01_Introduction.md", "sec1.tex"),
    ("02_Method.md", "sec2.tex"),
    ("03_Results.md", "sec3.tex"),
    ("04_Discussion.md", "sec4.tex"),
]

PREAMBLE = r"""\documentclass[11pt,a4paper]{article}

\usepackage{fontspec}
\usepackage{xeCJK}
\setCJKmainfont{FandolSong-Regular.otf}[BoldFont=FandolSong-Bold.otf,
                                        ItalicFont=FandolKai-Regular.otf]
\setCJKsansfont{FandolHei-Regular.otf}[BoldFont=FandolHei-Bold.otf]
\setCJKmonofont{FandolFang-Regular.otf}
\usepackage[margin=1in]{geometry}
\usepackage{amsmath,amssymb,amsthm}
\usepackage{graphicx}
\usepackage{booktabs,longtable,array,calc}
\usepackage{tikz}
\usetikzlibrary{positioning,arrows.meta}
\usepackage{microtype}
\usepackage{xcolor}
\usepackage[hidelinks]{hyperref}
\usepackage{caption}
\usepackage{float}
\usepackage{etoolbox}
\hypersetup{pdftitle={The Mathematical Limits of AI Reliability: Inevitable Failure under Strong Causality},pdfauthor={Zhizhi Liao (廖至智)}}
\AtBeginEnvironment{longtable}{\small}
\setlength{\tabcolsep}{4pt}
\renewcommand{\arraystretch}{1.12}
\captionsetup{font=small,labelfont=bf,skip=6pt}
\graphicspath{{./}}
\setlength{\emergencystretch}{3em}
\setcounter{secnumdepth}{0}
\setcounter{tocdepth}{0}
\providecommand{\tightlist}{\setlength{\itemsep}{0pt}\setlength{\parskip}{0pt}}
\newcounter{none}
\AtBeginEnvironment{thebibliography}{\footnotesize\setlength{\itemsep}{0pt}\linespread{0.97}\selectfont}

\title{\bfseries The Mathematical Limits of AI Reliability\\[2pt]
\large Inevitable Failure under Strong Causality}
\author{Zhizhi Liao (廖至智) \\
Independent Researcher \\
\texttt{liaozhizhi@foxmail.com}}
\date{November 2026}

\begin{document}
\maketitle

"""


def strip_dag_block(text: str) -> str:
    """Swap the ASCII graph for a marker, and drop the TikZ source listing."""
    text = re.sub(r"<!-- include:begin -->.*?<!-- include:end -->", "", text, flags=re.S)
    text = text.replace("<!-- include:ascii-end -->", "")

    lines = text.split("\n")
    out, i, done = [], 0, False
    while i < len(lines):
        if not done and lines[i].strip() == "```":
            j, buf = i + 1, []
            while j < len(lines) and lines[j].strip() != "```":
                buf.append(lines[j])
                j += 1
            if any("\u25bc" in b for b in buf):
                out.append(DAG_MARK)
                i = j + 1
                done = True
                continue
        out.append(lines[i])
        i += 1
    if not done:
        sys.exit("build: the ASCII causal graph was not found in 02_Method.md")
    return "\n".join(out)


def pandoc(md: str) -> str:
    proc = subprocess.run(
        ["pandoc", "-f", "markdown", "-t", "latex", "--wrap=preserve"],
        input=md, capture_output=True, text=True,
    )
    if proc.returncode != 0:
        sys.exit("pandoc failed:\n" + proc.stderr)
    return proc.stdout


def promote_tagged_display_math(tex: str) -> str:
    """\\[...\\] does not accept \\tag under every amsmath setup; use equation."""
    def repl(m):
        body = m.group(1)
        if r"\tag" not in body:
            return m.group(0)
        return "\\begin{equation}" + body + "\\end{equation}"

    tex = re.sub(r"\\\[(.*?)\\\]", repl, tex, flags=re.S)
    # Push the end-of-proof marker to the right margin instead of letting it
    # wrap onto a line of its own.
    return tex.replace(r"$\square$", r"\hfill$\square$")


def as_abstract_body(tex: str) -> str:
    tex = tex.strip()
    tex = re.sub(r"^\\section\*?\{Abstract\}[ \t]*\n*", "", tex)
    return tex


def main() -> int:
    BUILD.mkdir(exist_ok=True)
    fragments = {}

    for src, dst in SOURCES:
        text = (HERE / src).read_text(encoding="utf-8")
        if src == "02_Method.md":
            text = strip_dag_block(text)
        tex = promote_tagged_display_math(pandoc(text))
        if src == "00_Abstract.md":
            tex = as_abstract_body(tex)
        fragments[dst] = tex

    body = []
    body.append("\\begin{abstract}\n\\noindent\n" + fragments["abs.tex"] + "\n\\end{abstract}\n")
    body.append("\\vspace{1.2em}\n")
    for dst in ("sec1.tex", "sec2.tex", "sec3.tex", "sec4.tex"):
        body.append(fragments[dst])

    doc = PREAMBLE + "\n".join(body) + "\n\\end{document}\n"

    figure = (
        "\\begin{figure}[H]\n\\centering\n"
        "\\input{figures/dag}\n"
        "\\caption{The causal graph of the hypotheses. $U$ is the environment's\n"
        "exogenous factor and the common cause of the truth $T$ and the record $O$;\n"
        "that edge is what makes the record informative. $O\\to V$ and $\\Pi\\to V$\n"
        "are the two inputs of a same-origin evaluator. The edge that is missing,\n"
        "$T\\to V$, is the hypothesis (D2.1), i.e. the factorisation identity of Proposition 7. The arrow\n"
        "$T\\to W$ is a witness: an arrow out of the truth that bypasses $O$.}\n"
        "\\label{fig:dag}\n\\end{figure}\n"
    )
    doc = doc.replace(DAG_MARK, figure)

    # The bibliography is generated by bibtex, so the document needs the
    # \bibliography hook before \end{document}.
    doc = doc.replace(
        "\\end{document}",
        "\\bibliographystyle{plain}\n\\bibliography{references}\n\\end{document}",
    )

    tex_path = HERE / "paper.tex"
    tex_path.write_text(doc, encoding="utf-8")
    print(f"wrote {tex_path.name} ({len(doc.splitlines())} lines)")

    def run_xelatex() -> tuple[int, str]:
        proc = subprocess.run(
            ["xelatex", "-interaction=nonstopmode", "-halt-on-error",
             "-file-line-error", "paper.tex"],
            cwd=HERE, capture_output=True, text=True,
        )
        return proc.returncode, proc.stdout

    log = []
    # Pass 1 writes the .aux that bibtex reads; pass 2 resolves \cite; pass 3
    # settles the page numbers of the bibliography items.
    code, out = run_xelatex()
    log.append(out)
    if code != 0:
        print(out[-6000:])
        print("BUILD FAILED on pass 1")
        return 1

    bib = subprocess.run(["bibtex", "paper"], cwd=HERE,
                         capture_output=True, text=True)
    if bib.returncode != 0:
        print(bib.stdout[-4000:])
        print("BUILD FAILED in bibtex")
        return 1

    for i in (2, 3):
        code, out = run_xelatex()
        log.append(out)
        if code != 0:
            print(out[-6000:])
            print("BUILD FAILED on pass", i)
            return 1

    text = log[-1]
    missing = [ln for ln in text.splitlines() if "Missing character" in ln]
    overfull = [ln for ln in text.splitlines() if ln.startswith("Overfull \\hbox")]
    warnings = [ln for ln in text.splitlines() if ln.startswith("LaTeX Warning")]

    print(f"passes: 3 + bibtex | overfull hbox: {len(overfull)} | "
          f"missing glyphs: {len(missing)}")
    if missing:
        print("\n".join(missing[:10]))
    if overfull:
        print("worst overfull:")
        print("\n".join(sorted(overfull, key=lambda s: -int(re.search(r"\(([\d.]+)pt", s).group(1)) if re.search(r"\(([\d.]+)pt", s) else 0)[:5]))
    for w in warnings[:12]:
        print(w)

    if "--keep" not in sys.argv:
        for junk in ("paper.aux", "paper.log", "paper.out", "paper.blg"):
            p = HERE / junk
            if p.exists():
                p.unlink()
        shutil.rmtree(BUILD, ignore_errors=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
