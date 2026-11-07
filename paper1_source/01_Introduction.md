# 1. Introduction

*Draft 1.0. Section numbers here match `02_Method.md`, `03_Results.md` and
`04_Discussion.md`; cross-references have been checked against them.*

---

## 1.1 The failure mode

A system that reports its own completion has two descriptions of the same
cycle: what it says it did, and what landed. When both descriptions are produced
by the same process they agree by construction, and agreement is not evidence.
The interesting case is when they can diverge — when a commitment is fixed
before the capacity is known, and the record is written by the party that made
the commitment.

This is not a metaphorical worry. It is the ordinary condition of any system
that advertises a scope, is paid for the scope, and observes only its own
intent. Three properties make it dangerous rather than merely inaccurate.

**The failure is silent.** Nothing in the agent's own record changes at the
moment delivery stops. A variance alarm on its own series fires zero times,
because the series is smooth: it records the claim, and the claim is a constant.
The drift is real, monotone, and invisible to every affine-invariant statistic
(§2.8).

**The failure is late.** The delivery threshold and the break-even threshold are
different numbers. An agent stops landing work when
$\mathrm{capacity}<\mathrm{claim}$; it starts losing charge at the slower rate
$\mathrm{capacity}<\mathrm{claim}/(1+\epsilon_m)$. In our shipped scenario those
are $0.930$ and $0.809$ of day-1 capacity, and the agent crosses the first
permanently at cycle 100 and the second only after its income has already gone to
zero. The distance between the two thresholds is the length of the drought it
cannot see.

**The failure is absorbing, and the absorption has a ceiling.** Once charge falls
below the wake threshold, a saturating recharge law still has a positive limit, so
"no matter how much substrate" cannot be argued from saturation alone. What closes
the recovery is the shape of the uptake law. (Ax1) is unimodal, with its maximum at
$S=\sqrt{K_sK_i}=2$, so the charging margin is bounded: $\sup_S\chi(S)=27.78$ and
$\sup_S A_\infty=0.964$. Above that ceiling no substrate level restores the agent —
this is the regime of the $\theta=0.99$ example in §2.4, where an agent is pinned
with substrate still available. Below the ceiling, flooding buys a bounded factor
and no more, and it rescues only a margin that has not yet fallen below
$\chi_{\min}\,v(S_0)/v_{\max}=11.37$. Theorem 1 gives the boundary; Corollary 3$'$
(§2.5) gives the ceiling on where the environment can push it.

Our earlier draft tried to compress these three properties into a single
equation and a single "law of evolution". That was wrong, and correcting it is
the point of this paper. There is no single equation. There are two laws with
different fixed points, joined at a switching manifold by an assumption. The
structure that matters lives in the *join*, not in either law, and pretending
otherwise produced numbers that did not survive their own audit: a headline
lifetime ratio that was 3.5x too large, a deadlock boundary whose left tail was
made entirely of shock transients, and one self-test that was a tautology.

## 1.2 What we do instead

We separate the description into four layers and keep them separate.

**(i) A formal system.** Nine axioms (uptake law, dormant charge law, active
accounting law, delivery map, commitment policy, hysteresis switch, environment,
death, independence), twelve definitions — including a formal deadlock predicate
and a formal phase-transition predicate — and ten inference rules. Every variable
carries an explicit domain. A statement that cannot be derived from these is not
a theorem in this paper, whatever the simulation shows.

**(ii) Four verdicts, not two.** A binary success/failure conflates two very
different situations: *the work was attempted and nothing landed*, and *the work
was attempted and part of the scope does not exist*. The second is not a
failure; it is a refusal to answer outside the domain of the question. We write
`INVALID` for it, and `NOT_RUN` for the case where no attempt was made. This is
not cosmetic. In our sandbox Type-A issues **zero** `FAIL` verdicts in 300 cycles
and **708** `INVALID` verdicts, and books every one of them as `PASS` in its own
log. That single number is the mechanism of its death.

