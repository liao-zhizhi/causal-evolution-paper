# Causal Evolution Dynamics: Formalizing the Boundaries of Grounding and Hysteresis in Complex Systems

*Draft 1.0 — abstract. Every number quoted here is produced by
`evolution_sim.py` and re-checked by `--selftest` (10 invariant groups) and
`--audit-doc` (28 claims). No number is typed from memory.*

---

## Abstract

Complex systems increasingly report on their own success. When the report and
the delivery come from different places, a system can keep recording completion
after the work has stopped landing. We give this failure a formal treatment
rather than a rhetorical one.

We build a minimal formal system: nine axioms, twelve definitions, ten
inference rules, an explicit domain for every variable, and a four-valued
verdict (`PASS` / `FAIL` / `INVALID` / `NOT_RUN`) that is a statement about the
*scope* of a claim rather than about its success. Two dynamical laws are kept
separate throughout, because they are not the same equation: a saturating
metabolic law (M1, used while dormant) and a linear accounting law (M2, used
while active). Earlier versions of this work treated their concatenation as one
"unified equation"; we show they have different fixed points, different
stability and different time constants, and that the concatenation is an
assumption (A7) rather than a derivation.

Three results survive the audit.

1. **The deadlock boundary is hyperbolic and exact.** Under a quasi-static
   substrate assumption and a wake rule that requires $\kappa$ consecutive
   qualifying cycles, the dormant state is permanent if and only if
   $\chi<\chi_{\min}=1/(1-\theta_{\mathrm{wake}})$, where
   $\chi(v)=Y\phi_v v/(m_0\phi_{\mathrm{dorm}})$ is the charging margin of the
   agent itself; equivalently $\chi_0<1/(f(1-\theta_{\mathrm{wake}}))$ with
   $\chi_0=\chi(V_{\max})$ and $f=v/V_{\max}$. The two forms differ by the factor
   $f$ and must not be quoted interchangeably. Because the uptake law is unimodal,
   the margin has a finite maximum: $\sup_S\chi(S)=27.78$ and
   $\sup_S A_\infty=0.964$, attained at $S=\sqrt{K_sK_i}$. Deadlock above $0.964$
   is therefore immune to any amount of substrate — the pinned agent of §2.4 at
   $\theta=0.99$ is pinned for that reason — while below it a flood buys at most
   the factor $v_{\max}/v(S_0)=1.56$ and rescues only a margin still above
   $0.64\,\chi_{\min}$. The ceiling comes from the $S^2/K_i$ term, not from a
   decaying marginal return; we no longer claim the stronger statement, which is
   false in the range this paper's sweep covers.
2. **A closed system has no hysteresis loop.** With a Lyapunov function
   $V=S$, a batch system without feed drives $S\to0$ and then $A$ below any
   threshold in finite time; the downward edge is autonomous and the upward edge
   can never fire. The general claim that *any* hysteresis loop needs an
   external upward trigger is false (van der Pol is a counterexample), and we
   withdraw it.
3. **A drift detector with power one, and its limits.** Any affine-invariant
   statistic has power exactly $\alpha$ against linear drift; sliding-window
   variance has an expectation that does not grow with $n$. The cumulative
   potential
   $\Phi_n=n\Delta_{\mathrm{drift}}+\varepsilon_0-\varepsilon_n$ has
   signal-to-noise $n\Delta_{\mathrm{drift}}/(\sqrt2\sigma)\to\infty$. It is
   unbiased and consistent, but **not sufficient** and not efficient: the OLS
   slope has variance $12\sigma^2/[n(n^2-1)]$, an order of magnitude smaller.

We then audit our own framework and publish the audit. Twenty-eight implicit
assumptions are identified; **eleven are load-bearing** — if any one fails, at
least one of the results above or one headline number collapses. They are listed
in Table 1 with the specific theorem each supports, and the seventeen that are
not load-bearing are inventoried with their failure modes. We also withdraw two strong
claims of the earlier draft (that multiplicative availability is *necessary* in
systems, and that the observed cliff is a *phase transition*), and we downgrade
the latter to a conjecture that is, in the independent-agent limit, false.

Finally we report a controlled ablation in a 100-agent sandbox. Type-A commits a
fixed scope and reads only its own log; Type-B commits a scope that is a function
of the world's verdict. Both face the same capacity trajectory. Type-A stops
delivering permanently at cycle 100, dies at 107, and its own log ends 15.56%
above what landed. Type-B is stranded at 279. The lifetime ratio is **2.61**,
not the 9.19
that the previous draft reported; the difference is a unit error in the wake
gate, which we isolate as a three-way sensitivity table (2.61 / 2.18 / 9.19).
Wiring the `INVALID` channel into Type-A — and changing nothing else — is
sufficient for it to survive the same 300 cycles with a zero log gap. The
channel, not the drift, is what the cliff is made of.

The extinction is scheduled rather than emergent: Corollary 4 places each death
four to seven cycles after the onset, from the upkeep rates alone.

The algebraic skeleton — the threshold equivalence of Lemma 4, the mutual
exclusion of the two modes, and the totality of the four-valued verdict — is
machine-checked in Lean 4 (`Formal_Verification/Core_Theorems.lean`): 0 errors,
0 warnings, no `sorry`, with the `#print axioms` receipts printed from the
source rather than summarised here.

We make no claim of universality. The contribution is a boundary that can be
checked, three proofs that can be refuted, and a list of the assumptions that
would have to hold for either.

**Keywords**: grounding; hysteresis; deadlock; open systems; self-report;
Lyapunov methods; power of a test; assumption audit.

---

*This abstract deliberately contains no figure and no claim that is not backed
by a numbered theorem or a reproducible CSV. No section was promoted to
"complete" until `--selftest` and `--audit-doc` both passed on the commit that
contains it.*
