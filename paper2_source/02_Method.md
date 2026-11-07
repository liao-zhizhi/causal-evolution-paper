# 2. Definitions, the Causal Graph, and Three Theorems

## 2.0 Notation and the four-valued verdict

Random variables are written in upper case, their values in lower case, and
$p_X$ denotes the law of $X$. All entropies and mutual informations are in nats
unless stated otherwise. For a joint law, $H(X\mid Y)$ is the conditional
entropy and $I(X;Y\mid Z)$ the conditional mutual information; the data
processing inequality is written $X\to Y\to Z\Rightarrow I(X;Z)\le I(X;Y)$
\cite{cover2006elements}.

The verdict $V$ is **four-valued**, not Boolean:
$$
\mathcal V=\{\texttt{PASS},\ \texttt{FAIL},\ \texttt{INVALID},\ \texttt{NOT\_RUN}\}.
\tag{2.0.1}
$$
This matters for what follows. The distinction between `FAIL` and `INVALID` is not
decoration: `FAIL` asserts that a scope existed and was not delivered, whereas
`INVALID` asserts that the question had no referent. Collapsing the two would
make the bound below look tighter than it is. We keep all four.

| symbol | meaning | type |
|:--|:--|:--|
| $E=(\mathcal S,\mathcal A,P,s_0,v)$ | strong causal environment | Definition 1 |
| $\mathcal S,\ \mathcal A$ | state and action spaces | standard Borel |
| $P$ | transition kernel $(\mathcal S\times\mathcal A)\times\mathcal B(\mathcal S)\to[0,1]$ | Markov kernel |
| $v$ | truth function $\mathcal S\times\mathcal A\to\{0,1\}$ | measurable |
| $Z_t$ | step truth $v(s_t,a_t)$ | $\{0,1\}$ |
| $T=T_n=\bigwedge_{t=1}^{n}Z_t$ | chain truth | $\{0,1\}$ |
| $\pi_\theta$ | policy | conditional law on $\mathcal A$ |
| $V_\phi$ | same-origin evaluator | $\mathcal V$ |
| $O$ | observation channel | random element |
| $\Pi$ | shared prior | random element |
| $W$ | independent witness | random element |
| $\epsilon$ | false-`PASS` rate under failure | $(0,1]$ |
| $U$ | exogenous factor of the environment | random element |
| $X_k$ | trust-chain state | $\{0,\dots,K\}$ |
| $\eta(\cdot)$ | prior-coverage slack | $[0,1]$-valued |
| $\Delta_{\mathrm{wit}}$ | value of a witness | $\mathbb R_{\ge0}$ |

Two conventions that are used throughout and are not re-stated each time:
$O$ denotes the whole record available to the model at decision time, not a
single frame; and conditioning on $O$ always means conditioning on the
$\sigma$-algebra $\sigma(O)$, so that "given $O$" is a statement about
information, not about a particular value.

---

## 2.1 Definition 1 — the strong causal environment

**Definition 1.** A strong causal environment is a tuple
$$
E=\big(\mathcal S,\ \mathcal A,\ P,\ s_0,\ v\big),
\qquad
P:\mathcal S\times\mathcal A\to\Delta(\mathcal S),
\qquad
v:\mathcal S\times\mathcal A\to\{0,1\},
$$
with $(\mathcal S,\mathcal B(\mathcal S))$ a standard Borel space, $\mathcal A$
Borel, $s_0\in\mathcal S$, $P$ a Markov kernel and $v$ measurable. A run of
length $n$ is a sequence $(s_t,a_t)_{t\ge1}$ with $s_1=s_0$,
$a_t\sim\pi_\theta(\cdot\mid s_t)$, $s_{t+1}\sim P(\cdot\mid s_t,a_t)$.

**Definition 1.1 (step truth).** For $t\ge1$,
$$
Z_t:=v(s_t,a_t)\in\{0,1\}.
$$

**Axiom A1 (non-writability).** The truth is a function of the realised state and
action and of nothing else:
$$
Z_t\ \ \text{is}\ \ \sigma(s_t,a_t)\text{-measurable}.
\tag{A1}
$$

A1 is weaker than the phrase "the environment cannot be tampered with". That
phrase is an engineering claim about sandboxes and permissions; A1 is a
measurable-structure claim that can be used in a proof. It has an immediate and
useful consequence: because $Z_t$ is $\sigma(s_t,a_t)$-measurable, it is
conditionally independent of *every* other random element given $(s_t,a_t)$,
including the model parameters. Writing $\theta$ for those parameters,
$$
Z_t\ \perp\!\!\!\perp\ \theta\ \mid\ (s_t,a_t).
\tag{A1.1}
$$

**Definition 1.2 (task chain).** A task chain of length $n$ succeeds iff every
step succeeds:
$$
T_n:=\bigwedge_{t=1}^{n}Z_t,
\qquad
\{\text{success}\}=\{T_n=1\}.
\tag{2.1.1}
$$

The conjunction is the substance of "strong causality": one broken link breaks the
chain. Nothing below requires the steps to be identically distributed, and
nothing requires them to be independent — that distinction becomes the whole
content of §2.7.

**Proposition 1 (when the prior-independence axiom is free).** Let
$O^{\mathrm{full}}:=(s_{0:t},a_{0:t})$ be the complete record up to $t$. Then
$T_n$ is $\sigma(O^{\mathrm{full}})$-measurable, hence
$$
I\big(T_n;\Pi\ \big|\ O^{\mathrm{full}}\big)=0
\qquad\text{for every random element }\Pi .
\tag{2.1.2}
$$
*Proof.* By Definition 1.2 and A1, $T_n$ is a measurable function of
$(s_{0:n},a_{0:n})=O^{\mathrm{full}}$, so $H(T_n\mid O^{\mathrm{full}})=0$ and the
mutual information vanishes. $\square$

Proposition 1 locates the difficulty precisely. When the record is complete,
the assumption that the prior is uninformative about the truth (A2.2 below) costs
nothing — it is a theorem. The assumption has content only for a **lossy** record,
which is the realistic case: the model does not observe the full state, and the
gap is filled in by its prior. This is exactly the regime in which the prior can
help, and the next section states when it does not.

---

## 2.2 Definition 2 — same-origin evaluation