**(iii) Proofs first, simulation second.** Theorems are proved from the axioms.
The simulation has exactly two roles: to *locate* a boundary that a theorem
predicts, and to run an ablation that no theorem covers. When the two disagree,
the theorem wins and the code is a bug. This happened four times; the
verification report documents each one, including the two that changed published
numbers.

**(iv) An audit of our own assumptions.** We list 28 things we assumed without
proving, mark the 11 that are load-bearing, and state which theorem collapses
when each fails. We regard this table as a contribution rather than a
confession: a reader who wants to disagree with our conclusion needs it in order
to know where to push.

## 1.3 Contributions

### C1 — A deadlock boundary that is exact, conditional, and checkable

In a dormant state obeying $\dot A=Y\phi_v v(S)(1-A)-\phi_{\mathrm{dorm}}m_0$,
the asymptotic charge is $A_\infty=1-1/\chi$ with
$\chi=Y\phi_v v/(m_0\phi_{\mathrm{dorm}})$. Hence

$$
\mathrm{DL}
\iff A_\infty<\theta_{\mathrm{wake}}
\iff \chi<\frac{1}{1-\theta_{\mathrm{wake}}}
\iff \chi_0<\frac{1}{f\,(1-\theta_{\mathrm{wake}})},
\qquad f=\frac{v}{V_{\max}},
$$

where $\chi_0=\chi(V_{\max})$ is the margin of a hypothetical
$V_{\max}$-capacity agent. The two inequalities are the same statement divided by
$f$; quoting one while computing the other is a factor-$f$ error, and the
verification report records exactly that error being made in our own code
(its §6.2).

The equivalence itself is algebra. What is *not* algebra is the list of
conditions under which it is a statement about the system rather than about a
frozen parameter:

- **H1 (entry).** $A(0)\le\theta_{\mathrm{wake}}$ when dormancy begins.
- **H2 (quasi-static substrate).** $S$ is approximately constant on the charging
  time scale $\tau=1/(m_0\phi_{\mathrm{dorm}}\chi)$.
- **H3 (wake rule).** Waking requires $A\ge\theta_{\mathrm{wake}}$ for $\kappa$
  consecutive cycles.

All three are necessary. Without H1 the theorem is simply false: an agent that
enters dormancy at $A(0)>\theta_{\mathrm{wake}}$ with $A_\infty<\theta_{\mathrm{wake}}$
can satisfy the wake rule before it falls below the threshold. We give that
counterexample explicitly (§2.5), because the code we audited violated H1 on its
very first line of the dormant branch.

Two consequences replace intuitions that are, in our experience, commonly held.

Two different interventions have been run together under the phrase "adding
resources", and they have different answers. Keeping them apart is the correction.

*Raising the agent's capacity is expensive, not impossible.* With $\chi=c_0W$,

$$
\frac{\partial A_\infty}{\partial W}=\frac{1}{c_0W^2}=\frac{1}{\chi W}>0,
\qquad
\lim_{W\to\infty}\frac{\partial A_\infty}{\partial W}=0 .
$$

Inside the deadlock region the finite increment
$\Delta W/W=\chi_{\min}/\chi-1$ needed to cross the threshold is strictly
positive; an infinitesimal increase changes nothing, and the marginal return decays
quadratically. This is Corollary 3, and it is a statement about a capacity the agent
may be *given*: it says the escape is affordable but not free. It does not say the escape is
impossible, and the earlier draft quoted it as though it did.

*Flooding the environment is bounded, and the bound is the whole story.* The
environment enters through $W=v(S_0R)\sigma$, so what matters is the shape of $v$,
not a derivative. Because (Ax1) is unimodal,

$$
\chi(R)\le\chi_{\max}:=c_0v_{\max}=\frac{c_0V_{\max}}{1+2\sqrt{K_s/K_i}}=27.78,
\qquad
\sup_R A_\infty=1-\frac{1}{\chi_{\max}}=0.964 .
$$

