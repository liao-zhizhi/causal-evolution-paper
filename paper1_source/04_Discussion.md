# 4. Discussion

## 4.1 The drought clock and systemic fragility

Corollary 4 of §2.6 states that for an agent whose commitment is fixed and whose
income stops at $t_c$,

$$
t_{\mathrm{death},i}=t_c+\left\lceil\frac{1}{m_{0,i}}-\delta\right\rceil,
$$

where $\delta$ is the accumulated deficit in units of the upkeep and $t_c$ is the
first cycle on which the delivered claim falls short. Two properties of this
expression matter more than its arithmetic.

**It is evaluated at $t=0$.** None of the quantities on the right-hand side is
discovered at runtime. $t_c$ is the first crossing of the capacity ratio below the
utilisation, and the utilisation and the drift schedule are design constants;
$\delta$ follows from the surplus accumulated while delivery still succeeded; and
$m_{0,i}$ is the upkeep rate, also a design constant. For the base configuration
these give $t_c=100$, $\delta=2.1$ and a death window of 104–107, and every one of
these numbers can be computed from `Params` and the scenario table before a single
agent is instantiated. The failure is therefore not an emergent property that
appears when the environment turns hostile. It is a scheduled event, and it was
scheduled at the moment the commitment was fixed above the capacity the system
would still have after the drift.

**It is a phase relationship, not a magnitude.** The formula contains no
comparison between the size of the shock and the size of the reserve. What
determines survival is whether the *period* of the external disturbance and the
*time constant* of internal recharge are commensurable. Four quantities appear:

| symbol | meaning | value here |
|:--|:--|:--|
| $P_{\mathrm{sh}}$ | period of the external disturbance | 23 cycles |
| $L$ | duration of one disturbance | 2 cycles |
| $\tau_{\mathrm{rec}}$ | recharge time of the reserve | $1/(m_0\phi_{\mathrm{dorm}}\chi)=3.125$ cycles |
| $1/m_{0,i}$ | drought survival time from full reserve | 5.5–8.6 cycles |

In the base run $L<\tau_{\mathrm{rec}}<1/m_0$, so a single episode is recovered
from and the population survives all four episodes. What kills is not the magnitude of
any episode but the duty cycle $L/P_{\mathrm{sh}}=8.7\%$, which sits below the
accounting threshold $\epsilon_m/(1+\epsilon_m)=13.04\%$. Changing the shock depth
from a capacity multiplier of $0.35$ to $0.85$ leaves the extinction at cycle 107
for all four values; changing the duration from 2 to 6 cycles moves it to 51
(§3.7). The system is sensitive to the duty cycle and insensitive to the depth,
and the accounting identity predicts both facts.

This is the sense in which the drought clock is a statement about systemic
fragility rather than about any single component. A system with a large reserve and
a slow recharge can be destroyed by a disturbance whose amplitude it would tolerate
if the disturbance came less often; a system with a small reserve and a fast
recharge can survive disturbances that are individually larger. Neither fact is
visible in a specification that reports only peak capacity, and neither is
visible in a specification that reports only average capacity. Both become visible
when the commitment, the reserve and the disturbance period are placed in the same
equation, which is all that Corollary 4 does.

**Where the argument does not extend.** The formula is exact for the accounting law
M2 and for the `PASS` branch; it inherits assumption A10 (atomicity) through
Proposition 2 and A28 through the saturation reference. It is a statement about a
system whose income is a step function of capacity. A system whose income degrades
continuously has no $t_c$ and therefore no clock; its failure is a slope, not a
date, and Corollary 4 says nothing about it. The sharpness of the result is a
consequence of the discontinuity, not of the dynamics.

## 4.2 Ledger deception and virtual delivery

The base run delivers 7676.93 units and records 8871.71. The difference, 1194.78 or
15.563%, is not noise, not rounding, and not an accounting error in the
implementational sense: it is an exact identity (§2.7),

$$
V=\sum_{\tau}\ \sum_{i\in\mathcal{A}:\ C_i(\tau)<c_i(\tau)} c_i(\tau),
$$

with $\mathcal{A}$ the Type-A agents: the sum of the claimed scope over all
Type-A cycles that did not deliver in full,
i.e. the `FAIL` and partial-scope `INVALID` rows of §2.7. In the base run the
Type-A `FAIL` count is zero, so the sum runs over `INVALID` cycles alone. The
number is large because the mechanism is systematic, and the mechanism is worth
naming precisely.

**Two ledgers, one report.** The classifier produces four values. Type-A's ledger
map is $\mathcal{L}_{\mathrm{self}}(\texttt{INVALID})=(0,c)$: zero credit, full
charge, and — this is the part that matters — the cycle is written into the record
as a completion. Type-B's map is $\mathcal{L}_{\mathrm{r7}}(\texttt{INVALID})=(C,C)$:
credit for the part that existed, charge for the part that existed, and the cycle
is written into the record as a refusal. Both maps are internally consistent. They
differ in what they do with a partial cycle, and the difference is 15.563% of the
output.