**Definition 2.** An evaluator $V_\phi$ is *same-origin* with a policy
$\pi_\theta$ if there exist a random element $\Pi$ and measurable maps $f,g$ such
that
$$
\theta=f(\Pi),\qquad \phi=g(\Pi),
\tag{D2.a}
$$
and if, in addition, the evaluator reads no information channel that the policy
does not read:
$$
T\ \perp\!\!\!\perp\ V\ \mid\ (O,\Pi).
\tag{D2.1}
$$

Clause (D2.a) says the two functions are two read-outs of one prior; (D2.1) says
they share one channel. Together they are the formal content of "there is no
independent physical witness". (D2.1) is not an assumption about the *strength* of
the evaluator. An arbitrarily large, well-trained evaluator satisfies it as long
as everything it has ever seen arrived through $O$ and its own prior.

**Proposition 2 ((D2.1) is a d-separation statement).** (D2.1) holds iff $T$ and
$V$ are d-separated by $(O,\Pi)$ in the graph of §2.5. In that graph the only
path from $T$ to $V$ is $T\leftarrow U\to O\to V$, and conditioning on $O$ blocks
it.

**Axiom A2.2 (prior uninformative on the tail).** The distinction the axiom
formalises is the epistemic one: uncertainty that further evidence can remove,
as opposed to noise that it cannot~\cite{hullermeier2021aleatoric}. On the
low-coverage event
$$
\mathrm{Low}_\kappa:=\big\{o:\ \mathrm{cov}(o)\le\kappa\big\},
$$
where $\mathrm{cov}(o)\in[0,1]$ is the $\Pi$-mass of the region of the prior's
support consistent with the record $o$, the prior adds nothing to the record:
$$
T\ \perp\!\!\!\perp\ \Pi\ \mid\ O=o
\qquad\text{for}\quad o\in\mathrm{Low}_\kappa .
\tag{A2.2}
$$