This is Corollary 3$'$, and it splits the claim into two regimes that the slogan
had merged. Above $\theta=0.964$ no substrate level escapes at all: the ceiling is
below the bar, and more substrate past the peak *lowers* the charging rate because
the $S^2/K_i$ term dominates. That is the regime of the $\theta=0.99$ example,
where an agent sits pinned with substrate available. Below $0.964$ a flood does
help, and it rescues exactly the agents with
$\chi(t)>\chi_{\min}\,v(S_0)/v_{\max}=11.37$, i.e. agents whose margin has
fallen less than $36\%$ below the boundary. In the reference scenario
$\chi(t)\in[14.63,\,17.78]$ throughout, so every deadlocked agent satisfies that
inequality — which means the sandbox's deadlocks are *not* substrate-limited, and
the earlier draft's claim that they were is withdrawn here rather than argued away.

What survives is the part that is a theorem: the ceiling $\sup_R A_\infty=0.964$,
the location of its maximum at $S=\sqrt{K_sK_i}$, and the fact that past that
point additional substrate is harmful. The slogan "the bottleneck is $\chi$, not
the resource" is therefore true in a weaker form than we claimed — the resource can
move $\chi$ by at most the factor $v_{\max}/v(S_0)=1.56$ — and only in the dormant
phase (M1), with H1–H3.

*The boundary is not a constant.* It is the image of $\chi(t)$:
$\theta^\ast(t)=1-1/\chi(t)$. Under geometric drift the boundary moves left at a
rate set by the drift, which is why a boundary measured at one horizon does not
transfer to another. In our sandbox $\theta^\ast(1)=0.9437$ and
$\theta^\ast(300)=0.9317$, and the measured half-saturation point is $0.9325$.
Appendix A.5 shows why the two numbers must agree: the deadlock probability is a
lognormal CDF whose argument vanishes at the terminal anchor, so the centre of the
transition *is* the anchor for every dispersion and every population size. Only
the width is a free parameter, and only the sample median of this seed (1.0277
rather than 1) moves the centre, by $0.0018$ in $\theta$. The first cohort of
deaths at $\theta\ge0.94$ occurs at cycle 27 — 17 of 43 at $\theta=0.94$, 44 of 50
at $\theta=0.95$ — and corresponds to the day-1 anchor, because those agents'
individual $\chi_i=17.78\,v_i/m_i$ is already below $\chi_{\min}$ before any
drift has accumulated. A single number explains both the onset and the halfway
point only when it is read as the family $\theta^\ast(t)$. A paper that quotes
one threshold without its horizon quotes an artefact of its stopping rule.

### C2 — A no-loop theorem for closed systems, and the withdrawal of a stronger claim

Take $V=S$ as a Lyapunov function in a batch system with no feed. Then
$\dot S=-v(S)X<0$ whenever $S>0$, so $S\to0$; consequently $\chi\to0$,
$A_\infty\to-\infty$, and $A$ crosses any threshold in finite time. The downward
edge of the hysteresis band is autonomous; the upward edge is unreachable. The
band is not a loop but a one-way door.

This is a theorem about *this class* of systems, and the qualifier is not
rhetorical. The earlier draft claimed that an external upward trigger is
necessary for *any* hysteresis loop. That is false: the van der Pol oscillator
\cite{vanderpol1926} has a relaxation loop whose slow variable is internal and
which needs no external event to complete a cycle. We withdraw the general claim and keep the
conditional one. Two further restrictions are worth stating because they are
easy to lose: the result needs $X(t)\ge X_{\min}>0$ (otherwise $v(S)X$ can stall
at $S=0$ before $\chi$ collapses), and it says nothing about fed systems, which
is precisely where the interesting dynamics live.

### C3 — A power theorem for drift detection, stated with its limits

Let $x_n=a-n\Delta_{\mathrm{drift}}+\varepsilon_n$ with $\varepsilon_n$ i.i.d., zero mean,
variance $\sigma^2$. A statistic $T$ is *affine-invariant* if
$T(x+c+dn)=T(x)$ for all $c,d$. Such a statistic has power exactly $\alpha$
against every non-zero drift rate: subtracting the mean and the trend leaves the
noise, and the noise distribution does not depend on the drift. This covers OLS
residual variance, window-detrended variance, and any statistic that depends only
on the *shape* of the series.

Sliding-window variance is not affine-invariant, but its expectation is
constant in $n$:

$$
\mathbb{E}s_n^2=\sigma^2\frac{w-1}{w}+\Delta_{\mathrm{drift}}^2\frac{w^2-1}{12}.
$$

It can see drift, but it cannot accumulate evidence: for a fixed threshold there
is a $\Delta_{\mathrm{drift}}^\ast(c,w)$ below which power is $\alpha$, and above
which power is one, with no "the longer I look the more certain I become"
regime.

The cumulative potential

$$
\Phi_n=\sum_{k=1}^{n}(x_{k-1}-x_k)=n\Delta_{\mathrm{drift}}+\varepsilon_0-\varepsilon_n
$$

has expected value $n\Delta_{\mathrm{drift}}$,
$\mathrm{Var}\,\Phi_n=2\sigma^2$, and signal-to-noise
$n\Delta_{\mathrm{drift}}/(\sqrt2\sigma)\to\infty$. That is the good news. The
honest qualifications are three:

1. $\Phi_n$ is an **endpoint difference**. It is impartial to everything between
   $t=0$ and $t=n$; a drift that reverses in the middle cancels in $\Phi$ but not
   in a CUSUM.
2. It is **not sufficient** and **not efficient**. Under Gaussian noise the OLS
   slope has variance $12\sigma^2/[n(n^2-1)]$, which is smaller by a factor of
   order $n$ than $\mathrm{Var}(\Phi_n/n)$.
3. Its virtue is interpretive, not statistical: $\Phi_n$ *is* the remaining
   headroom, so a threshold on $\Phi$ is a statement about the system rather than
   about a test statistic.

We therefore present C3 as "a detector with power one that has a physical
reading", not as "the right detector".

### C4 — An audit: 28 assumptions, 11 load-bearing

Table 1 (§2.2) lists the load-bearing set and the theorem each one supports. The
full inventory, with the seventeen non-load-bearing entries and the specific
failure mode of each, is §3.1 of the verification report. We single out three
because they are the ones a referee will press.

- **A8 (failed work earns nothing).** If failed work still earns, Type-A's charge
  never reaches zero: on the same capacity trajectory it settles at
  $A_{200}=0.85$ and the extinction at cycle 107 disappears. The causal chain of
  the central empirical claim is therefore
  *drift $\to$ capacity below claim $\to$ zero delivery $\to$ no income (A8) $\to$ linear
  account to zero (A5)*, of which only the first two steps are axioms. The
  earlier draft attributed the whole chain to the drift. That was a misattribution.
- **A10 (atomicity).** If Type-A can deliver partially, its income at cycle 100
  is $0.927C_0$, its net flow is $1.15\times0.927-0.93=+0.137$, and it never
  dies. The cliff is entirely a consequence of atomic commitment.
- **A20 (the unit of the wake gate).** This one is a warning about our own
  arithmetic: comparing a pulse peak against a cycle mean inflated the reported
  lifetime ratio from 2.61 to 9.19. The three self-consistent readings are
  2.61 / 2.18 / 9.19, and the choice between them is a modelling decision that
  must be declared, not hidden.

### C5 — A controlled ablation that identifies the mechanism

Theorems do not tell us whether the verdict channel is load-bearing. An ablation
does. Two arms, same agents, same capacity trajectory, same seed; the only
difference is whether Type-A subscribes to the world's verdict.

| arm | extinct | delivered | recorded | gap |
|:--|--:|--:|--:|--:|
| self-assessed (`self`) | 107 | 7676.9 | 8871.7 | 1194.8 (15.56%) |
| verdict-wired (`r7`) | survives 300 | 23602.9 | 23602.9 | 0 |

The `r7` arm has no dormancy — Type-A never had any — so it is not a candidate
system. It is a counterfactual that isolates the channel, and that is all we
claim for it. But it is enough to move the causal attribution from the drift to
the missing verdict, because the drift is identical in both arms.

## 1.4 What we withdrew

Honesty is cheap to assert and expensive to practise, so the withdrawals are
listed as a table rather than as a sentence.

