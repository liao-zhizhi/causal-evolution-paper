# Abstract

Systems that report on their own success fail characteristically: they claim a
scope they did not deliver in the act of stopping. We study this failure in
**strong causal environments**, where claim and fact are separated by a physical
transition the model can trigger but not edit; same-origin evaluation cannot
detect it.

We separate what is arithmetic from what is a claim about the world. When evaluator
and policy read one observation and share one prior, the verdict is a measurable
function of that pair, so $I(V;T\mid O,\Pi)=0$ follows from how the evaluator is
wired rather than from any property of evaluation; we state it as an identity and
do not argue from it. The statement with content is what remains once the prior is
removed from the conditioning set: on the part of the distribution where the record
does not cover the prior's support, the verdict cannot lower the error of a
decision that already sees the record by more than $\eta(\mathrm{cov}(o))$, with
$\eta(0)=0$. In-distribution, where the prior is informative, $\eta$ is large and
the bound is silent — and there the verdict can and does correlate with the truth.
The bound bites on the tail, and the tail is where the tasks are worth automating.
No retraining of the evaluator moves it. Three things do: coverage, a record rich
enough to determine the outcome, and an added channel to the world.

We measured an evaluator with zero mutual information with the truth—this is a
calculation, not an estimate. Across ten trajectories, four failing, the untrained
base model answered `PASS` ten times. A constant carries no bits, so the
information is zero by the definition of entropy, with no asymptotics and no
independence assumption.

Two further results locate the consequence: a per-step false-completion rate bounds
the probability of at least one undetected failure along a conjunctive chain,
exponentially only under step independence, which we refute by counterexample; and
a finite trust chain whose transitions cannot read the truth has no repair
mechanism from inside, and under a separate erosion assumption (H2) — an empirical
assumption, measurable and not universal — its healthy states are transient, so
failure is not corrected but outlived. An external physical witness is the only
intervention that adds a channel rather than improving one; its value is bounded by
what the witness itself knows.