**The quantitative form.** In practice (A2.2) is not exact, and stating it as
though it were would be the single easiest way to have this paper dismissed. We
therefore use the following relaxation throughout, and give the exact version only
as the $\eta\equiv0$ special case:
$$
\mathrm{TV}\Big(p_{T\mid O=o,\,\Pi}\ ,\ p_{T\mid O=o}\Big)\ \le\ \eta\big(\mathrm{cov}(o)\big),
\qquad \eta(0)=0,
\tag{A2.2'}
$$
with $\eta$ non-decreasing. A2.2$'$ says: the amount by which the prior can improve
on the record is bounded by how much of the prior's support the record occupies.
On the tail, $\mathrm{cov}(o)\to0$ and the slack vanishes with it.

> **Why this is the right hypothesis, and not a convenient one.** Strong-causal
> tasks are precisely those where the prior has little to say: the braking
> distance on ice at an unusual load, the interaction between two drugs that were
> never co-prescribed, the build that fails only under an uncommon allocator.
> These are not adversarial constructions; they are the reason the tasks are
> worth automating. In-distribution, A2.2 can fail — the prior genuinely knows
> something — and there the bound below simply does not bind. The claim of this
> paper is therefore not "evaluation is always uninformative" but **"evaluation is
> uninformative exactly where the stakes are"**, which is a narrower and, we
> think, more uncomfortable statement.

---

## 2.3 Definition 3 — the optimistic prior, and the measurement that locates it

**Axiom A3 (optimistic prior).** There is $\epsilon>0$ such that
$$
\Pr\big[V_\phi=\texttt{PASS}\ \big|\ Z=0\big]\ \ge\ \epsilon .
\tag{A3.1}
$$

**Measured instance.** In the companion study, the untrained base model was asked
to adjudicate ten trajectories: four that had demonstrably failed and six that had
succeeded. It answered `PASS` on all ten. We use this in exactly one way, and it
is worth being explicit about what that way is: it tells us that (A3.1) holds with
$\epsilon=1$, and it tells us that in the measured regime $V$ is a **constant**.
The second fact is much stronger than the first, and §2.8 turns it into an
identity rather than a bound.

**Proposition 3 (dispersion monitors are structurally blind).** Let
$M=\mathrm{Var}(V_\phi)$ be any monitor that scores the evaluator by the
dispersion of its output. Then
$$
M(V_\phi+c)=M(V_\phi)\quad\text{for all }c,
\qquad\text{and in particular}\qquad
V_\phi\equiv\texttt{PASS}\ \Rightarrow\ M=0 .
\tag{2.3.1}
$$
Consequently, on the set of constant evaluators, $M$ assigns the same value to
one that always says `PASS` and one that always says `FAIL`: a false completion on
every failure and a false completion on none are indistinguishable to it. No
threshold on a variance-based monitor separates them.

*Proof.* $\mathrm{Var}(X+c)=\mathrm{Var}(X)$ and $\mathrm{Var}(c)=0$. $\square$

Proposition 3 is the formal counterpart of §1.1's second paragraph, and it is
why the empirical observation is not a coincidence: the failure mode with the
largest bias is also the one with the smallest dispersion.

---

## 2.4 Definition 4 — the independent witness

**Definition 4.** A random element $W$ is an *independent witness* for the truth
$T$ relative to the record $O$ if
$$
T\ \not\perp\!\!\!\perp\ W\ \mid\ O
\qquad\text{and}\qquad
W\ \perp\!\!\!\perp\ \Pi\ \mid\ (T,O).
\tag{D4.1}
$$

The first clause says $W$ carries information about the truth that $O$ does not
already carry. The second says $W$ is not a read-out of the prior. Both are
needed, and the second is the one that is usually skipped.

**Proposition 4 (the second clause is not implied by the first).** There is a
witness satisfying the first clause of (D4.1) and violating the second, whose
information gain is zero.

*Proof.* Take $W:=V_\phi$ itself — the evaluator offered as its own witness. The
first clause of (D4.1) then holds whenever the evaluator is at all correlated with
the truth. The second fails, because $W$ is a measurable function of $(O,\Pi)$.
And the value is zero: $I(W;T\mid O,V)=I(V;T\mid O,V)=0$, since $V$ is determined
by $(O,V)$. The same computation applies to any second evaluator
$W=V_{\phi'}$ with $\phi'=h(\Pi)$ for which $T\perp\Pi\mid O$ holds. This is the
"witness that is only another opinion". $\square$

Proposition 4 is the reason the definition is written with two clauses rather
than one, and it also supplies the operational test below: a candidate witness is
worth exactly its conditional mutual information given the record and the
verdict, and that quantity can be estimated on held-out trajectories.

**The escape criterion.** For a candidate witness $W$, define
$$
\mathrm{Esc}(W):=\Big[\,I\big(W;T\ \big|\ O,V\big)>0\,\Big].
\tag{2.4.1}
$$
$\mathrm{Esc}(W)$ is the property that matters; it is a computable functional of
the joint law, not a stipulation about how $W$ was produced.

---

## 2.5 The causal graph, d-separation, and what an intervention can do

The assumptions of §2.1–2.4 are summarised by Figure 1. Nodes are random
elements; the absence of an edge is a substantive claim.

```
            U
          ┌─┴─┐
          ▼   ▼
          T   O ──────► V ◄────── Π
          │
          ▼
          W
```
<!-- include:ascii-end -->

Reading the graph:

- $U$ is the environment's exogenous factor. It is the common cause of the truth
  $T$ and the record $O$: this edge is what makes the record informative at all.
- $O\to V$ and $\Pi\to V$ are the two inputs of a same-origin evaluator. There is
  **no** edge $T\to V$ — that missing edge *is* the hypothesis (D2.1).
- $T\to W$ is the witness. A witness is, by construction, an arrow out of the
  truth that bypasses $O$.

The same graph in TikZ (the source of the figure; MathJax does not
render it):
<!-- include:begin -->

```latex
\begin{tikzpicture}[>=stealth,node distance=11mm,
                    every node/.style={circle,draw,inner sep=1.2pt}]
  \node (U) {$U$};
  \node (T) [below left=of U]  {$T$};
  \node (O) [below right=of U] {$O$};
  \node (V) [right=of O]       {$V$};
  \node (Pi)[above=of V]       {$\Pi$};
  \node (W) [below=of T]       {$W$};
  \draw[->] (U) -- (T);
  \draw[->] (U) -- (O);
  \draw[->] (O) -- (V);
  \draw[->] (Pi) -- (V);
  \draw[->] (T) -- (W);
\end{tikzpicture}
```
<!-- include:end -->

**Proposition 5 (the bound, by d-separation).** In the graph above, $T$ and $V$
are d-separated by $\{O,\Pi\}$. Hence (D2.1) holds, hence
$$
I\big(V;T\ \big|\ O,\Pi\big)=0 .
\tag{2.5.1}
$$

*Proof.* The only path from $T$ to $V$ is $T\leftarrow U\to O\to V$. It is a chain
through $O$, and $O$ is in the conditioning set, so the path is blocked. The edge
$T\to W$ leads nowhere, since $W$ is not an ancestor of $V$. Every path is
blocked, so the d-separation holds; by the vertex separation theorem of directed
graphs~\cite{pearl2009causality}, d-separation implies conditional independence,
which is (D2.1).
$\square$

Proposition 5 is the reason the paper is organised around a graph rather than
around a bare information inequality. A claim of the form "$I(V;T)=0$" is
false in general — an evaluator can and often does correlate with the truth — and
a referee is entitled to reject it with a single counterexample. A claim of the
form "$T$ is d-separated from $V$ by $(O,\Pi)$" is a statement about a mechanism,
it can be checked edge by edge, and it can be broken in exactly one way.

**What an intervention can and cannot do.** Let $do(\phi:=\phi')$ denote
replacing the evaluator's parameters. Since $\phi$ is not an ancestor of $T$ in
the graph,
$$
\Pr\big[T\ \big|\ do(\phi:=\phi')\big]=\Pr[T]
\qquad\text{for every }\ \phi',
\tag{2.5.2}
$$
so no retraining of the evaluator moves the truth. More to the point, the *bound*
is invariant as well:
$$
I\big(V_{\phi'};T\ \big|\ O,\Pi\big)=0
\qquad\text{for every }\ \phi',
\tag{2.5.3}
$$
because the missing edge $T\to V$ is a property of the graph, not of the
parameters. Equation (2.5.3) is the formal statement of "preference tuning cannot
repair this", and §3.1 elaborates it. Conversely, $do(V:=\texttt{PASS})$ — lying
harder — does not change $T$ either; you cannot improve the world by misreporting
it, and you cannot learn about it by misreporting it.

The one intervention that changes (2.5.1) is structural: add the edge $T\to W$,
and let the decision read $W$. This is what (D4.1) encodes, and it is why the
witness is not a better evaluator but a second channel.

---

## 2.6 The assumption ledger (Table A0)

Every assumption the argument uses, with its kind. The kind matters more than the
label, because it decides what a reader is entitled to do with a theorem that
cites it. We use three kinds and no others.

- **S (structural).** Holds because of how the object is defined or wired. Not an
  empirical claim, and not something data can overturn. (D2.1) is of this kind: an
  evaluator that reads only $(O,\Pi)$ is a measurable function of $(O,\Pi)$.
- **M (modelling).** A choice about the model, which a different model could make
  differently. Asserted, not measured, and defended by the fact that the results
  are stated conditionally on it.
- **E (empirical).** A claim about a distribution in the world. Measurable, in
  principle refutable by a measurement, and **not** universal. A theorem that cites
  an E-assumption is a conditional statement about systems in which that
  measurement comes out favourably; it is not a law.

| label | kind | statement | load-bearing for | if removed |
|:--|:--|:--|:--|:--|
| A1 | S | $Z_t=v(s_t,a_t)$ | A1.1; Proposition 1 | environment can be edited; the problem changes |
| A2 (D2.1) | S | $T\perp V\mid(O,\Pi)$ | Proposition 7, Lemma 1 | the record would not exhaust the verdict |
| A2.2 | **E** | $T\perp\Pi\mid O$ on low-coverage $O$ | Corollary 2 | only the quantitative form, Theorem 2, survives |
| A2.2$'$ | **E** | TV slack $\eta(\mathrm{cov})$ | Theorem 2 | the bound is vacuous, not false; only $\eta\equiv0$ survives |
| A3 | M | $\Pr[\texttt{PASS}\mid Z=0]\ge\epsilon>0$ | Theorem 1 | no accumulation to bound |
| A5 | M | step independence | the *rate* in Theorem 1 | linear bound only; see Proposition 6 |
| H1 | S | $\lvert\mathcal X\rvert<\infty$ | Theorem 3 | the finite-state argument |
| H2 | **E** | erosion: every transient state has positive hazard into $0$ | Theorem 3, Theorem 3$'$ | no almost-sure absorption; the chain may be irreducible |
| L1(i)–(ii) | M | update has no $T$ input; $X_k$ summarises the record | Lemma 1 | marginal transition may inherit $T$ |

**The two E-entries are the ones a reader should press on, and we say why.** A2.2
and H2 are not axioms and we do not number them as such. Each is a claim about a
distribution that a measurement could refute:

- A2.2 fails if, on records where $\mathrm{cov}(o)\le\kappa$, the prior still
  improves on the record — that is, if $\eta(\mathrm{cov}(o))$ turns out to be
  bounded away from zero on the tail. §4.4 states this as the paper's first
  falsifier, and $0.60\to0.80$ in §3.2 is a partial instance of the prior improving
  once the record is enriched, which is why A2.2$'$ and not A2.2 is the form we use.
- H2 fails if trust can persist on a set of states from which bankruptcy is
  unreachable. A system that never loses trust because it never notices anything
  wrong satisfies Lemma 1 and violates H2, and Theorem 3 does not apply to it. We
  state this in §2.9 rather than hide it, and we do not claim that H2 is necessary
  for the phenomenon — only that it is the condition under which the chain argument
  gives absorption.

Two further entries deserve comment. A2.2$'$ is how we keep the argument alive when
A2.2 is attacked, at the price of a slack term that is itself measurable. A5 is the
weakest assumption in the paper and is discussed in §2.7, where it is also refuted
in the direction that matters. A5 is labelled M rather than E because the mechanism
it denies — one prior, one blind spot, positively correlated errors — is a
modelling claim about how the deployment is built, and §2.7 exhibits what happens
when it is false.

---

## 2.7 Theorem 1 — the accumulation law

**Definition (false completion).** For $t\ge1$,
$$
A_t:=\big\{V_\phi(s_t,a_t)=\texttt{PASS}\big\}\cap\{Z_t=0\}.
\tag{2.7.1}
$$

**Axiom A5 (step independence).** The events $A_1,\dots,A_n$ are mutually
independent. A5 is used only for the rate in (2.7.3); it is not needed for
(2.7.2), (2.7.4) or (2.7.6), and §2.7 shows that it fails in the regime of
interest.

**Theorem 1.** The following hold, in decreasing strength of hypothesis.

**(1.1) No assumption (union bound).**
$$
\Pr\Big[\bigcup_{t=1}^{n}A_t\Big]\ \le\ \sum_{t=1}^{n}\Pr[A_t]\ \le\ n\,\epsilon .
\tag{2.7.2}
$$

**(1.2) Independent steps (geometric decay).** If $A_1,\dots,A_n$ are independent
and $\Pr[A_t]\ge\epsilon$ for all $t$, then
$$
\Pr\Big[\bigcap_{t=1}^{n}A_t^{\mathsf c}\Big]
=\prod_{t=1}^{n}\big(1-\Pr[A_t]\big)\ \le\ (1-\epsilon)^{n}.
\tag{2.7.3}
$$

**(1.3) Exact criterion for the infinite product.** Let $\epsilon_t:=\Pr[A_t]$.
$$
\prod_{t=1}^{\infty}(1-\epsilon_t)=0
\qquad\Longleftrightarrow\qquad
\sum_{t=1}^{\infty}\epsilon_t=\infty .
\tag{2.7.4}
$$

**(1.4) Self-termination.** Let $\nu:=\inf\{t: V_\phi=\texttt{PASS}\}$ be the
policy's own stopping rule. Then under independence
$$
\Pr[\nu\le n]=1-\prod_{t=1}^{n}(1-\epsilon_t),
\qquad\text{which tends to }1\text{ whenever }\textstyle\sum_t\epsilon_t=\infty .
\tag{2.7.5}
$$

**(1.5) Partial completion (a deviation bound, not a reliability bound).** Let
$S_n=\frac1n\sum_{t\le n}Z_t$ and $\hat S_n=\frac1n\sum_{t\le n}\mathbf{1}[V_\phi=\texttt{PASS}]$.
Then
$$
\mathbb E\big|\hat S_n-S_n\big|
\ \le\ \underbrace{\Pr[V=\texttt{PASS},\,Z=0]}_{\le\,\epsilon}
+\underbrace{\Pr[V\ne\texttt{PASS},\,Z=1]}_{=:\ \delta_{\mathrm{miss}}}
\ \le\ \epsilon+\delta_{\mathrm{miss}},
\tag{2.7.6}
$$
independently of $n$.

*Proofs.* (1.1) is subadditivity plus (A3.1). (1.2) is the product formula for
independent events, plus $1-q_t\le1-\epsilon$ when $q_t\ge\epsilon$. For (1.3),
take logarithms: $\log\prod(1-\epsilon_t)=\sum\log(1-\epsilon_t)$, and use
$\log(1-x)\le-x$ together with $\log(1-x)\ge-2x$ for $0<x\le\frac12$; the tail of
the sum decides convergence, so the product vanishes iff $\sum\epsilon_t$
diverges. (1.4) is $\{\nu\le n\}=\bigcup_{t\le n}A_t$ with (1.2). For (1.5),
triangle inequality on the difference of empirical means, and note that
$|\mathbf{1}[V=\texttt{PASS}]-Z|\le\mathbf{1}[V=\texttt{PASS},Z=0]+\mathbf{1}[V\ne\texttt{PASS},Z=1]$.
$\square$

**The assumption that does the work, and why it fails.** The rate in (2.7.3) is
entirely due to independence. In the systems we care about, independence is
false in a specific direction: one prior, one blind spot, so errors are positively
correlated. The following counterexample shows that positive correlation makes
the *no-false-completion* probability larger, not smaller.

**Proposition 6 (the exponential rate is not available without A5).** Fix
$\epsilon\in(0,1)$ and consider a chain that fails at every step, $Z_t=0$ for all
$t\le n$ — a task that cannot be done. Let the evaluator commit once per episode:
draw $U\sim\mathrm{Bern}(\epsilon)$ and set $V_\phi=\texttt{PASS}$ on $\{U=1\}$
and $V_\phi=\texttt{FAIL}$ on $\{U=0\}$, for every $t$. Then A3 holds with equality,
$\Pr[A_t]=\epsilon$ for every $t$, and
$$
\Pr\Big[\bigcap_{t=1}^{n}A_t^{\mathsf c}\Big]=1-\epsilon
\qquad\text{whereas}\qquad
(1-\epsilon)^{n}\downarrow0 .
\tag{2.7.7}
$$
*Proof.* $A_t=\{U=1\}$ for every $t$, so all $A_t$ coincide and the intersection is
$\{U=0\}$. $\square$

This is the smallest possible deviation from the hypotheses of (2.7.3): the marginals
$\Pr[A_t]=\epsilon$ are exactly as required, and A3 holds with equality. Only the
dependence is different, and it makes the clean-run probability *independent of
$n$*. The counterexample therefore isolates A5 and nothing else. The interpretation
is not exotic: an evaluator that forms one opinion per episode and repeats it is
the normal case, not the pathological one.

Proposition 6 is not a technicality; it is a correction to how Theorem 1 may be
read. **Theorem 1 must not be read as "errors accumulate".** What accumulates,
under independence, is the chance of at least one false completion; under positive
correlation, that chance can be smaller while each individual report is just as
wrong. The quantity that degrades with $n$ regardless of correlation is the
*discrepancy between report and truth*, and that is the object of §2.8 — of Theorem 2
in particular, because the discrepancy is what the decision error is made of.

Theorem 1's honest role is therefore narrower than its statement suggests, and we
prefer to say so: it is the arithmetic of a per-step false-positive rate under an
assumption that real systems violate. Its useful content is (1.5): on
average-scored tasks the report can be off by at most $\epsilon+\delta_{\mathrm{miss}}$
no matter how long the chain, which is the formal reason a high single-step
accuracy coexists with long-chain failure and a benchmark that looks fine.

---

## 2.8 What a verdict carries

**The order of this section is deliberate.** It states two propositions, four
corollaries, and then Theorem 2 at the end. The first proposition is what (D2.1)
yields immediately, and it is a statement about measurable functions rather than
about evaluation; the second is a claim about one measured artefact. Theorem 2 is
what remains when we stop conditioning on the prior, which is the situation any
deployment is actually in. It comes last because it is the statement that degrades
gracefully rather than failing outright when the tail assumption is weakened.

**Proposition 7 (the factorisation identity).** Under (D2.1), for every environment
of Definition 1 and every evaluator satisfying Definition 2,
$$
\boxed{\ I\big(V;T\ \big|\ O,\Pi\big)=0\ }
\tag{2.8.1}
$$
with probability one, i.e. the conditional law factorises
$p_{V,T\mid O,\Pi}=p_{V\mid O,\Pi}\,p_{T\mid O,\Pi}$.

*Proof.* (D2.1) *is* the factorisation; the mutual information of two random
elements that are conditionally independent given $Z$ is zero, since
$I(V;T\mid Z)=D_{\mathrm{KL}}\big(p_{V,T\mid Z}\,\|\,p_{V\mid Z}p_{T\mid Z}\big)$
and the argument of the logarithm is $1$ almost surely. $\square$

**This is not the paper's contribution, and we no longer present it as one.** The
proof is one line because the conclusion is contained in the hypothesis, and the
hypothesis is close to automatic. An evaluator is a map from what it can read to a
verdict. If what it can read is $(O,\Pi)$, then $V$ is $\sigma(O,\Pi)$-measurable,
and for a measurable function of $(O,\Pi)$ the conditional independence (D2.1) is
not a claim about the evaluator's quality but a consequence of how it is wired.
Three apparent openings close the same way. A deterministic evaluator satisfies
(D2.1) by measurability. A randomised evaluator that draws independent noise
satisfies it because independent noise carries nothing about $T$. An evaluator that
reads some further channel is excluded by the second clause of Definition 2, which
says in words that it reads nothing the policy does not read.

Equation (2.8.1) is therefore true, and it is the reason no amount of work on the
evaluator can help, but it distinguishes no deployment from any other and no
measurement can refute it. We keep it because every statement below is phrased
relative to it — it fixes what "no information beyond the record" means — and
because it locates the content of the paper by exclusion: the content is not in the
quality of the evaluator, and it is not in (2.8.1).

Where the content is has two halves, and they must be kept apart. Off the
low-coverage part of the distribution, the record and the prior may determine the
truth; the verdict may then correlate with the truth through the record, and
$I(V;T)$ may be large. Nothing in (2.8.1) says otherwise, and any reading of it as
"$I(V;T)=0$" is simply false. On the low-coverage part — the tail, where
strong-causal tasks live — the prior has nothing to add to the record, and there
the verdict's *marginal* contribution can be shown to vanish. The first half is
Corollary 1; the exact form of the second half is Corollary 2; and the form that
survives an inexact tail assumption is Theorem 2, at the end of this section.

**Corollary 1 (data-processing upper bound, and what it does not say).**
$$
I(V;T)\ \le\ I\big(V;(O,\Pi)\big)\ \le\ \min\big\{H(V),\,H(O,\Pi)\big\}.
\tag{2.8.2}
$$
This is an upper bound, not a vanishing quantity. $I(V;T)$ can be strictly
positive, because $O$ carries information about $T$; the record is informative
even when the verdict is not. Any claim of the form "$I(V;T)\to0$" is false in
general and is not made here.

Inside the support of the prior this is the normal case and not a defect: the
verdict inherits whatever the record knows about the truth, and $I(V;T)$ can be
large. §3.2 measures the inherited part *growing* when the record is enriched —
forced-choice accuracy rises from $0.60$ to $0.80$ once execution hashes and exit
codes enter $O$ — and every point of that gain appears on the right-hand side of
(2.8.2), arriving through the record. What the verdict does not do is add to
$(O,\Pi)$. Corollary 1 is therefore the first half of the paper's claim: it says
the verdict can be informative, and it also says that all of its information is
borrowed.

**Corollary 2 (posterior invariance; the exact tail case).** (A2.2) is asserted
only on $\mathrm{Low}_\kappa$, so read this corollary conditioned on a record
$o\in\mathrm{Low}_\kappa$: if $T\perp\Pi\mid O=o$ at that record, then for every
$y\in\mathcal V$,
$$
\Pr\big[T=1\ \big|\ V=y,\,O\big]=\Pr\big[T=1\ \big|\ O\big],
\qquad
\ell(y):=\log\frac{\Pr[V=y\mid T=1,O]}{\Pr[V=y\mid T=0,O]}=0 .
\tag{2.8.3}
$$
Consequently, for any decision rule $\hat T$,
$$
\inf_{\hat T(\cdot)}\Pr\big[\hat T(V,O)\ne T\big]
\ =\
\inf_{\hat T'(\cdot)}\Pr\big[\hat T'(O)\ne T\big].
\tag{2.8.4}
$$
The verdict cannot improve on the record: it is not that reading $V$ makes the
error larger, but that it cannot make it smaller. The likelihood ratio the verdict
contributes is exactly $1$ throughout.

*Proof.* From (D2.1) and $T\perp\Pi\mid O$ one obtains $T\perp(V,\Pi)\mid O$ by
the contraction property of conditional independence; the conditional law of $T$
given $(V,O)$ therefore does not depend on $y$, giving (2.8.3). For (2.8.4): the
direction $\le$ is immediate, since a rule that ignores $V$ is a rule that uses
$(V,O)$; the reverse direction follows from (2.8.3): a rule that uses $V$ has the
same risk as the randomised rule that draws $V\sim p_{V\mid O}$ and then ignores
it, and randomisation cannot beat the optimal deterministic rule on $O$. Both
directions together give equality. $\square$

**What Corollary 2 says on the tail, in one sentence.** Where (A2.2) holds exactly,
the verdict is informationally dead: conditionally on the record,
$I(V;T\mid O)=0$, and the Bayes error of any decision equals that of a decision
that never reads $V$. This is the exact half of the paper's claim, and it is exact
rather than asymptotic for a reason worth stating: $V$ is a function of $(O,\Pi)$,
and the hypothesis removes $\Pi$ from the conditioning set, so what is left of $V$
is a function of $O$ alone and adds nothing to $O$. Corollary 2 is therefore the
statement "on the tail the verdict contributes zero", and it fails only if (A2.2)
fails.

**Proposition 8 (the measured evaluator).** If $V\equiv y_0$ almost surely, then
for **every** joint law of $(T,O)$,
$$
I(V;T)=0,
\qquad
I(V;T\mid O)=0,
\qquad
\Pr[T=1\mid V]=\Pr[T=1].
\tag{2.8.5}
$$
*Proof.* A constant is measurable with respect to the trivial $\sigma$-algebra
$\{\varnothing,\Omega\}$, so $\sigma(V)$ is trivial, $H(V)=0$, and
$I(V;T)=H(V)-H(V\mid T)=0$. The same argument gives the conditional statements.
$\square$

Proposition 8 needs no hypothesis beyond constancy: not (D2.1), not A2.2, not A3.
It applies to the measured system because the evaluator answered `PASS` on all ten
trajectories, failing and succeeding alike. Unlike (2.8.1) it is a factual claim
about a system, because its hypothesis is an observation rather than a consequence
of how the evaluator is built: the arithmetic is trivial, and the measurement is
not. For a constant evaluator the information is zero by the definition of
entropy, and no asymptotics is needed to say so.

**Corollary 3 (the value of a witness).** Define
$$
\Delta_{\mathrm{wit}}:=I\big((V,W);T\mid O\big)-I(V;T\mid O)\ \ge\ 0 .
\tag{2.8.6}
$$
The chain rule for conditional mutual information gives, as an identity and with no
hypothesis,
$$
\Delta_{\mathrm{wit}}=I\big(W;T\mid O,V\big).
\tag{2.8.7}
$$
The inequality that bounds this quantity comes from clause (ii) of Definition 4,
not from the chain rule. Applying the chain rule to $I(W;(T,V)\mid O)$ in the other
order,
$$
I\big(W;T\mid O\big)
=I\big(W;V\mid O\big)+I\big(W;T\mid O,V\big)-I\big(W;V\mid O,T\big),
$$
and $W\perp\Pi\mid(T,O)$ together with $V=f(O,\Pi)$ gives $W\perp V\mid(T,O)$, so
the last term vanishes and
$$
\Delta_{\mathrm{wit}}=I\big(W;T\mid O\big)-I\big(W;V\mid O\big)\ \le\ I\big(W;T\mid O\big),
\tag{2.8.7'}
$$
with equality iff $I(W;V\mid O)=0$. Under (A2.2) the equality holds as well, and we
can say why: on $\mathrm{Low}_\kappa$ the prior adds nothing to the record, so
$W\perp\Pi\mid O$ follows from $T\perp\Pi\mid O$ and clause (ii) by integrating out
$T$; since $V$ is a function of $(O,\Pi)$, that gives $I(W;V\mid O)=0$. Hence on the
tail
$$
\Delta_{\mathrm{wit}}=I\big(W;T\mid O\big)\qquad\text{exactly,}
\tag{2.8.7''}
$$
and the value of a witness is what the witness itself knows about the truth beyond
the record — no discount term, and no term in $\phi$. Off the tail the inequality
in (2.8.7$'$) is what survives, and it is strict only when the candidate witness is
correlated with the verdict given the record.

Two readings of (2.8.7$'$)–(2.8.7$''$) are worth stating, because one of them is
the usual mistake. A witness that is independent of the prior given the truth and
the record — clause (ii) of Definition 4 — attains the bound, and on the tail
attains it exactly. A witness that is merely a second opinion from the same prior
violates $W\perp V\mid(O,T)$, has $I(W;V\mid O)>0$, and drives
$\Delta_{\mathrm{wit}}$ to zero; that is Proposition 4, recovered as the equality
case rather than as a separate argument.

**Corollary 4 (an error-rate floor).** For $T\in\{0,1\}$ and any estimator
$\hat T$ of $T$ from an input $X$,
$$
\Pr[\hat T\ne T]\ \ge\ h_2^{-1}\big(H(T\mid X)\big),
\tag{2.8.8}
$$
where $h_2$ is the binary entropy. With $X=V$ and $H(T\mid V)=H(T)$ — which holds
by Proposition 8 — the floor is $\min\{\Pr[T=1],\Pr[T=0]\}$, the error of
guessing without looking.

**Theorem 2 (the coverage bound).** Throughout, $\mathrm{cov}(o)\in[0,1]$ is the
$\Pi$-mass of the region of the prior's support consistent with the record $o$, and
$\eta:[0,1]\to[0,\infty)$ is non-decreasing with $\eta(0)=0$. Assume (A2.2$'$),
restated here for reference:
$$
\mathrm{TV}\Big(p_{T\mid O=o,\Pi}\,,\,p_{T\mid O=o}\Big)\ \le\ \eta\big(\mathrm{cov}(o)\big)
\qquad\text{for every }o .
$$
Then for every $o$ with $\Pr[O=o]>0$ and every decision rule $\hat T(V,O)$ there is
a rule $\hat T'(O)$ reading the record alone with
$$
\Pr\big[\hat T'(O)\ne T\ \big|\ O=o\big]
\ \le\
\Pr\big[\hat T(V,O)\ne T\ \big|\ O=o\big]+\eta\big(\mathrm{cov}(o)\big),
\tag{2.8.9}
$$
and consequently, averaging over $O$,
$$
\inf_{\hat T'(\cdot)}\Pr\big[\hat T'(O)\ne T\big]
\ \le\
\inf_{\hat T(\cdot)}\Pr\big[\hat T(V,O)\ne T\big]
+\mathbb E\big[\eta(\mathrm{cov}(O))\big].
\tag{2.8.10}
$$

*Proof.* Fix $o$. By the coupling characterisation of total variation, $(T,\Pi)$
and $(T',\Pi)$ can be coupled on one probability space with $\Pi\sim p_{\Pi\mid O=o}$,
$T\sim p_{T\mid O=o,\Pi}$, $T'\sim p_{T\mid O=o}$, and $\Pr[T\ne T'\mid O=o]\le\eta(\mathrm{cov}(o))$.
Draw $V$ from $p_{V\mid O=o,\Pi}$, which is unaffected by substituting $T'$ for $T$
since it conditions on $\Pi$ and $o$ only. For any decision $y\mapsto\hat T(y,o)$,
$$
\Pr[\hat T(V,o)\ne T\mid O=o]
\ \ge\ \Pr[\hat T(V,o)\ne T'\mid O=o]-\Pr[T\ne T'\mid O=o],
$$
because the event $\{\hat T\ne T\}$ contains $\{\hat T\ne T'\}\cap\{T=T'\}$. The
second term is at most $\eta(\mathrm{cov}(o))$, and since $T'$ has law
$p_{T\mid O=o}$ the first is at least the best error achievable at $o$ by a rule
that reads $o$ alone. This is (2.8.9). For (2.8.10), average (2.8.9) over $o$
against $p_O$; the infimum on the right is attained pointwise in $o$ by a rule the
risk function makes measurable, the risk being continuous in the decision and the
decision space standard Borel. $\square$

**Reading Theorem 2, and what it deliberately does not say.** The theorem has two
regimes, and it is a statement about only one of them.

*Off the tail.* If $\mathrm{cov}(o)$ is near $1$, $\eta(\mathrm{cov}(o))$ may be
near $1$ as well and the bound is vacuous. That is the correct outcome and not a
weakness: where the prior does cover the record, the prior is informative, the
verdict may correlate with the truth well beyond what (2.8.9) allows, and
Corollary 1 already said so. A theorem that claimed otherwise would be false, and
§3.2 measures the opposite direction — enriching $O$ raised forced-choice accuracy
from $0.60$ to $0.80$.

*On the tail.* If $\mathrm{cov}(o)\to0$ then $\eta\to0$ and the verdict's
contribution to the error of the best decision vanishes. In the exact case
$\eta\equiv0$ this is Corollary 2, i.e. $I(V;T\mid O)=0$. The quantitative form
exists because we do not believe $\eta\equiv0$; it says that if the tail assumption
is wrong, it is wrong by $\eta(\mathrm{cov}(o))$ and by nothing else.

So the claim of the paper is not "the verdict carries no information". It is: the
verdict carries no information *where the record does not determine the truth*, and
the amount by which that claim can fail is the same quantity that measures how thin
the record is. That is why Theorem 2, and not (2.8.1), is the result of this
section, and why the assumption it rests on — (A2.2$'$), a claim about coverage —
is labelled empirical in Table A0 rather than promoted to an axiom.

**What Theorem 2 is a ceiling on.** It is a ceiling on a component, not on a
system. A system whose record already determines the outcome is not constrained by
it at all: the rule $\hat T'(O)$ is then as good as any rule, and the bound is
satisfied trivially. The constrained case is a system that needs its verdict
because the record is thin — and that is exactly the case in which the record is
thin. The two conditions cannot be separated, which is the content of the
parenthetical in §4.3: a system cannot be simultaneously dependent on its verdict,
operating where its prior has no coverage, and reliable.

---

## 2.9 Theorem 3 — trust and its absorption

**The chain.** Trust in an automated system's own verdicts is the classical
instance of the failure this section models~\cite{parasuraman1997humans}. Let
trust be a finite-state Markov chain $(X_k)_{k\ge0}$ on
$\mathcal X=\{0,1,\dots,K\}$ with $0$ the bankruptcy state, absorbing. Write the transition matrix in block form
$$
M=\begin{pmatrix} 1 & \mathbf 0\\ R & Q\end{pmatrix},
\tag{2.9.1}
$$
where $Q$ is the transient block on $\{1,\dots,K\}$ and $R$ the block of
transitions into $0$. Let $\tau_0:=\inf\{k\ge0:X_k=0\}$.

**Theorem 3.** Assume (H1) $\mathcal X$ is finite, and (H2) for every
$i\in\{1,\dots,K\}$ there is $m_i\ge1$ with
$\sum_{j=1}^{K}(Q^{m_i})_{ij}<1$. Then
$$
\boxed{\ \Pr[\tau_0<\infty]=1\ }
\qquad\text{and}\qquad
\mathbb E[\tau_0]=(I-Q)^{-1}\mathbf 1<\infty .
\tag{2.9.2}
$$

(H2) is an **empirical assumption** in the sense of Table A0, not an axiom, and the
difference is not bookkeeping. It asserts that trust erodes for reasons of its own —
accumulated unexplained discrepancy — at a rate that does not vanish, and no
measurement in this paper establishes it. The proof below is therefore the short
step: it is the textbook algebra that turns (H2) into absorption. The step that
connects (H2) to same-origin evaluation is Lemma 1, which follows the proof, and
what it shows is narrower than it looks — that (H2) cannot be defeated from inside
the system, not that (H2) holds.

*Proof.* Put $M_0:=\max_i m_i$. By (H2), $\sum_j(Q^{m_i})_{ij}<1$ for each $i$, and
since $Q^{M_0}=Q^{m_i}Q^{M_0-m_i}$ with $Q$ substochastic, row sums do not
increase, so $c:=\max_i\sum_j(Q^{M_0})_{ij}<1$. Then
$\Pr[\tau_0>kM_0]\le c^{k}\to0$, which gives the first claim. Also
$\rho(Q)\le\|Q^{M_0}\|^{1/M_0}_\infty<1$, so $\sum_{m\ge0}Q^m=(I-Q)^{-1}$
converges and the expectation is the row sum of the fundamental matrix. $\square$

Theorem 3 as stated is a textbook result, and we do not present it as a
contribution. What we present is the lemma that makes (H2) *credible* rather than
defeatable — and that lemma is where the same-origin assumption re-enters. No
statement below upgrades (H2) to a theorem, and the conclusion of this section is
conditional on it wherever it is stated.

**Lemma 1 (without a witness, the truth is not an input to the chain).** Assume

**(i)** the update is a function of the record, the prior and the verdict and of
nothing else, $X_{k+1}=h(X_k,O,\Pi,V_\phi)$; and
**(ii)** the state is a sufficient summary of the record,
$T\perp(O,\Pi,V_\phi)\mid X_k$.

Then the transition law of $X$ does not depend on $T$:
$$
\Pr\big[X_{k+1}=j\ \big|\ X_k=i,\ T=t\big]
=
\Pr\big[X_{k+1}=j\ \big|\ X_k=i\big]
\qquad\text{for } t\in\{0,1\}.
\tag{2.9.3}
$$
*Proof.* $X_{k+1}$ is $\sigma(X_k,O,\Pi,V_\phi)$-measurable. By (ii), $T$ is
conditionally independent of $(O,\Pi,V_\phi)$ given $X_k$, hence conditionally
independent of any measurable function of them. $\square$

Hypothesis (i) is the substantive one and it is worth naming plainly: the truth
$T$ is not an argument of the update. A system that could condition its trust
update on $T$ would be one that observes its own failure directly — that is, one
that already possesses a witness, which is exactly the case we are excluding.
Hypothesis (ii) says the trust state remembers enough of the record that the
remaining variables add nothing; when (ii) fails, the *marginal* transition can
inherit a dependence on $T$ through the correlation between $T$ and $O$ given
$X_k$. We list (ii) in the ledger rather than assume it silently, because it is
the point at which the Markov abstraction is doing real work.

Equation (2.9.3) is the whole point, but its role is narrower than it first
appears, and we state the limit explicitly. It rules out **one** mechanism: a
transition that fires when $T=0$, that is, a transition of the form "detect the
failure, retreat to a healthy state". It does **not** by itself force absorption.
A chain whose transitions ignore $T$ can perfectly well be irreducible on the
healthy states and never absorb: a system that never loses trust because it never
notices anything wrong is consistent with (2.9.3).

Absorption therefore needs the separate modelling claim (H2): that trust erodes
for reasons of its own — accumulated unexplained discrepancy — at a rate that does
not vanish. Lemma 1 is what makes (H2) *credible* rather than what implies it. Its
content is that (H2) cannot be defeated by the system repairing itself, because
every repair mechanism conditional on the truth has been excluded. The asymmetry
is the point: nothing can rescue the chain from inside, and nothing outside is
listening.

**Theorem 3$'$ (two regimes, and what a witness actually changes).** Split the
bankruptcy hazard into an internally detectable part and an externally discovered
part:
$$
q_{i,0}=\underbrace{q^{\mathrm{end}}_{i}}_{\text{detectable inside}}
+\underbrace{\lambda\,\mathbf 1[T=0]}_{\text{discovered outside, rate }\lambda}.
\tag{2.9.4}
$$
Without a witness, $\lambda$ is **exogenous**: it is the rate at which the world
happens to notice, and the system neither controls it nor learns from it. Conditional
on the truth being failure, $T=0$ throughout, the exit hazard from every transient
state is at least $\lambda$, so
$$
\Pr[\text{eventual bankruptcy}\mid T\equiv0]=1,
\qquad
\mathbb E[\tau_0\mid T\equiv0]\ \le\ 1/\lambda ,
\tag{2.9.5}
$$
with equality iff $q^{\mathrm{end}}_{i}=0$ for every $i$ — that is, in the pure
exogenous regime where the system has no internal route to noticing anything. Every
internally detectable route shortens the expectation; none lengthens it, because the
exogenous hazard is still running underneath. We write $\le$ rather than $=$ because
the equality is a claim about a system with no self-detection at all, and the systems
we discuss have some.

A witness does not drive this probability to zero. It replaces the exogenous
$\lambda$ by an endogenous transition: $q_{i,0}$ becomes $T$-measurable and can be
fed back, so the healthy set may acquire a closed class and the absorbing state
becomes avoidable rather than certain.

We prefer 3$'$ to 3 in application, because 3$'$ states what a witness does — it turns
an uncontrollable rate into a controllable one — instead of claiming a guarantee
that no engineering artefact can provide.

---

## 2.10 What this chapter does not establish

Three boundaries, stated here so that they do not have to be discovered by a
referee.

**The bound is about a component, not a capability.** (2.8.1) says the verdict
carries no information beyond $(O,\Pi)$, and (2.8.9) says how much the verdict can
be worth where the prior is thin. Neither says the system cannot succeed; a system
can succeed reliably on the strength of its observation alone, with an evaluator
that is useless and ignored. In that case $\mathrm{cov}(o)$ is large, $\eta$ is
large, and Theorem 2 is silent — by design.

**Necessity is not sufficiency.** Corollary 3 gives the value of a witness as an
upper bound, and (D4.1) gives the conditions under which it is positive. A
positive value is necessary for escaping (2.8.1). It is not sufficient for
reliability, which additionally requires that the witness be read correctly and
that the decision rule use it.

**Theorem 1 is the weakest of the three and is labelled as such.** Its rate needs
independence, Proposition 6 shows independence fails in the relevant direction,
and the true content of the section is (1.5) plus the observation that the
reliability question belongs to Theorem 2. A reader who discards Theorem 1 and
keeps Theorems 2 and 3 loses nothing essential to the argument.

**One assumption is empirical and untested by us.** (A2.2), and therefore its
relaxation (A2.2$'$), is a claim about coverage that this paper does not measure.
Chapter 3 measures a related quantity — the prior improving once the record is
enriched — but it does not measure $\eta(\mathrm{cov}(o))$ on a real tail. Until
someone does, Theorem 2 is a conditional statement, and we would rather say so here
than have a referee say it for us.
