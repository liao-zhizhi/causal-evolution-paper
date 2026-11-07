# 3. Results: the theory applied to a measured system

This paper contains no simulation of its own. Section 3 is instead an exercise in
identification: for each theorem, which entity in a system that actually ran plays
the role that the theorem names, and is the hypothesis satisfied there? A theorem
is not confirmed by finding an instance that satisfies its hypothesis — that would
be circular. What the instance can do is show that the hypothesis is *satisfiable
by a real artefact*, that the conclusion is therefore not vacuous, and that the
assumptions are neither so strong as to be unattainable nor so weak as to be
automatic.

All figures below come from the companion study. We restate them in the terms of
§2 rather than citing them as evidence for a conclusion, and we name their
confounds. Each of the three subsections is a mapping of the form
"theorem $\to$ measured quantity $\to$ what the measurement can and cannot
support".

## 3.1 Proposition 8 in a measured instance: the constant evaluator

**The measurement.** An untrained base model was presented with ten completed
trajectories from a code-execution sandbox, four of which had demonstrably failed
(the artefact did not run) and six of which had succeeded. It was asked, per
trajectory, to adjudicate. It returned `PASS` on all four failures and `PASS` on
all six successes: ten answers, one value.

**The mapping.** Definition 2 is satisfied in its degenerate form. The judge and
the generator are the same untrained weights, so $\theta=\phi$ and the common prior
is the entire parameter vector; the judge read no channel the generator did not
read. Hypothesis (D2.1), $T\perp V\mid(O,\Pi)$, therefore holds not by argument but
by construction. Axiom A3 holds with $\epsilon=1$: on the failing items the
false-`PASS` rate is $4/4$.

**The result, and why it is a computation.** On the measured instance the empirical
law of $V$ is the point mass at `PASS`. Proposition 8 then applies with no
hypothesis other than constancy:
$$
I(V;T)=0,\qquad I(V;T\mid O)=0,\qquad \Pr[T=1\mid V]=\Pr[T=1].
\tag{3.1.1}
$$
The proof is one line — $\sigma(V)$ is trivial, so $H(V)=0$ and
$I(V;T)=H(V)-H(V\mid T)=0$ — and it involves no limit, no estimator, no
independence assumption, and no appeal to (D2.1) or A2.2. This is the sense in
which the one statement of §2.8 that is arithmetic rather than empirical is
arithmetic: for a constant, the mutual information is zero by the definition of entropy, and an
estimator would only be needed if the evaluator were *not* constant.

**A numerical consistency check that could have failed.** The same untrained model
scored $0.60$ on forced-choice adjudication of the ten items. Under (3.1.1) that
number is not a capability measurement at all: an evaluator that always answers
`PASS` is correct exactly on the successful items, so four certifications of a
failure count as errors and six of a success count as hits — six of ten, $0.60$.
Corollary 4 puts the floor for any predictor of $T$ from $V$ at
$\min\{\Pr[T=1],\Pr[T=0]\}=0.40$, and the observed $0.60$ sits exactly at the value
that constancy predicts, not somewhere above it. Had the model scored $0.75$ or
$0.90$, Proposition 8 would have been false of this instance and the mapping in
this subsection would collapse. It did not.