**Why the discrepancy is invisible from inside.** The recorded series is the
delivered series plus a term that is nonnegative, zero on every `PASS` cycle, and
positive exactly on the cycles that did not deliver in full --- the `INVALID`
cycles, in a run with no `FAIL`:

$$
R(t)-D(t)=\sum_{\tau\le t}\ \sum_{i\in\mathcal{A}:\ C_i(\tau)<c_i(\tau)} c_i(\tau)\ \ge\ 0 .
$$

No per-cycle figure of merit can therefore separate the two series, because they
are equal on the cycles that a monitor is asked to judge and differ only in the
accumulated offset. There is no cycle on which the record is *wrong*; there are
cycles on which the record is *complete* and the delivery is not, and the record
does not carry that distinction. A monitor watching the record sees a system
reporting completion; a monitor watching delivery sees a step. Both are looking at
the same run, and the difference between them is the 15.563%, which is not a
residual but the sum of the partial scopes.

**The magnitude is not the point; the absorbing class is.** Of the 708 `INVALID`
verdicts, 400 arise from eight shock cycles — four two-cycle episodes, fifty
agents each — and 308 from the terminal drought. The 400 are transient — capacity returns to its pre-shock level
on the cycle after each episode, and the reserve repays the deficit within
$\tau_{\mathrm{rec}}$ — and they were absorbed. What is fatal is that the same
classifier assigns the same value to a recoverable transient and to an
unrecoverable decline, and that the ledger map books both as completion. A
classification system that distinguishes the two would not need a different
dynamics, a better controller or a larger reserve. It would only need to stop
recording a partial cycle as a whole one.

**The ablation isolates this.** Section 3.6 changes nothing but the ledger map.
Under $\mathcal{L}_{\mathrm{self}}$ the population is extinct at 107; under
$\mathcal{L}_{\mathrm{r7}}$ it is alive at 300 with a gap of exactly zero. The
`INVALID` count *rises* from 708 to 4950, which is the measure of the
reclassification rather than a deterioration: those cycles were always partial,
and the channel merely stops calling them complete. The capacity trajectory, the
shock schedule, the seed and the population are identical in the two arms.

**What the ablation does not show.** The `r7` arm has no dormancy, because Type-A
never had any (I4). Its survival is the joint effect of the channel and the absence
of a dormant phase, and the stranding boundary of D5 is untouched by the channel. A
system that has both would still strand at 279. The claim supported by the ablation
is therefore exactly one claim, and it is narrow: *the ledger map alone, with the
environment held fixed, is sufficient to remove the extinction at 107.* It is not a
claim that a verdict channel confers survival in general, and it does not license
the reading that classification is a substitute for reserve.

**A caution about the statistic itself.** The 15.563% figure is a property of this
run, not a constant. It depends on how many cycles are partial, which depends on
the shock schedule and on the drift rate. What generalises is the identity, not the
percentage: a system whose ledger has no `INVALID` state will report a positive
virtual delivery equal to the sum of its partial scopes, and the ratio will grow as
the environment deteriorates. The base run's 15.563% is one sample of that growth
curve.

## 4.3 From unification to the dual regime

The earlier draft of this work contained a section titled "the one equation". Its
claim was that the active and dormant phases are two branches of a single law, and
that the apparent discontinuity between them is a notational artefact that a
sufficiently general formulation would remove. Proposition 1 and Appendix A.7
together decide the matter, and they decide it against that claim.

**Why the unification failed.** M1 is affine in $A$ with a nonzero slope
$-Y\phi_vv$; M2 is affine in $A$ with zero slope. A uniform limit of the first
family has slope $\lim(-a_n)$; for the limit to equal M2 that limit must be zero,
which makes M1's field independent of $A$; and then the field must equal M2's,
which varies in time because the delivered-minus-claimed balance is positive on
`PASS` and negative on `INVALID`. A constant cannot equal a sign-changing function,
so the only limits are the trivial ones in which both fields vanish. This is
Appendix A.7, and it is not a statement about our parameter choice: it holds for
every parameter value at which the systems are non-trivial.

**What follows for the general problem.** Three methodological consequences.

*First, a discontinuity is a finding, not a defect.* The switch at `Ax6` was
introduced to model a biological fact (a dormant cell does not perform
high-energy work) and then had to be defended as something other than a
mathematical embarrassment. The defence is that the two sides have genuinely
different structure, so the join is a modelling decision that must be declared, and
the paper's results then split cleanly: Theorem 1 is a theorem about M1, and the
107-cycle extinction is a corollary of M2. Neither is a theorem about "the
system".

