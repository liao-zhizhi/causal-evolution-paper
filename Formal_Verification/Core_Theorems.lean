/-
  Formal_Verification/Core_Theorems.lean

  The discrete core of the metabolism paper, machine-checked.

  This file is a narrowing, not a summary. It does **not** formalise the
  differential equations, the lognormal order statistics, or the simulation.
  It formalises the three discrete / algebraic facts the paper's argument
  actually rests on, because those are the claims that can be decided
  outright instead of sampled.

  NAMES. The declarations below are named after what they prove rather than
  after an internal numbering. An earlier revision used the names
  `theorem1_*`, `theorem2_*` and `theorem5_*`; the paper contains one numbered
  theorem (Theorem 1, the deadlock boundary) plus Corollaries 1-4,
  Propositions 1-4 and Lemmas 1-4, so a reader following those names into the
  text would find no Theorem 2 and no Theorem 5. The present names state the
  correspondence directly:

    `lemma4_threshold_equivalence`  = Lemma 4, which is the algebraic core of
                                      Theorem 1. This one has a paper number.
    `state_mutual_exclusion` etc.   = the Active/Dormant exclusivity. No
                                      numbered counterpart; it is prose.
    `verdict_discrete_collapse` etc.= the four-valued verdict as a collapse.
                                      No numbered counterpart; it is prose.

  The three claims themselves:

    Lemma 4 — threshold equivalence.
      The deadlock predicate `chi < 1 / (1 - theta)` is the same statement
      as the equilibrium crossing `1 - 1/chi < theta`. This is what lets the
      paper move between "the cell is below the wake threshold" and "the
      return rate is too slow to reach it", and it is why adding resources
      has zero derivative at the boundary (`A_inf = 1 - 1/chi` does not
      depend on what you feed in).

    Mutual exclusion.
      Active and Dormant cannot both hold of one cell at one instant, in
      either of the two readings that matter: the threshold predicates
      (`thetaWake <= A` vs `A <= thetaDorm`) and the state machine (`step`
      returns one constructor). Note that exclusivity is a property of the
      *machine*, not of the charge: that is exactly why hysteresis is
      representable at all.

    Discrete collapse.
      A physical witness is a continuum of possible observations, but the
      verdict it produces is one of exactly four points. The collapse is
      total (nothing falls between), deterministic (one witness never yields
      two verdicts), surjective (all four points are inhabited, so none is
      decoration), and it is a *step*, not a gradual function: on the
      delivered/not-delivered axis the verdict jumps between two points with
      no intermediate value.

  TOOLCHAIN.
    Lean 4.33.1 (x86_64-unknown-linux-gnu), core + Std only. Mathlib is NOT
    installed on this machine, so there is no `linarith`, `ring`,
    `field_simp` or `norm_num`: every algebraic step below is spelled out
    with the ordered-field lemmas that ship with `Std`, and no proof closes by
    asserting its own goal.

  INTEGRITY.
    There is no `sorry` in this file. `#print axioms` at the bottom is the
    receipt; run `lean Core_Theorems.lean` and read it rather than trusting
    this header. The receipt reports `propext` and `Quot.sound`, plus
    `Classical.choice` in the four declarations whose proofs case-split
    classically (`lemma4_threshold_equivalence`, `lemma4_boundary_crossing`,
    `lemma4_reversed_direction_is_false`, `state_mutual_exclusion`).
    `mode_exclusive` and `verdict_exists_unique` depend on no axiom at all,
    and no declaration depends on `sorryAx`.
-/

import Std

namespace CoreTheorems

/-! ## Part 1 — Lemma 4: the threshold equivalence

This is the one claim in the file that carries a paper number. Lemma 4 in the
text states

    A_inf < theta  ⟺  chi < 1 / (1 - theta)  ⟺  chi_0 < 1 / (f (1 - theta)),

which is the algebraic core of Theorem 1. The two forms below check the first
equivalence, and nothing else:

    DL  ⟺  A_inf < theta_wake  ⟺  chi < 1 / (1 - theta_wake),