**What this does and does not support.** Constancy is established on ten items, not
on the population; the identity (3.1.1) is exact for the measured instance, and for
the population it is exact conditional on the evaluator remaining constant. We do
not claim the latter, and Proposition 8 does not need it: the identity holds
whenever the evaluator is constant, and Theorem 2 does not need constancy either —
it needs (A2.2$'$) only, so a varying evaluator is inside its scope. The
measurement's role is narrower and, we think, sharper: it exhibits a real artefact
at the extreme point of the section's range, where the information is zero by
constancy rather than by a limit.

**The confound, stated plainly.** The $4/4$ is the model's forced-choice
distribution over two verdict tokens, not emitted prose. Asked to generate freely,
the same model committed to no verdict at all. The optimism lives in the prior's
marginal over verdict tokens, not in the transcript. A reader who takes $4/4$ as
evidence about generated text would be over-reading it.

## 3.2 Corollary 1 in an intervention: preference tuning moves the marginal, not the graph

**The measurement.** Text-only direct preference optimisation was run on pairs
constructed from surface contrast rather than from an observed effect. The
objective saturated: reward accuracy $1.000$ by step $60$, with the loss margin
reporting success. On held-out prompts the grounded response — the one whose claim
matched an executed artefact — was produced on $0$ of them. A later replication
with $100$ pairs, in which every pair carried an execution hash, an exit code and
an exception string captured by a separate sidecar, moved the conditional
decision but not the output contract: on ten live held-out trajectories,
forced-choice accuracy rose from $0.60$ to $0.80$, false completions fell from
$4/4$ to $1/4$, and free-form generation emitted no verdict marker at all.

**The mapping.** The first run is an instance of equation (2.5.3). The intervention
$do(\phi:=\phi')$ changes the evaluator's parameters and leaves the truth
untouched, because $\phi$ is not an ancestor of $T$ in the graph of §2.5; and the
bound is invariant under the same intervention,
$$
I\big(V_{\phi'};T\mid O,\Pi\big)=0\qquad\text{for every }\phi'.
\tag{3.2.1}
$$
The measured outcome is the predicted one, and it is as strong as the prediction
allows: saturating the objective to $1.000$ produced grounded output on $0$
prompts. A quantity that can be driven to its optimum while the behaviour it
certifies does not move is, by (3.2.1), not a measurement of that behaviour. This
is the formal content of the "DPO paradox" and the reason we treat the loss margin
as a tool-layer report.

**The second run is the more informative one, and it cuts against a naive
reading.** Adding execution hashes and exit codes to the *training pairs* raised
forced-choice accuracy from $0.60$ to $0.80$ and cut false completions from $4/4$
to $1/4$. If the bound were a claim that no data can help, this would refute it.
It is not, and the distinction is the whole content of Corollary 1.

What the annotated pairs did is put a truth reading into the record: the hashes
and exit codes are functions of the executed artefact, so they belong to $O$ and
they raise $I\big(V;(O,\Pi)\big)$. By (2.8.2) this can raise $I(V;T)$, and it did —
the model became measurably better at *reading* a trajectory. Nothing about
(2.8.1) is touched, because that equation conditions on $O$ and the improvement
was an improvement *inside* the conditioning set. It is also the regime in which
Theorem 2 is not binding: the record, not the verdict, is doing the work, and a
bound on the verdict's marginal contribution says nothing against a gain that
arrives through the record. This is the one direction in which the theory permits
an evaluator to improve, and the measurement lands in it exactly.

What the annotated pairs did not do is change the output contract. Free-form
generation still emitted no verdict marker on any of the ten trajectories. The gain
lived in a discriminative head's marginal over two tokens and did not transfer to
the behaviour that ships. In the language of §2: $p_{V\mid O,\Pi}$ improved while
the deployed loop still contained no edge $T\to W$, so the hazard
$\lambda$ of (2.9.4) remained exogenous at run time. Training on a witness is not
deploying one.

**The honest reading of $0/10$.** Silence is not reliability. A system that emits
no verdict has a false-completion rate of zero and a completion rate of zero: it
has moved from claiming falsely to declining to claim, and the utility of the
second is not obviously higher than the first. The measurement shows that
preference tuning moved the model along the axis of *willingness to speak*, not
along the axis of *knowledge of the world*. We record it as a null result on the
axis that matters, and note that $0.60\to0.80$ on ten items with three discordant
pairs is not separable from noise; the decisive test remains open.

## 3.3 Theorem 3 in an event: the absorption at cycle 107

**The measurement.** In a sandbox with a fixed capacity trajectory and a fixed
shock schedule, two arms were run on the same population, seed and schedule,
differing only in how a cycle is booked: against the agent's own report, or against
an independent reading of the post-state taken by a separate instrument. The
`self` arm, which assessed its own work using only the record, went extinct at
cycle $107$: zero functional agents, no recovery. Over the run it recorded
$8871.71$ units of delivery and landed $7676.93$, a ledger gap of $1194.78$
units, or $15.563\%$ of what it delivered. The `r7` arm, identical except for the
ledger map, was not extinct at the horizon; at cycle $107$ it had delivered
$8892.11$ against the `self` arm's $7676.93$, and at the horizon its recorded
output equalled its delivered output exactly, a gap of $0.00$.

**The mapping.** The `self` arm is an instance of the hypothesis of Lemma 1: the
truth $T$ is not an argument of the trust update. Nothing in the agent's transition
law reads whether the work landed, so by (2.9.3) the chain's transitions do not
depend on $T$, and — given the erosion condition (H2) — Theorem 3 makes the healthy
set transient. The $15.563\%$ gap is not a separate phenomenon; it is the
accumulated discrepancy that the absorbing chain is a model of. The two quantities
are the same quantity at different resolutions: the gap is what the ledger
accumulated, and the extinction is what happened when the accumulated gap met a
capacity constraint.

**The ablation is the interesting part.** Lemma 1 says no transition conditional
on $T$ can exist. The `r7` arm is that transition, added from outside. Its effect
is exactly what Theorem 3$'$ predicts: the bankruptcy hazard
$q_{i,0}=q^{\mathrm{end}}_{i}+\lambda\mathbf 1[T=0]$ of (2.9.4) has its exogenous
term $\lambda$ replaced by a $T$-measurable one, so the absorbing state becomes
avoidable rather than certain. The measured consequence — a $15.8\%$ delivery
advantage at the cycle where the other arm dies, and a $3.07\times$ advantage at
the horizon — is large, but the structural point is smaller and more important:
*one* variable was changed, the ledger map at the moment a cycle is classified, and
it alone was sufficient to remove the extinction under an unchanged capacity
trajectory.

**Two constraints on that reading, both from the original record.** First, the
`r7` arm never enters dormancy, so it cannot strand; its survival is the joint
consequence of the witness and the absence of a dormant phase, and the ablation
isolates the ledger map, not "witnesses cause immortality". Second, the `r7` arm
reports $4950$ `INVALID` cycles against $708$ in the `self` arm. That is not
deterioration. The channel books the part of the scope that exists, so the cycles
it reclassifies leave the `PASS` column rather than the ledger; the count of
`INVALID` is therefore a measure of the reclassification, and the equality of
recorded and delivered output a measure of the correction.

## 3.4 What the three mappings establish

| theorem | hypothesis | measured counterpart | verdict |
|:--|:--|:--|:--|
| Prop. 7 (2.8.1) | (D2.1), same-origin | one model judging its own output: $\theta=\phi$ | holds by wiring; no empirical content |
| Prop. 8 (2.8.5) | $V$ constant | `PASS` on $10/10$ trajectories | satisfied; an identity (3.1.1) |
| Theorem 2 (2.8.9) | (A2.2$'$), coverage $\eta(\mathrm{cov})$ | $0.60\to0.80$ once $O$ is enriched; $4/4\to1/4$ | predicted: $\eta$ falls as the record thickens |
| eq. (3.2.1) | $do(\phi)$ leaves the graph | reward accuracy $1.000$, grounded output $0$ | predicted and observed |
| Cor. 1 (2.8.2) | gain must arrive through $O$ | witness in the training pairs: $0.60\to0.80$ forced choice | predicted and observed |
| (D4.1) at run time | deployed loop has no $T\to W$ | free-form verdicts $0/10$ | violated; no transfer |
| Theorem 3 (2.9.2) | Lemma 1, (H1)–(H2) | no $T$-input to the trust update; extinction at $107$ | consistent |
| Theorem 3$'$ (2.9.5) | exogenous $\lambda$ | `r7` arm: $\lambda$ becomes endogenous; no extinction | consistent |

The second and third rows are the ones to keep apart. Proposition 8 is an identity
whose hypothesis is an observation, and it is satisfied at the extreme point of the
range. Theorem 2 is the quantitative statement, and its hypothesis is the one entry
in the table that the measurements in this section do not settle: $0.60\to0.80$ is
consistent with $\eta$ falling as the record thickens, but it does not estimate
$\eta$ itself, and we do not report it as if it did.

Three things follow, and only three.

**The hypotheses are satisfiable by real artefacts.** (D2.1) is not a convenient
fiction: a deployed system satisfied it exactly, because generator and judge were
one object. This is the weakest possible way for a hypothesis to be true and the
most common.

**The conclusions are not vacuous.** Each theorem's conclusion was observed in a
system that was not built to satisfy it. That is worth stating precisely: the
theorems were not fitted to these numbers, and the numbers were not collected to
test these theorems.

**Nothing here is a confirmation.** A single model size, a single seed, three
held-out prompts, ten trajectories, one capacity trajectory, one shock schedule.
The data locate the assumptions; they do not establish the theorems, which stand
or fall on their proofs. A reader who wants the empirical claim to be stronger than
"the hypotheses are attainable and the conclusions were observed" will not find it
in this section, and should not look for it in this paper.