*Second, smooth fitting of a hysteretic process produces confident wrong answers.*
The reason is Proposition 5: if the observable is affine-invariant, no amount of
data will detect a linear drift in it, and the fit will report a stable system with
a small residual. The error is not in the estimation but in the choice of a
statistic whose invariance class excludes the phenomenon under study. A framework
that insists on a single smooth law is forced to choose statistics that are
invariant to the switch, and those statistics are then blind to the thing that
matters.

*Third, the honest object is a pair of models with a stated interface.* We have two
laws, one switch, and a declared set of conditions under which each is valid. The
conditions are not decoration: H1 fails for entry through the verdict clause, and the
one-cycle verdict that ignored it produced a spurious left tail of the boundary
that took a rewrite to remove (§3.5). H2 holds at $\tau=3.125$ cycles with relative
error $10^{-4}$, but it is a condition and not a theorem. A28 holds with a margin
of 14 cycles, but it is an assumption and is listed as one (Appendix A.28).
Publishing the interface costs more prose than publishing a single equation, and
it is the only version of the claim that survives contact with its own audit.

**The limit of the lesson.** It would be easy to overstate this into a general
prohibition on unification. That would be wrong, and the counterexamples are
ordinary: the van der Pol oscillator \cite{vanderpol1926} has two regimes and is
one equation; the
Chapman–Enskog expansion recovers fluid dynamics from kinetics across a genuine
scale separation. What the present case shows is narrower — that when the two
branches have different *order* in the state variable (affine-with-slope versus
affine-without), no parameter path identifies them, and the burden of proof lies
with anyone who asserts a unified law. The claim is that the burden was not met
here, and that the failure is informative because the obstruction is structural
rather than technical.

---

## 4.4 The DPO Paradox: When the Loss Curve Commits a False Completion

