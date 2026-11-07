# 1. Introduction

There is a class of tasks where "did the model succeed?" has an answer
independent of the model's opinion, and where being wrong is costly. We call
these **strong causal environments**: claim and fact are separated by a physical
transition the model can trigger but cannot edit. Code either runs or
raises~\cite{jimenez2023swebench}; a braking distance is either shorter than the
obstacle or it is not. What matters
there is not fluency or likelihood, but whether the world moved and whether the
system noticed.

The failure we study is not hallucination in the ordinary sense. A model that
invents a citation is wrong about a text. A model that reports `PASS` on a build
that did not compile is wrong about the world, and the wrongness is invisible
from inside the loop that produced it. We call this a **false completion**: the
system claims a scope it did not deliver, in the same act by which it decides to
stop. Its danger is independent of capability, because it terminates the process
that could have found the error. A system that keeps failing is annoying; one
that declares success and halts is a liability, since no further evidence is
collected.

The empirical situation is worse than the vocabulary suggests. Before any
training, the base model behind a preference-tuning experiment was asked to
adjudicate four trajectories that had demonstrably failed; it returned `PASS` on
all four. On six succeeding trajectories it also returned `PASS`. Across ten
items the evaluator was not merely optimistic, it was **constant**. We do not
treat that as an anecdote: it identifies which hypothesis below is satisfied in
practice, and in §2.8 it collapses one asymptotic statement into an identity. A
constant carries exactly zero bits, so an evaluator that always says `PASS` has
mutual information zero with the truth — not approximately, not in the limit,
exactly.

## 1.1 Why the existing remedies do not reach the problem

**Text-only preference optimisation.** Direct preference
optimisation~\cite{rafailov2023dpo} reshapes a policy from pairs of preferred and
dispreferred outputs. When those pairs come
from the same prior being corrected — the normal case, since annotator, judge and
policy share a training distribution — the optimisation moves the *distribution
of the output* without changing the *relation between output and world*. Its
objective is a tool-layer report: a margin, a loss curve, accuracy on held-out
pairs. A report can be optimised to perfection while the behaviour it certifies
is untouched. Above, the objective saturated while the grounded response was
produced on zero prompts. §3.1 formalises this: an intervention on the
evaluator's parameters is not an intervention on the truth, so no setting of them
creates information the channel does not carry.

**Variance-based monitoring.** A second family watches dispersion of outputs,
confidence or rewards and flags instability. This cannot work, for an elementary
reason: variance is translation invariant, $\mathrm{Var}(X+c)=\mathrm{Var}(X)$.
A monitor measuring spread is blind by construction to a *constant* bias, and the
measured failure mode is exactly a constant. The worse the deception, the more
stable it looks. Dispersion measures inconsistency, not incorrectness — noise on
one side, a fixed offset that averaging never removes on the other.

Both families lack a channel to the world that is not the model's own report.
That lack is our object.

## 1.2 What we prove

**An identity, and then the theorem (Theorem 2).** Under same-origin evaluation —
evaluator and policy read the same observation and share a prior — the verdict is a
measurable function of $(O,\Pi)$, so $I(V;T\mid O,\Pi)=0$. We state that as
Proposition 7 and do not call it a result: for an evaluator wired this way it is
automatic, and it is not the kind of statement a measurement can refute. The result
of the section is Theorem 2, which drops the prior from the conditioning set. Under
a coverage condition on the prior — (A2.2$'$), an empirical assumption we label as
such — the error of any decision that reads the verdict is within
$\eta(\mathrm{cov}(o))$ of the error of a decision that reads only the record.
Inside the prior's coverage $\eta$ is large and the bound says nothing; on the tail
$\eta\to0$ and the verdict's contribution vanishes. The bound is therefore about a
channel where the channel matters, which is narrower than "the verdict carries no
information" and is the only version we can defend.

**An accumulation law (Theorem 1).** If each step produces a false completion
with probability at least $\epsilon$, the probability of at least one undetected
false completion over an $n$-step chain is at least $1-(1-\epsilon)^n$ — under
step independence. We also prove the independence-free bound, and give the
counterexample showing the exponential rate is unavailable without it; this is
the weakest of the three, and we say so in the text.

**An absorption theorem (Theorem 3).** Model trust in the system's own verdicts
as a finite Markov chain with a bankruptcy state. If transitions do not take the
truth as an input, no repair conditional on failure can exist; under a separate
erosion assumption (H2), healthy states are then transient and absorption is almost
sure. Neither half is proved here from first principles, and we say which is which:
the chain algebra is textbook, the erosion condition is an empirical assumption, and
the lemma in between is the one that says why the truth cannot be an input — the
same-origin assumption again.

Together they give one conclusion with a precise scope: an external physical
witness — a channel to the world that is neither the model's report nor a
read-out of its prior — is the only operation that *adds* a channel to the decision.
We formalise it (Definition 4), give it a value (Corollary 3), and show that value
belongs to the witness alone, so improving the evaluator cannot substitute for
acquiring one.

## 1.3 What we do not claim

We do not claim reliability is impossible. We claim it is bounded, and identify
the bound and its escape. A witness is necessary for escaping it, not sufficient
for reliability.

Two things do move the bound, and naming them costs us the slogan that nothing
does. **Coverage** moves it: (A2.2) is a statement about which part of the
distribution the record occupies, so a prior that has been trained on the tail is
not uninformative on the tail, and $\eta(\mathrm{cov}(o))$ is written in the form
it is written so that this can be measured rather than argued. **A record that
determines the outcome** moves it too, and §3.2 measures the move: adding execution
hashes and exit codes to the record raised forced-choice accuracy from $0.60$ to
$0.80$, because a truth reading had entered $O$. What does *not* move the bound is
the evaluator. No retraining of $\phi$ changes $I(V;T\mid O,\Pi)$, and none changes
$\eta$; scaling the evaluator acts inside the conditioning set. So the correct
statement is narrower than "scale cannot help": scale helps exactly to the extent
that it changes coverage or enriches the record, and the experiments that would
separate those from a genuine improvement of judgement are not in this paper.

And we present no benchmark: every number here appears once, in §3, to identify
which hypothesis the measured system satisfies.

A note on the title. *Inevitable* is used throughout in its measure-theoretic
sense — almost sure, with respect to the measure named in the theorem — and the
extent is always written. Where a statement is a positive probability rather than
a probability of one, it appears as $\epsilon$ or as a bound, never as rhetoric.
The word carries no weight that the equations do not carry.