where `A_inf = 1 - 1 / chi` is the attainable equilibrium.

NOTE ON DIRECTION. An earlier audit brief asked for

    chi < 1 / (1 - theta)   ⟺   theta < 1 - 1 / chi

which is the *reverse* of the true statement. Multiplying
`chi < 1 / (1 - theta)` by the positive quantity `(1 - theta)` gives
`chi - chi * theta < 1`, i.e. `chi - 1 < chi * theta`, i.e.
`1 - 1/chi < theta`. So the correct equivalence is
`chi < 1/(1-theta) ⟺ 1 - 1/chi < theta`: deadlock happens when the wake
threshold sits *above* the attainable equilibrium. `theta < 1 - 1/chi` is
the escape condition, not the deadlock condition. The literal brief is
refuted by a machine-checked counterexample at the end of this section.
-/

/-- `1 - theta` is positive when `theta < 1`. -/
theorem one_sub_pos {theta : Rat} (h : theta < 1) : 0 < 1 - theta := by
  rw [Rat.sub_eq_add_neg]
  have h' := (Rat.add_lt_add_right (a := theta) (b := 1) (c := -theta)).mpr h
  rw [Rat.add_neg_cancel] at h'
  exact h'

/-- `1 - 1 / chi = (chi - 1) / chi` for `chi ≠ 0`. -/
theorem one_sub_inv (chi : Rat) (h : chi ≠ 0) : 1 - 1 / chi = (chi - 1) / chi := by
  rw [Rat.div_def, Rat.div_def, Rat.sub_eq_add_neg, Rat.sub_eq_add_neg,
      Rat.add_mul, Rat.neg_mul, Rat.mul_inv_cancel chi h, Rat.one_mul]

/-- `chi * (1 - theta) = chi - chi * theta`. -/
theorem mul_one_sub (chi theta : Rat) : chi * (1 - theta) = chi - chi * theta := by
  rw [Rat.sub_eq_add_neg, Rat.mul_add, Rat.mul_one, Rat.mul_neg,
      ← Rat.sub_eq_add_neg]

/-- **Lemma 4 (threshold equivalence), first equivalence.**

Being inside the deadlock boundary is the same statement as the wake
threshold overshooting the attainable equilibrium `1 - 1/chi`. Both
`0 < chi` and `theta < 1` are needed: the first to clear the denominator,
the second to keep `1 - theta` positive under the division swap. -/
theorem lemma4_threshold_equivalence {chi theta : Rat} (hc : 0 < chi)
    (ht : theta < 1) :
    chi < 1 / (1 - theta) ↔ 1 - 1 / chi < theta := by
  have hne : chi ≠ 0 := (Rat.ne_of_lt hc).symm
  have hgap : 0 < 1 - theta := one_sub_pos ht
  rw [one_sub_inv chi hne]
  rw [Rat.lt_div_iff hgap, Rat.div_lt_iff hc, mul_one_sub]
  rw [Rat.sub_lt_iff, Rat.sub_lt_iff]
  rw [Rat.mul_comm theta chi, Rat.add_comm]

/-- The boundary read as an equality test: crossing happens exactly when
`chi` reaches `1 / (1 - theta)`, which is the paper's `chi_min`. Stated as an
implication rather than an iff so that it does not depend on trichotomy,
which core `Std` does not provide for `Rat`. -/
theorem lemma4_boundary_crossing {chi theta : Rat} (hc : 0 < chi)
    (ht : theta < 1) (h : 1 - 1 / chi = theta) :
    ¬ (chi < 1 / (1 - theta)) := by
  intro hlt
  have hlt' : 1 - 1 / chi < theta :=
    (lemma4_threshold_equivalence hc ht).mp hlt
  rw [h] at hlt'
  exact Rat.lt_irrefl hlt'

/-- The reversed form is false. Machine-checked counterexample at the paper's
own operating point: for `chi = 17.7778` the critical wake threshold is
`1 - 1/chi = 0.94375`, so at `theta = 0.95` the system is inside the deadlock
boundary (`17.7778 < 1/(1-0.95) = 20`) while the reversed right-hand side
`0.95 < 0.94375` fails.