We also tested whether preference optimisation could substitute for the runtime
witness (the reproduction record is `causal-alignment/` in the companion
repository, and the adapter's own `verification.json` is the witness).
Text-only DPO saturated its objective (reward accuracy 1.000 by step 60) yet
produced the grounded response on zero held-out prompts, suppressing only the
unwitnessed claim. Because the pairs encoded a surface contrast rather than an
observed effect, this bounds text-only preference tuning over *phrasings*, not
fine-tuning in general. A later 100-pair replication, in which every pair
carried a hash, an exit code and an exception string captured by executing the
action in a sandbox and reading the post-state from a separate sidecar, moved
the conditional decision but not the output contract: on ten live held-out
trajectories, forced-choice accuracy rose from 0.60 to 0.80 and false
completions fell from 4/4 to 1/4, while free-form generation still emitted no
verdict marker at all. With ten items and three discordant pairs in the
favourable direction, that shift is not distinguishable from noise, and the
decisive test therefore remains open — but it is now bounded from below, since
the first result was shown to be partly a property of the data rather than of
preference tuning as such. The result nonetheless illustrates the paper's point
one level up: the objective's margin is a tool-layer report, and
only an independent observation could reveal that the behaviour had not changed.

The DPO training run described here is, in microcosm, exactly the failure mode
this paper warns against: the scalar objective (loss margin) reported a perfect
success, while the independent witness (greedy decoding) proved nothing had
changed at the behavioural level.

Most strikingly, the untrained base model claimed PASS on all four failing
trajectories (4/4). This suggests that false completion is not an artifact of
the training objective, but the default prior of the pretrained model. The model
is an optimist by default; it generates success narratives because they are the
most probable continuation, not because it was trained to do so. This reframes
the problem: the challenge is not to fix a broken objective, but to overcome an
optimistic prior. Only an external witness can do that — or so we hypothesise,
since a prior observed at one model size under one instrument does not establish
that no other mechanism could.

One qualification: $4/4$ is a forced-choice statistic over two verdict tokens,
not a count of generated text. Left free to generate, the model issued no verdict
at all, and it returned `PASS` on the six successful trajectories as well. What is
optimistic here is the prior rather than the transcript.

> *Provenance and scope.* These figures come from the reproduction record named
> above rather than from `--audit-doc`, and are deliberately excluded from the 28
> audited claims: a number the audit cannot recompute has no place in the
> audited set. The result is one run, one seed, one model size, and three
> held-out prompts. It is reported as an external observation with its confound
> named — the preference data contained no witness reading to condition on — and
> not as evidence that fine-tuning cannot internalise grounding.

To truly confirm that fine-tuning can internalize causal grounding, future
experiments must move beyond offline text-only preference data. The model must
be placed in an online reinforcement learning loop where the reward signal is
derived from actual physical execution (exit codes, file hashes) audited by an
external sidecar. We hypothesize that only through such physical "pain" will the
model learn to proactively request a witness rather than falling into silent
abstention.

---

# 5. Conclusion

We set out to determine whether the failure of a self-reporting system under
declining capacity has a boundary that can be stated, proved and checked. It has
three, and none of them is a metaphor.

The dormant phase has an exact hyperbolic boundary,
$\chi_{\min}=1/(1-\theta_{\mathrm{wake}})$, conditional on entry, quasi-statics and
a wake rule, and it is a family rather than a number:
$\theta^\ast(t)=1-1/\chi(t)$, $0.9437$ at day one and $0.9317$ at cycle 300, with
the measured midpoint at $0.9325$ and the identity in Appendix A.5 explaining why
the two must coincide. The active phase has an atomic boundary at
$\rho=U$, which places the onset at cycle 100 and the extinction at 104–107 by
Corollary 4, computable in advance and matching the simulated multiplicities
$11,23,13,3$ exactly — a lead time of four to seven cycles from the onset. The ledger has a boundary too, and it is the one that is
usually missing: a partial cycle recorded as a whole one is a positive quantity,
1194.78 units here, and it grows as the environment deteriorates.

These are not three versions of one thing. They belong to two models with different
structure, joined by a declared assumption, and the attempt to unify them is what
Appendix A.7 refutes. The dual regime is not a compromise between rigour and
coverage; it is the correct description, and the boundary of each regime is
available.

What the framework provides, then, is narrower and more useful than a promise of
survival. Causal grounding — the four-valued verdict, wired into the ledger — does
not extend life. In the ablation it does not touch the stranding boundary, and a
system with both the channel and a dormant phase would still strand at 279. What it
changes is the *observability* of failure. Under $\mathcal{L}_{\mathrm{self}}$ the
extinction at 107 arrives with a record that reports completion on every cycle up
to the last, carries an offset of 15.563% that the record never discloses, and
contains no cycle on which it can be distinguished from a healthy one. Under
$\mathcal{L}_{\mathrm{r7}}$ the same extinction would be visible as a sequence of
`INVALID` verdicts, dated, attributably partial, and charged only for what existed.

That difference is not an optimisation. An optimisation improves a number that is
already being measured correctly; this changes what is measured. It is a choice
about which quantities a system is allowed to report about itself, and its
consequence is that a failure which was previously silent becomes a trace. A
system governed this way still dies of the drought clock — the clock is set by the
commitment and the drift, not by the ledger — but it dies with a record that can be
audited, and the audit can begin before the death rather than after it.

The reserve of a system is finite and its disturbances are periodic; against that,
no accounting scheme is decisive. Against silence, one is: a failure that is dated
and attributable can be acted upon, and a failure that is absorbed into a stable
record cannot. This paper's contribution is to have made the first kind of failure
the only kind the model can produce.

---

## 5.1 Limits of the present work

1. **Parameters are placeholders.** The eleven kinetic constants are dimensional
   shapes chosen so the system has both reserve and turnover; no number here is a
   prediction for a physical, biological or computational system. What is claimed
   is the structure of the boundaries, not their locations.
2. **One environment, one seed.** The population statistics are descriptive of the
   configuration tabulated in §2.9. Theorems 1 and Propositions 2–3 are per-agent
   and parameter-free up to their stated conditions; the ratios are not.
3. **The framework is a cohort survival model.** There is no reproduction,
   inheritance or interaction (A13, A14), so "evolution" is not literal. Selection
   could lower the utilisation, which is the most plausible adaptation available
   and is exactly what the model forbids.
4. **The ordering is not universal.** At $U\approx0.445$ Type-A outlives Type-B in
   the same code (A16). The result is conditional on the operating point.
5. **The `r7` arm conflates two changes.** It has the channel and no dormancy; only
   the channel is varied by design, and only the channel is claimed.
6. **Appendix A.7 is about non-existence.** It rules out identification of the two
   laws; it does not construct a better joint model. That construction is left
   open, and it is the natural next step.

7. **The LLM arm in §4.4 is a probe, not a result.** It is one model, one
   adaptation method, one seed, and ten held-out trajectories, and its numbers
   are deliberately outside the audited set. Its forced-choice shift
   ($0.60\to0.80$, three discordant pairs) is not separable from noise at that
   sample size. The claim it supports is narrow — that the earlier null was
   partly a property of the data — and it supports nothing about fine-tuning in
   general. An adequately powered version requires many more held-out
   trajectories and at least three seeds.

---

## 5.2 Reproducibility

`evolution_sim.py` regenerates every number in Sections 3 and 4 from one seed.
`--selftest` checks ten invariant groups, including the ablation, the gate
algebra and the shock-free confirmation rule. `--audit-doc` recomputes all 28
quoted quantities from the CSVs and prints `MISMATCH` for any that no longer hold.
The CSVs are byte-identical across re-runs. The four defects that the verification
report found in the previous implementation, and the numbers that changed because
of them, are documented there and referenced rather than paraphrased.
