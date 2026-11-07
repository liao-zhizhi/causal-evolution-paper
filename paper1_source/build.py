#!/usr/bin/env python3
"""Build Paper1.pdf from the markdown sources in this directory.

The markdown is the source of truth. This script does only what pandoc
cannot do on its own: wrap the abstract, lift the keyword line out of it,
promote display math carrying a \\tag into an equation environment, and
place the bibliography.

    Usage:  python3 build.py [--keep]
"""

import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BUILD = HERE / "build"

SOURCES = [
    ("00_Abstract.md", "abs.tex"),
    ("01_Introduction.md", "sec1.tex"),
    ("02_Method.md", "sec2.tex"),
    ("03_Results.md", "sec3.tex"),
    ("04_Discussion.md", "sec4.tex"),
    ("Appendix.md", "app.tex"),
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
\usepackage{microtype}
\usepackage{xcolor}
\usepackage[hidelinks]{hyperref}
\usepackage{caption}
\usepackage{float}
\usepackage{etoolbox}
\hypersetup{pdftitle={Causal Evolution Dynamics: Formalizing the Boundaries of Grounding and Hysteresis in Complex Systems},pdfauthor={Zhizhi Liao (廖至智)}}
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

\title{\bfseries Causal Evolution Dynamics: Formalizing the Boundaries of Grounding and Hysteresis in Complex Systems}
\author{Zhizhi Liao (廖至智) \\
Independent Researcher \\
\texttt{liaozhizhi@foxmail.com}}
\date{November 2026}

\begin{document}
\maketitle

"""

KEYWORDS_MARK = "**Keywords**"


def pandoc(md: str) -> str:
    proc = subprocess.run(
        ["pandoc", "-f", "markdown", "-t", "latex", "--wrap=preserve"],
        input=md, capture_output=True, text=True,
    )
    if proc.returncode != 0:
        sys.exit("pandoc failed:\n" + proc.stderr)
    return proc.stdout


def promote_tagged_display_math(tex: str) -> str:
    def repl(m):
        body = m.group(1)
        if r"\tag" not in body:
            return m.group(0)
        return "\\begin{equation}" + body + "\\end{equation}"

    tex = re.sub(r"\\\[(.*?)\\\]", repl, tex, flags=re.S)
    return tex.replace(r"$\square$", r"\hfill$\square$")


def split_abstract(text: str) -> tuple[str, str]:
    """Return (abstract body, keyword line) and drop the trailing editorial note."""
    head, sep, tail = text.partition(KEYWORDS_MARK)
    if not sep:
        sys.exit("build: the **Keywords** line was not found in 00_Abstract.md")
    keywords = tail.splitlines()[0].lstrip(": ").strip()
    head = re.sub(r"^#\s*Abstract\s*\n+", "", head.strip())
    return head, keywords


def main() -> int:
    BUILD.mkdir(exist_ok=True)
    fragments = {}

    for src, dst in SOURCES:
        text = (HERE / src).read_text(encoding="utf-8")
        if src == "00_Abstract.md":
            body, keywords = split_abstract(text)
            fragments["keywords"] = keywords
            text = body
        fragments[dst] = promote_tagged_display_math(pandoc(text))

    body = []
    body.append("\\begin{abstract}\n" + fragments["abs.tex"] + "\n\\end{abstract}\n")
    body.append("\\noindent\\textbf{Keywords:} " + fragments["keywords"] + "\n")
    for src, dst in SOURCES[1:]:
        body.append(f"% ===== {src} =====\n")
        body.append(fragments[dst])

    doc = PREAMBLE + "\n".join(body) + "\n\\end{document}\n"

    # pandoc rounds an equal-width fraction up (1/7 -> 0.1429); seven of them
    # then exceed \linewidth by 0.117pt and longtable reports an overfull box.
    # Shave the fraction back so the table is exact rather than nearly exact.
    doc = doc.replace(r"\real{0.1429}", r"\real{0.14285}")

    doc = doc.replace(
        "\\end{document}",
        "% Pull the reference list up by a line: without this its last entry lands alone\n"
        "% on a fresh page, which costs a whole page for three lines.\n"
        "\\vspace*{-0.9\\baselineskip}\n"
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
    pkgwarn = [ln for ln in text.splitlines() if "Warning" in ln
               and ln.startswith("Package")]

    print(f"passes: 3 + bibtex | overfull hbox: {len(overfull)} | "
          f"missing glyphs: {len(missing)} | latex warnings: {len(warnings)} | "
          f"package warnings: {len(pkgwarn)}")
    if missing:
        print("\n".join(missing[:10]))
    if overfull:
        print("worst overfull:")
        print("\n".join(sorted(
            overfull,
            key=lambda s: -float(re.search(r"\(([\d.]+)pt", s).group(1))
            if re.search(r"\(([\d.]+)pt", s) else 0)[:5]))
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