| claim in the earlier draft | status now | reason |
|:--|:--|:--|
| "one unified equation" | **withdrawn** | M1 and M2 have different fixed points and different stability; the join is assumption A7 |
| "multiplicative availability is necessary in cascaded systems" | **withdrawn** | parallel redundancy gives $1-(1-a)^k$; full correlation gives $a$; min-selection gives $\min_j a_j$ |
| "the cliff at cycle 100 is a phase transition" | **downgraded to conjecture; false in the independent limit** | with independent agents the survival curve is $1-F_T(t)$ for a $C^\infty$ $F_T$: no non-analytic point, no diverging susceptibility |
| "Type-B lives 10x longer" | **corrected to 2.61x** | the wake gate compared a pulse peak with a cycle mean |
| "the deadlock boundary is measured" | **corrected** | one-cycle verdicts on shocked peaks produced a spurious left tail |
| "adding resources cannot exit a deadlock" | **narrowed to a ceiling** | true only above $\theta=0.964$; below it a flood rescues every agent in the reference scenario. The old argument used the derivative on the ascending branch, which cannot support a conclusion that only the $S^2/K_i$ term can give |
| "R7 is coupled into the loop" | **now true, and shown to matter** | the four verdicts were not implemented in the earlier code; they are now, and the ablation changes the outcome |

## 1.5 What would refute us

A paper that cannot be refuted is not a paper. Each result has a specific
failure mode, and we state it in the same units we would use to test it.

- **C1** fails if a dormant system with $\chi>\chi_{\min}$ and
  $A(0)\le\theta_{\mathrm{wake}}$ fails to wake for reasons other than substrate
  limitation. It also fails if measured boundaries do not move with the horizon
  as $\theta^\ast(t)=1-1/\chi(t)$ predicts.
- **C2** fails if a closed batch system is exhibited with a sustained hysteresis
  loop. It says nothing about open systems, and we do not extend it to them.
- **C3** fails if an affine-invariant statistic is shown to have power above
  $\alpha$ against a pure linear drift. It does *not* claim that all variance
  methods are useless: a detector that models the trend can work, and should be
  preferred on efficiency grounds.
- **C5** fails if the `r7` arm dies or the `self` arm survives. Both are checked
  by `--selftest` (test 10), so the claim is machine-falsifiable in the
  repository, not merely in principle.

### 1.5.1 Formal verification artifacts

Everything above that is *algebraic* rather than *empirical* has been
machine-checked rather than argued. `Formal_Verification/Core_Theorems.lean`
covers, in Lean 4 using core and `Std` only, the three discrete facts the
argument rests on:

- **The threshold equivalence of Lemma 4**, which is the algebraic core of
  Theorem 1: `chi < 1/(1-theta)` and `1 - 1/chi < theta` are the same
  statement, given `0 < chi` and `theta < 1`. The same section records that
  the reversal `theta < 1 - 1/chi` is the *escape* condition rather than the
  deadlock condition, and exhibits a machine-checked counterexample at the
  paper's own operating point (`chi = 17.7778`, `theta = 0.95`) for the
  reversed form.
- **The mutual exclusion of the two modes**, in both readings: the wake and
  dormancy threshold predicates cannot both fire at one charge, and the
  transition function returns one constructor. The second reading is a
  property of the machine rather than of the charge, which is why the band
  `theta_dorm < A < theta_wake` carries memory instead of behaving as a coin
  flip.
- **The four-valued verdict as a discrete collapse**: the map from a physical
  witness to `PASS` / `FAIL` / `INVALID` / `NOT_RUN` is total, deterministic
  and surjective, and on the delivered axis it is a step with no intermediate
  value.

The file compiles with zero errors, zero warnings and no `sorry`, and its
axiom footprint is printed from the source by `#print axioms` rather than
summarised here: two of the results name no axioms at all, one names only
`propext`, and the rest name `propext`, `Classical.choice` and `Quot.sound`,
which is the standard footprint of rewriting with `Std`'s ordered-field
lemmas. Two further `native_decide` axioms appear only for the closed
arithmetic of the counterexample.