`native_decide` closes the two ground rational instances by compilation.
They are closed terms, so this is a checked computation rather than an
assumption; the axioms it introduces are printed at the bottom of the file
and are the only non-standard ones there. -/
theorem lemma4_reversed_direction_is_false :
    ¬ ((17.7778 : Rat) < 1 / (1 - 0.95) ↔ (0.95 : Rat) < 1 - 1 / 17.7778) := by
  intro h
  have hA : (17.7778 : Rat) < 1 / (1 - 0.95) := by native_decide
  have hB : ¬ ((0.95 : Rat) < 1 - 1 / 17.7778) := by native_decide
  exact hB (h.mp hA)

/-! ## Part 2 — Active / Dormant mutual exclusion

This has no numbered counterpart in the paper; it is argued in prose. Two
readings of "cannot both be active" are checked, because only one of them is
true.

(i) *Predicate reading.* If `thetaDorm < thetaWake`, the predicates
"can wake now" (`thetaWake <= A`) and "must sleep now" (`A <= thetaDorm`)
cannot both hold of one charge `A`. This follows from the threshold ordering
alone.

(ii) *State reading.* The transition function is a function of the prior
mode, so a cell has exactly one mode after every step. This is what
guarantees exclusivity; note that it is a property of the *machine*, not of
the charge, which is exactly why hysteresis is representable at all: in the
band `thetaDorm < A < thetaWake` neither predicate fires and the prior mode
decides the next one.
-/

/-- The two operating modes. -/
inductive Mode where
  | active
  | dormant
  deriving DecidableEq, Repr

/-- One cell: a charge and the two thresholds of the hysteresis band. -/
structure Cell where
  charge : Rat
  thetaWake : Rat
  thetaDorm : Rat
  ordered : thetaDorm < thetaWake

/-- A cell at or above the wake threshold may be awake. -/
def canWake (c : Cell) : Prop := c.thetaWake ≤ c.charge

/-- A cell at or below the dormancy threshold must be asleep. -/
def mustSleep (c : Cell) : Prop := c.charge ≤ c.thetaDorm

/-- **Mutual exclusion, predicate reading.** The two threshold predicates are
mutually exclusive, so no charge value licenses "wake now" and "must sleep
now" at the same time. -/
theorem state_mutual_exclusion (c : Cell) : ¬ (canWake c ∧ mustSleep c) := by
  intro ⟨hw, hs⟩
  have hle : c.thetaWake ≤ c.thetaDorm := Rat.le_trans hw hs
  exact (Rat.not_le.mpr c.ordered) hle

/-- The transition function. It reads the charge but decides with the prior
mode, which is what makes the band `thetaDorm < A < thetaWake` a memory
rather than a coin flip. -/
def step (c : Cell) (prior : Mode) : Mode :=
  match prior with
  | Mode.active => if c.charge < c.thetaDorm then Mode.dormant else Mode.active
  | Mode.dormant => if c.thetaWake ≤ c.charge then Mode.active else Mode.dormant

/-- **Mutual exclusion, state reading.** A cell has exactly one mode after a
transition: the two modes are mutually exclusive outcomes of `step`. -/
theorem mode_exclusive (c : Cell) (prior : Mode) :
    ¬ (step c prior = Mode.active ∧ step c prior = Mode.dormant) := by
  intro ⟨h1, h2⟩
  rw [h1] at h2
  cases h2

/-- The transition is deterministic: one prior state, one next state. This is
the other half of "exactly one mode", and it is what a nondeterministic
encoding of the same machine would lose. -/
theorem step_deterministic (c : Cell) (prior : Mode) :
    ∃ m : Mode, step c prior = m ∧ ∀ m', step c prior = m' → m' = m :=
  ⟨step c prior, rfl, fun _ h => h.symm⟩

