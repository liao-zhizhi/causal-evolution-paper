# 4. Discussion

## 4.1 What a benchmark measures

The word "reliability" is used for two different quantities, and the confusion is
not terminological. Let $V$ be a system's answer and $V'$ the answer its grader
would give. A benchmark reports agreement,
$$
\mathrm{score}=\Pr[V=V'],
\tag{4.1.1}
$$
while reliability is truth,
$$
\mathrm{acc}=\Pr[V=T].
\tag{4.1.2}
$$
These are unrelated orderings on the same systems. When $V$ and $V'$ share a
channel and a prior — the grader is the same model~\cite{zheng2023judging}, or a
model trained on the same distribution, or a rule written by the same team from
the same data — the agreement can be brought arbitrarily close to $1$ at any
level of accuracy.
$\Pr[V=V']=1$ is compatible with any value of $\Pr[V=T]$ whatsoever; in the
measured instance the two coexisted at $1.00$ and $0.60$, the second being exactly
the accuracy that constancy implies — the base rate of success in the sample, not
one point above it.

This is the precise sense in which a benchmark measures complicity rather than
capability. The score of (4.1.1) is a functional of the joint law of $(V,V')$ and
carries no term in $T$. It cannot, therefore, distinguish a system that reads the
world from a system that reads its own prior and reports what the prior expects.
On the bulk of a distribution the two are hard to separate and the distinction
hardly matters. On the tail they separate completely — and the tail is where the
tasks are worth automating. A braking system is not graded on the roads it has
seen a million times; it is graded on ice, at load, at night.

Corollary 1 gives the reason this is not merely a complaint about metric design.
$I(V;T)\le I(V;(O,\Pi))$: whatever a score can measure has already passed through
the record and the prior. There is no term in the score that could carry
information the pair did not already carry, and therefore no reweighting, no
harder subset, and no larger model can turn a same-origin score into a measurement
of causal capability. What such a score measures, when it is high, is the
coherence of a prior with itself.

The practical consequence is uncomfortable and follows directly. A benchmark
suite built by the same organisation that built the system, evaluated on data
drawn from the same pipeline, adjudicated by a grader sharing the same weights,
has an upper bound on what it can detect — and that bound is the information in
$O$. On the long tail, where the record determines almost nothing, the bound is
almost nothing, and a score of $1.00$ there is a statement about shared blind
spots.

## 4.2 Why the witness is not an optimisation

It would be natural to read §3.3 as an argument for a better evaluator. It is the
opposite, and Corollary 3 is the reason. The value of adding a witness is
$$
\Delta_{\mathrm{wit}}=I\big(W;T\mid O,V\big)\ \le\ I\big(W;T\mid O\big),
\tag{4.2.1}
$$
with equality on the tail, by (2.8.7$''$), and the right-hand side contains no term
in $\phi$. Whatever the evaluator's
quality, the marginal value of the witness is capped by what the witness itself
knows about the truth beyond the record. Improving $V$ cannot raise that cap;
only changing $W$ can. The evaluator and the witness are not on a single scale of
"quality", and the intuition that a sufficiently good judge would make an external
check redundant is exactly the intuition Theorem 2 forbids.

This is why we describe the intervention as a rescue rather than an optimisation.
An optimisation moves a system along a frontier; a rescue changes which frontier
it is on. Formally, $do(\phi:=\phi')$ leaves the graph of §2.5 unchanged and
leaves (2.8.1) true, for every $\phi'$ (equation 2.5.3). Adding $W$ changes the
graph, and it is the only intervention in this paper that does. The distinction is
not rhetorical: it predicts that an unbounded budget spent on evaluator quality
buys nothing at the bound, while a single cheap independent reading buys
$\Delta_{\mathrm{wit}}>0$ — and the two predictions are not the same prediction
with different constants.

There is a second, less obvious effect, and it is the one §3.3 measures. In the
two-regime model of Theorem 3$'$, the bankruptcy hazard decomposes as
$q_{i,0}=q^{\mathrm{end}}_{i}+\lambda\mathbf 1[T=0]$, where $\lambda$ is the rate
at which the world *happens* to notice a failure — an auditor, a customer, an
outage. Without a witness, $\lambda$ is exogenous: it is a property of the
environment's patience, not of the system, and no internal change alters it. With
a witness, the second term becomes $T$-measurable, and the system can act on it.
The difference is not a reduction in the probability of failure; it is a change in
*who owns the response*. A system whose failures are discovered only from outside
has no error-correcting dynamics, only a hazard rate, and by (2.9.5) its eventual
ruin is certain with expected time at most $1/\lambda$, and exactly $1/\lambda$
only if it has no internal route to noticing anything. A system that reads its own
failures has a policy.

This reframes the engineering question, and we prefer the reframed version. The
question is not "how accurate is our evaluator" but "what is
$I(W;T\mid O,V)$, and what does a unit of it cost". The first has no answer that
survives a distribution shift; the second is a measurable quantity, bounded above
by (4.2.1), and it is the only one of the two that appears in the decision.

## 4.3 The bound, and what it does not say

We are aware of the temptation to read a limit theorem as a verdict on an
industry, and we decline it. Three things are not claimed.

**Not that AI systems do not work.** (2.8.9) is a statement about a component,
conditional on a record. Where the record is rich, the record does the work: a
system whose observation determines the outcome needs no evaluator at all, and then
$\eta(\mathrm{cov}(o))$ is large and the bound does not bind — which is why we
write it as a bound rather than as an equality. The theorem does not say that
correct behaviour is impossible; it says that the *verdict's marginal contribution*
vanishes where the record is thin, which is a claim about a component and not about
a system.

**Not that the tail is unlearnable.** A2.2 is a statement about prior coverage, not
about a permanent incapacity. A prior that has seen the tail ceases to be
uninformative on it, and A2.2$'$ makes the slack quantitative precisely so that the
day it stops holding can be recognised. What the theory rules out is a system
that is simultaneously (i) dependent on its own verdict for correctness, and
(ii) operating where its prior has no coverage, and (iii) reliable. Pick two.

**Not that a witness suffices.** $\Delta_{\mathrm{wit}}>0$ is necessary for
escaping (2.8.1) and is not sufficient for reliability. A witness must be read
correctly, and the decision rule must use what it reads; the `r7` arm of §3.3 is a
demonstration that the channel can be built, not a proof that any channel will be
used well.

What remains after these retractions is narrower than the slogan, and easier to
defend. In a strong causal environment, on the part of the distribution where the
prior is thin, a system that certifies its own work has a reliability ceiling that
is a property of what it can see and not of how well it judges. The ceiling does
not move with the quality of the self-assessment, with objective design, or with
the scale of the evaluator: each of those acts inside the conditioning set and
changes nothing about what is in it.

It does move, in two ways, and denying that would be overstating the result. It
moves when coverage moves — a prior that has been trained on the tail is not
uninformative on the tail, and $\eta(\mathrm{cov}(o))$ is written in measurable
form precisely so that this can be recognised when it happens. And it moves when
the record thickens enough to determine the outcome, which is what §3.2 measured
when execution hashes entered $O$ and accuracy went from $0.60$ to $0.80$. Neither
move is an improvement of the evaluator; both change what the decision can see.

The third move is structural, and it is the one this paper is about: adding an
arrow to the graph. Between the three there is no fourth. Parameters of the
evaluator leave $O$, $\Pi$ and the graph unchanged, and therefore leave $\eta$
unchanged; that is the precise sense in which no budget spent on judgement buys
anything here, and it is a narrower claim than saying that scale never helps.

The organisational version of this is worse than the technical version. A system
that reports `PASS` without a witness does not merely fail; it destroys the
information that would have allowed the failure to be attributed. The ledger of
§3.3 recorded $8871.71$ against a delivery of $7676.93$: at the moment of
extinction the record said the work had been done, and the discrepancy was
recoverable only because a separate instrument had been measuring the same thing
all along. Remove that instrument and the failure becomes indistinguishable from
success at every point where a decision is made — by the system, and by whoever
reads its reports.

## 4.4 What would refute this

A theory of limits should name its falsifiers, and these are ours. We list only
falsifiers that a measurement could in fact produce. An earlier draft of this
section opened with "a counterexample to (D2.1)", and that was a mistake: (D2.1)
holds by measurability for any evaluator whose inputs are $(O,\Pi)$, so no
measurement can refute it, and a falsifier that cannot fail is not a falsifier. The
list below is correspondingly shorter and harder to satisfy.

**A measurement of $\eta(\mathrm{cov}(o))$ that stays bounded away from zero on
the tail.** This is the direct refutation of (A2.2$'$) and therefore of Theorem 2:
find a task family where the record occupied little of the prior's support, and
where a decision reading the verdict beats the best decision reading the record
alone by more than $\eta$. We would want the number, because it would tell us where
the ceiling is rather than whether one exists. A2.2$'$ was written in measurable
form precisely so that this could be tested rather than argued, and we would regard
such a measurement on a real task as more valuable than any further theorem in this
paper.

**A same-origin system that survives the tail.** If a system with no external
witness were shown to be reliable on strong-causal tasks in the low-coverage
regime, then (A2.2), the definition of `PASS`, or our account of coverage would have
to be wrong about it. We would want to know which, because any of those answers
would be more interesting than the theorem. Note what is *not* on this list: a
system whose evaluator reads the world directly — a controller with a force sensor
in the loop — is not a counterexample but a witness, and Proposition 2 says so:
it has the edge out of $T$ that the hypothesis excludes.

# 5. Conclusion

A system that grades its own homework is not measuring its homework. This is
usually said as a joke about institutions; we have tried to show that the precise
version of it is a statement about what a decision can see. When the evaluator and
the policy read one observation and share one prior, the verdict is a measurable
function of that pair, the conditional mutual information is zero, and no amount of
evaluator quality moves it — because the evaluator's parameters are not ancestors
of the truth. That identity is arithmetic, and we have stopped presenting it as the
paper's result: it holds by wiring, and it is not the kind of statement a
measurement can refute.

The result is the statement that survives dropping the prior from the conditioning
set: on the part of the distribution where the record does not cover the prior's
support, the verdict cannot lower the error of a decision that already sees the
record by more than $\eta(\mathrm{cov}(o))$, and there the amount is estimable. In
the instance we measured the extreme case was exact rather than asymptotic: a
constant evaluator, ten answers, one value, zero bits.

Three consequences follow and we have proved each in its own register. Along a
conjunctive chain, a per-step false-completion rate bounds the chance that at
least one failure goes undetected, and the familiar exponential rate is a
consequence of an independence assumption that fails in the direction that
matters. In the trust dynamics, a finite chain whose transitions do not read the
truth has no repair mechanism from inside; given an independent erosion assumption
— empirical, measurable, and stated as such — its healthy states are transient, so
failure is not corrected but merely outlived. And in both cases the intervention
that changes the bound is a channel to the world that is neither the report nor a
read-out of the prior.

We have not shown that current systems are worthless, and we would regard that
reading as a misuse of the result. We have shown something narrower and harder to
argue with: that in the environments where being wrong is expensive, the
reliability of a self-certifying system is capped by what it can see, that the cap
is computable, and that three things move it — coverage, a record rich enough to
determine the outcome, and an added arrow. The first two are not improvements of
the evaluator, and the third is not an optimisation of anything. The cap is not a
prediction about the next model. It is a statement about which measurements could
tell us anything, and it implies that most of the numbers now being reported cannot.