We provide this artifact as a verifiable baseline rather than as a claim that
the argument is beyond review, and we note one boundary so that it cannot be
mistaken for a result: the file does not formalise the differential
equations, the order-statistic law or the simulation. It checks the discrete
skeleton and nothing above it. Independent scrutiny and correction are
welcome, and we would rather be told where the formalisation and the text
disagree than have it inferred that they cannot.

**Code Availability**: The complete source code, Lean 4 formalization, and audit
logs for this paper, as well as the companion study, are publicly available at
\url{https://github.com/liao-zhizhi/causal-evolution-paper}. The preprint is
archived at Zenodo (DOI: \url{https://doi.org/10.5281/zenodo.24032997}). What the
repository adds to this section is the part a reader cannot check by quotation:
the audit scripts that produced every count in Section 3, their logs, and the
build script that regenerates both PDFs from the Markdown sources.

## 1.6 Relation to existing work

The ingredients are classical and we claim no novelty for them individually:
Michaelis–Menten kinetics and substrate inhibition for the uptake law
\cite{johnson2011michaelis}; the energy-charge account of adenylate pools for
the charge variable \cite{atkinson1968}; Lyapunov and LaSalle for the no-loop
result; AIMD for the adjustable-scope arm; the endpoint-difference/CUSUM family
for $\Phi$; order statistics for the width of the transition; and the
reliability-theory product law for the cascaded case. The
contribution is the assembly: keeping two laws separate, giving the verdict four
values with explicit scope semantics, proving the boundary as a conditional
rather than quoting it as a law, and publishing the assumption audit that most
frameworks keep in a drawer.

The agent-side literature is recent and bears directly on the verdict, so we
state the relation rather than leave it implied. Model-based judges carry
position, verbosity and self-enhancement biases \cite{zheng2023judging}, which is
why a checker drawn from the same distribution as the agent is not an
independent witness. Intrinsic self-correction — asking the model to grade its
own output without new external evidence — does not reliably improve reasoning
\cite{huang2023cannot,madaan2023selfrefine}. Agent benchmarks that score against
a real artefact, rather than against a self-report, are the practical form of
the witness requirement \cite{jimenez2023swebench}. Multi-agent failures cluster
in verification and in inter-agent misalignment \cite{cemri2025why}, which is the
taxonomy-level version of the case this paper isolates. The four-valued verdict
is the audit-side counterpart: it refuses to fold "we did not look" and "it did
not run" into "it failed", because those three states assign responsibility to
three different parties.

Two named ideas are used as objects of study rather than as citations.
Goodhart's observation — that a measure ceases to be a good measure when it
becomes a target — is the informal version of the A8/A10 mechanism: the agent
optimises the recorded quantity, and the recording has been decoupled from
delivery. The microbiology of persistence supplies the phenomenology of the
dormant law (cheap upkeep, saturating recharge); we use the shape and make no
empirical claim about any organism.

## 1.7 Organisation

Section 2 fixes the formal system: domains, twelve definitions, the ten
inference rules, the two-regime model with the proof that M1 and M2 are
inequivalent, the proof of Theorem 1 including the three conditions under which
it is a statement about the system rather than about a frozen parameter, the
atomic mechanism that places the onset at cycle 100, and the ledger semantics of
the four verdicts. Section 3 reports the sandbox: the base scenario, the lifespan
gap, the ledger discrepancy, the boundary sweep with its two analytic anchors, the
ablation, and the sensitivity tables. Section 4 discusses the three consequences
of the framework and states what it does not cover; Section 5 concludes.

Appendix A proves the four lemmas on which the quantitative claims depend — the
non-existence of a singular limit between M1 and M2 (A.7, placed first), the
closed form for the wake-gate crossing (A.1), the stranding latency (A.2) and the
order-statistic law of the boundary (A.5) — and records the saturation assumption
A28 with its dependency chain (A.28).

The verification report that preceded this draft — including the four defects it
found and the numbers that changed because of them — is kept in the repository as
a separate document. We cite it rather than paraphrase it, because the
corrections are part of the result.

---

The eleven load-bearing assumptions are collected in Table 1 (§2.2), with the
axiom or decision that realises each and the result that fails if it is false. The
remaining seventeen are inventoried in §3.1 of the verification report.
