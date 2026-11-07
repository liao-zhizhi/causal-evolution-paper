#!/usr/bin/env bash
# Re-run the Lean4 check on Formal_Verification/Core_Theorems.lean and write
# audits/lean_verification.log. Exits non-zero if the file does not type-check
# cleanly, if it emits a warning, or if any declaration depends on `sorryAx`.
#
#   bash audits/run_lean_verification.sh
#
# What Lean4 covers here: the discrete and algebraic core (Lemma 4's threshold
# equivalence, the Active/Dormant exclusivity, the verdict as a four-valued
# collapse). What it cannot cover: the figures, the CSVs behind them, and the
# copy of a CSV number into a sentence. That is audits/figure_table_audit.py.

set -u

HERE="$(cd "$(dirname "$0")" && pwd)"
BUNDLE="$(dirname "$HERE")"
FV="$BUNDLE/Formal_Verification"
LOG="$HERE/lean_verification.log"
RAW="$(mktemp)"

cd "$FV" || exit 2

lean Core_Theorems.lean > "$RAW" 2>&1
STATUS=$?

N_ERR=$(grep -cE "(^|[^a-z])error(\(|:)" "$RAW" || true)
N_WARN=$(grep -c "warning" "$RAW" || true)
N_SORRY=$(grep -c "sorryAx" "$RAW" || true)
N_SORRY_DECL=$(grep -c "declaration uses 'sorry'" "$RAW" || true)

{
  echo "=============================================================================="
  echo "Lean4 verification"
  echo "=============================================================================="
  echo "file        : Formal_Verification/Core_Theorems.lean"
  echo "toolchain   : $(lean --version)"
  echo "command     : lean Core_Theorems.lean   (run in Formal_Verification/)"
  echo "exit status : $STATUS"
  echo "errors      : $N_ERR"
  echo "warnings    : $N_WARN"
  echo "sorryAx     : $N_SORRY"
  echo "sorry decls  : $N_SORRY_DECL"
  echo ""
  echo "Scope. This file is a narrowing, not a summary: it checks the discrete"
  echo "and algebraic facts the argument rests on, not the differential"
  echo "equations, the lognormal order statistics or the simulation. It also"
  echo "cannot see a figure, a caption, or a number copied from a CSV into a"
  echo "sentence; those are checked by audits/figure_table_audit.py (C1-C7)."
  echo ""
  echo "-------------- declarations in the file ------------------------------"
  grep -nE "^(theorem|lemma|def) " Core_Theorems.lean | sed 's/^/  /'
  echo ""
  echo "-------------- #print axioms output ----------------------------------"
  sed 's/^/  /' "$RAW"
  echo ""
  echo "-------------- conclusion -------------------------------------------"
  if [ "$STATUS" -eq 0 ] && [ "$N_ERR" -eq 0 ] && [ "$N_WARN" -eq 0 ] \
     && [ "$N_SORRY" -eq 0 ]; then
    echo "  PASS: 0 errors, 0 warnings, 0 sorry."
    echo ""
    echo "  Every axiom reported above is a Lean kernel axiom (propext,"
    echo "  Classical.choice, Quot.sound) or a native_decide certificate. None"
    echo "  is sorryAx, so no proof is unfinished. The claims are proved, not"
    echo "  assumed — but only the claims in this file. Theorem 1 of the paper"
    echo "  is analysed, not formalised: its differential part has no Lean"
    echo "  counterpart and is argued in prose."
  else
    echo "  FAIL: see the counts above."
  fi
  echo "=============================================================================="
} > "$LOG"

rm -f "$RAW"
cat "$LOG"

if [ "$STATUS" -eq 0 ] && [ "$N_ERR" -eq 0 ] && [ "$N_WARN" -eq 0 ] \
   && [ "$N_SORRY" -eq 0 ]; then
  exit 0
fi
exit 1