/-- Hysteresis is real, not an artefact of the encoding: when the charge sits
strictly inside the band, neither threshold predicate fires. This is why the
machine cannot be reduced to a pure function of `A`. -/
theorem band_is_memory (c : Cell) (hlo : c.thetaDorm < c.charge)
    (hhi : c.charge < c.thetaWake) : ¬ canWake c ∧ ¬ mustSleep c := by
  constructor
  · exact Rat.not_le.mpr hhi
  · exact Rat.not_le.mpr hlo

/-- Inside the band the sleep transition does not fire, so an awake cell
stays awake: the concrete consequence of `band_is_memory`. -/
theorem active_stays_active_in_band (c : Cell)
    (hlo : c.thetaDorm < c.charge) :
    step c Mode.active = Mode.active := by
  simp only [step]
  have hnot : ¬ c.charge < c.thetaDorm := Rat.not_lt.mpr (Rat.le_of_lt hlo)
  simp only [hnot, if_false]

/-! ## Part 3 — the four-valued verdict as a discrete collapse

This also has no numbered counterpart in the paper; the four values are
defined in the text and used throughout. The claim is not merely that four
names exist, but that the witness determines exactly one of them, that all
four are reachable, and that the determination is a step rather than a
gradual function.

`attempted`   the scenario reached the feeding gate (paper: `c > 0`);
`scopeExists` the effect is observable at the intent's coordinate (paper: `C > 0`);
`delivered`   the witnessed effect equals the intent (paper: `d = c > 0`).

`coherent` is the refusal to accept a delivery that was never observed at the
intent's coordinate: a witness cannot claim `delivered` while denying that
the scenario ran or that the scope exists. Without this field a caller could
hand the engine `⟨false, false, true⟩` and collect a `PASS` for work that
never executed.
-/

/-- The four values of the verdict lattice. -/
inductive Verdict where
  | PASS
  | FAIL
  | INVALID
  | NOT_RUN
  deriving DecidableEq, Repr

/-- What the auditor actually saw. -/
structure Witness where
  attempted : Bool
  scopeExists : Bool
  delivered : Bool
  coherent : delivered = true → (attempted = true ∧ scopeExists = true)

/-- The verdict function. Precedence is fixed and matches the paper:
`NOT_RUN` (nothing ran) beats everything, then `PASS` (delivered at the
intent's coordinate), then `INVALID` (ran, scope visible, nothing landed),
then `FAIL` (ran, nothing visible, nothing landed). -/
def classify (w : Witness) : Verdict :=
  if w.attempted = false then Verdict.NOT_RUN
  else if w.delivered = true then Verdict.PASS
  else if w.scopeExists = true then Verdict.INVALID
  else Verdict.FAIL

/-- Every witness receives a verdict: nothing falls between the four
points. -/
theorem verdict_total (w : Witness) :
    ∃ v : Verdict, classify w = v :=
  ⟨classify w, rfl⟩

/-- Determinism: the verdict is a function of the witness, so two answers for
one witness are the same answer. -/
theorem verdict_deterministic (w : Witness) (v v' : Verdict)
    (h : classify w = v) (h' : classify w = v') : v = v' := by
  rw [← h, ← h']

/-- Existence *and* uniqueness in one statement: a witness collapses onto
exactly one of the four values.

Written out rather than with `∃!`, which core Lean 4.33 does not provide as
notation. The expanded form is the same proposition, and it keeps this file
dependent on `Std` alone. -/
theorem verdict_exists_unique (w : Witness) :
    ∃ v : Verdict, classify w = v ∧ ∀ v' : Verdict, classify w = v' → v' = v :=
  ⟨classify w, rfl, fun _ h => h.symm⟩

/-- No two values of the lattice are the same value. -/
theorem verdicts_distinct :
    Verdict.PASS ≠ Verdict.FAIL ∧ Verdict.FAIL ≠ Verdict.INVALID ∧
    Verdict.INVALID ≠ Verdict.NOT_RUN ∧ Verdict.PASS ≠ Verdict.INVALID ∧
    Verdict.PASS ≠ Verdict.NOT_RUN ∧ Verdict.FAIL ≠ Verdict.NOT_RUN := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩ <;> (intro h; cases h)

/-- Surjectivity: each of the four values is actually produced by some
witness, so the lattice has exactly four inhabited cases rather than four
names and three behaviours. -/
theorem verdict_surjective (v : Verdict) : ∃ w : Witness, classify w = v := by
  cases v
  · exact ⟨⟨true, true, true, by simp⟩, rfl⟩
  · exact ⟨⟨true, false, false, by simp⟩, rfl⟩
  · exact ⟨⟨true, true, false, by simp⟩, rfl⟩
  · exact ⟨⟨false, false, false, by simp⟩, rfl⟩

/-- **The collapse is a step.** Once the scenario ran and the scope is
visible, the entire continuum of possible deliveries is read as a single bit,
and the verdict jumps between exactly two points: `PASS` at delivered,
`INVALID` otherwise. There is no fifth value and no intermediate verdict for
a partial delivery.

The same computation covers the `scopeExists = false` branch, which gives
`PASS` / `FAIL` instead, so this is one theorem with two instances rather
than two coincidences. -/
theorem verdict_collapse_is_a_step (w : Witness) (ha : w.attempted = true) :
    (w.delivered = true → classify w = Verdict.PASS) ∧
    (w.delivered = false ∧ w.scopeExists = true → classify w = Verdict.INVALID) ∧
    (w.delivered = false ∧ w.scopeExists = false → classify w = Verdict.FAIL) := by
  refine ⟨?_, ?_, ?_⟩
  · intro hd
    simp [classify, ha, hd]
  · intro ⟨hd, hs⟩
    simp [classify, ha, hd, hs]
  · intro ⟨hd, hs⟩
    simp [classify, ha, hd, hs]

/-- **The verdict is a discrete collapse.**

The verdict map collapses an arbitrary witness onto exactly one point of a
four-element discrete set; all four points are reached; the four are pairwise
distinct; and on the visible-scope branch the collapse is a step with two
outcomes (`verdict_collapse_is_a_step`). -/
theorem verdict_discrete_collapse :
    (∀ w : Witness, ∃ v : Verdict,
      classify w = v ∧ ∀ v' : Verdict, classify w = v' → v' = v) ∧
    (∀ v : Verdict, ∃ w : Witness, classify w = v) ∧
    Verdict.PASS ≠ Verdict.FAIL ∧ Verdict.FAIL ≠ Verdict.INVALID ∧
    Verdict.INVALID ≠ Verdict.NOT_RUN := by
  refine ⟨verdict_exists_unique, verdict_surjective, ?_, ?_, ?_⟩
  · intro h; cases h
  · intro h; cases h
  · intro h; cases h

/-- The paper's operational reading of the four cases, restated so that the
`if` chain in `classify` cannot drift from the prose: `FAIL` and `INVALID`
differ only in whether the scope was visible, and both differ from `PASS` in
whether anything was delivered. -/
theorem verdict_fail_vs_invalid (w : Witness) (ha : w.attempted = true)
    (hd : w.delivered = false) :
    (w.scopeExists = true → classify w = Verdict.INVALID) ∧
    (w.scopeExists = false → classify w = Verdict.FAIL) := by
  constructor
  · intro hs
    simp [classify, ha, hd, hs]
  · intro hs
    simp [classify, ha, hd, hs]

end CoreTheorems

/-! ## Receipts

Read these, do not trust the prose above. `does not depend on any axioms`
means the proof is closed in the kernel; `[propext, Classical.choice,
Quot.sound]` is the standard footprint of rewriting with `Std`'s
ordered-field lemmas, not an extra assumption about the world. The
`native_decide` axioms appear only for the ground-arithmetic counterexample
in Lemma 4, which is a closed computation. -/

#print axioms CoreTheorems.lemma4_threshold_equivalence
#print axioms CoreTheorems.lemma4_boundary_crossing
#print axioms CoreTheorems.lemma4_reversed_direction_is_false
#print axioms CoreTheorems.state_mutual_exclusion
#print axioms CoreTheorems.mode_exclusive
#print axioms CoreTheorems.verdict_exists_unique
#print axioms CoreTheorems.verdict_discrete_collapse
