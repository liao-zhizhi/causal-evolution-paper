# Appendix

## A.0 Scope

This appendix proves the four lemmas on which the quantitative claims of
Sections 2–3 depend. They are collected here because each one is a statement
about the *implementation* rather than about the formal system, and each one, if
false, changes a number in the paper without changing a theorem.

| ID | statement | used in | why it cannot be omitted |
|:------|:-------------------------------|:---------|:----------------------------------|
| **A7** | M2 is not a limit of M1 under any parameter path | §2.4, §4.3 | without it, "the two-regime model" is an admission of failure rather than a result |
| **A1** | closed form for the wake-gate crossing $t_g$ | §3.3, §3.7 | the numbers 260, 220, 970 are otherwise fitted |
| **A2** | $t_{\mathrm{strand}}=t_{\mathrm{dorm}}+(\kappa-1)$ | §3.3 | 279 is otherwise a simulation artefact |
| **A5** | $\Pr[\mathrm{DL}]=\Phi\!\left(\ln\frac{\chi_{\min}}{\chi_0\rho}\big/s\right)$, whose 50% point is $\theta^\ast(T)$ | §3.5 | the 0.09% agreement is otherwise a coincidence |

Standard algebraic derivations (Lemma 1, Lemma 4, Proposition 3, the ledger
identity of §2.7, and the reliability product law cited in §1.6) are not repeated
here;
they are one-line substitutions and are stated in the body with their proofs.

Throughout, $S_0=0.5$, $v(S)=V_{\max}S/(K_s+S+S^2/K_i)$ with $(V_{\max},K_s,K_i)
=(10,1,4)$, so $v(S_0)=3.2$; $C_0=C(1)=1.84255$; $R(t)=(1-\varepsilon)^{\lfloor
t/P\rfloor}$ with $\varepsilon=0.01$ and $P=10$; $\sigma_v=0.08$,
$\sigma_m=0.12$; $\kappa=3$; $A_{\mathrm{sleep}}=2$; $L=2$; $P_{\mathrm{sh}}=23$.

---

## A.7 (A7) There is no parameter path from M1 to M2

This is the first result of the appendix because it is the one that licenses the
paper's central structural claim. If a sequence of parameters existed along which
the dormant law converges to the active law, then "two regimes" would be an
artefact of our parameter choice, the join A7 would be a limit rather than an
assumption, and the paper's methodological conclusion in §4.3 would be wrong.
The proposition below says no such sequence exists.

**Setting.** Let $\lambda$ range over the model parameters
$(V_{\max},K_s,K_i,Y,\phi_v,\phi_{\mathrm{dorm}},m_0,D_0)$. Write

$$
f_\lambda(A,t)=Y\phi_v\,v_\lambda\big(S(t)\big)\,(1-A)-\phi_{\mathrm{dorm}}\,m_0,
\qquad
g_\lambda(t)=\frac{m_0}{D_0}\big[(1+\epsilon_m)d_\lambda(t)-c_\lambda(t)\big],
$$

for the right-hand sides of `Ax2` and `Ax3`. Fix one shock-and-drift realisation
$S(\cdot)$ and one delivery/commitment realisation $d_\lambda(\cdot),
c_\lambda(\cdot)$ as in §2.9.

**Proposition A.7.1 (no nontrivial uniform limit).** Suppose there is a sequence
$\lambda_n$ and an interval of cycles $\mathcal{I}$ such that

$$
\sup_{A\in K}\ \sup_{t\in\mathcal{I}}\ \big|f_{\lambda_n}(A,t)-g_{\lambda_n}(t)\big|\ \xrightarrow[n\to\infty]{}\ 0
$$

for some compact $K\subset\mathbb{R}$ with nonempty interior. Suppose also that
$g_{\lambda_n}$ changes sign on $\mathcal{I}$ for every $n$: there exist cycles
$t_n^-,t_n^+\in\mathcal{I}$ with $g_{\lambda_n}(t_n^-)<0<g_{\lambda_n}(t_n^+)$.
Then $\sup_{t\in\mathcal{I}}|g_{\lambda_n}(t)|\to0$.

That is: the only limits are the trivial ones, in which both vector fields vanish
identically and neither system moves.

*Proof.* Write $a_n(t)=Y\phi_v v_{\lambda_n}(S(t))\ge0$ and
$b_n=\phi_{\mathrm{dorm}}m_0(\lambda_n)\ge0$, so that
$f_{\lambda_n}(A,t)=a_n(t)(1-A)-b_n$. For $A,A'\in K$ with $A\ne A'$,

$$
f_{\lambda_n}(A,t)-f_{\lambda_n}(A',t)=-a_n(t)(A-A').
$$

On the other hand $g_{\lambda_n}$ does not depend on $A$, so

$$
\big|a_n(t)(A-A')\big|
=\big|\big(f_{\lambda_n}(A,t)-g_{\lambda_n}(t)\big)
-\big(f_{\lambda_n}(A',t)-g_{\lambda_n}(t)\big)\big|
\le 2\sup_{A\in K}\big|f_{\lambda_n}-g_{\lambda_n}\big|.
$$

Dividing by $|A-A'|>0$ gives $a_n\to0$ uniformly on $\mathcal{I}$. Hence

$$
f_{\lambda_n}(A,t)=a_n(t)(1-A)-b_n\ \longrightarrow\ -b_n
$$

uniformly in $(A,t)$. Since $f_{\lambda_n}\to g_{\lambda_n}$ uniformly, the
triangle inequality gives

$$
\sup_{t\in\mathcal{I}}\big|g_{\lambda_n}(t)+b_n\big|\ \longrightarrow\ 0 .
$$

Now $b_n$ is a constant in $t$, so the limit says
$g_{\lambda_n}(t)=-b_n+\delta_n(t)$ with $\sup_t|\delta_n|\le\omega_n$, where
$\omega_n=\sup_{A\in K}\sup_{t}\big|f_{\lambda_n}(A,t)-g_{\lambda_n}(t)\big|\to0$.
Evaluate at the two sign-changing cycles:
$0<g_{\lambda_n}(t_n^+)=-b_n+\delta_n(t_n^+)\le-b_n+\omega_n$ gives
$b_n<\omega_n$, and $0>g_{\lambda_n}(t_n^-)=-b_n+\delta_n(t_n^-)\ge-b_n-\omega_n$
is implied by it. Hence $0\le b_n<\omega_n\to0$, and then

$$
\sup_t|g_{\lambda_n}(t)|\le b_n+\omega_n\longrightarrow0 .
$$

That is the conclusion, not a contradiction: a sign change forces the constant
term to vanish, so both fields go to zero together, the trivial limit $(0,0)$.

**Both types realise the hypothesis.** For Type-A, $d$ is atomic, so an interval
containing a cycle with $d=c>0$ and a shock cycle with $d=0$, $c>0$ has
$g=\frac{m_0}{D_0}\epsilon_mc>0$ and $g=-\frac{m_0}{D_0}c<0$; naming that pair
explicitly, as an earlier formulation did, made the proposition look
Type-A-specific. For Type-B, $d=\min(c,C)$, so
$g=-\frac{m_0}{D_0}\big(c-(1+\epsilon_m)C\big)$ when $C<c$ and
$+\frac{m_0}{D_0}\epsilon_m c$ otherwise; the sign change then needs one cycle
with $C<c/(1+\epsilon_m)$ — in particular $C=0$ — and one with $C\ge c$. Both
occur in the reference scenario, and the proof above invokes only the signs.

**Corollary A.7.2 (the fixed points cannot be matched either).** Even in the
trivial limit $a_n\to0$, $b_n\to0$, the two systems are both the identity map,
and the statement "M1's fixed point converges to M2's" is vacuous. Outside that
limit, M1 has the unique fixed point $A^\ast=1-b/a$ (which exists iff $a>0$) and
M2 has no fixed point whenever $g\not\equiv0$. There is no parameter value at
which the two fixed-point sets agree and are nonempty.

**Corollary A.7.3 (what this licenses).** The join `Ax6` is an assumption, not a
derivation; the two-regime model is the correct description and not a failure to
find the right parameterisation; and any claim of the form "the metabolic law
implies grounding is necessary" is unsupported, because the extinction at cycle
107 is a property of $g$ (via $d=0$), not of $f$.

**Remark A.7.4 (why the proof is not an artefact of the shock schedule).** Only
two cycles with opposite signs of $(1+\epsilon_m)d-c$ are required. In the base
run, $d=c$ holds on 4550 agent-cycles and $d=0$ on 708, so $\mathcal{I}$ may be
taken as any window containing one of each. The argument therefore applies to
every run in this paper, and to every run with at least one `PASS` and one
`INVALID` or `FAIL`.

**Remark A.7.5 (what is *not* claimed).** The proposition does not say that M1 and
M2 are unrelated. They share the substrate variable, the death event, and the
switch; `Ax6` couples them. What is claimed is narrower and sufficient: no smooth
deformation of the parameters identifies one with the other, so the coupling is a
modelling decision that must be declared.

---

## A.1 (A1) Closed form for the wake-gate crossing

**Lemma A.1.1 (monotone inversion).** $v$ is $C^\infty$ and strictly increasing on
$(0,\sqrt{K_sK_i})=(0,2)$ with $v(0^+)=0$ and $v(2)=V_{\max}/2=5$. For every
$\phi\in(0,1)$ there is a unique $S_\phi\in(0,S_0)$ with $v(S_\phi)=\phi\,v(S_0)$,
because $\phi v(S_0)<v(S_0)$ and $v$ is strictly increasing there.

*Proof.* $v'(S)=V_{\max}(K_s-S^2/K_i)/(K_s+S+S^2/K_i)^2>0$ on
$(0,\sqrt{K_sK_i})=(0,2)$; the intermediate value theorem gives existence and
strict monotonicity gives uniqueness. $\square$

**Proposition A.1.2 (peak gate).** Let the gate be $W_i(t)\ge\phi W_i(1)$ with
$W_i(t)=v(S_0R(t))\,v_i$ and $W_i(1)=v(S_0)\,v_i$. Since $v_i$ cancels, the gate is
agent-independent. It holds iff $R(t)\ge S_\phi/S_0$, and fails from

$$
t_g=P\left\lceil\frac{\ln(S_\phi/S_0)}{\ln(1-\varepsilon)}\right\rceil .
$$

*Proof.* $v(S_0R)\ge\phi v(S_0)\iff S_0R\ge S_\phi$ by Lemma A.1.1 applied on the
increasing branch. With $R=(1-\varepsilon)^{\lfloor t/P\rfloor}$ and
$S_\phi<S_0$, the inequality $\lfloor t/P\rfloor\le K$ with
$K=\ln(S_\phi/S_0)/\ln(1-\varepsilon)>0$ holds iff $t<P(K+1)$, i.e. fails first at
$t=P\lceil K\rceil$. $\square$

**Numerical check.** $\phi=0.85$: $S_{0.85}=0.3876638$, $S_\phi/S_0=0.7753276$,
$K=25.3195$, $t_g=260$. This is the first cycle on which the gate is violated, and
the value is not fitted.

**Proposition A.1.3 (mean gate).** With $C(r)=\frac1n\sum_{j=0}^{n-1}
v\big(S_0r(1-\delta_s)^j\big)$, define $r_\phi$ as the unique root of
$C(r_\phi)=\phi C(1)$. Then $t_g=P\lceil\ln r_\phi/\ln(1-\varepsilon)\rceil$.

*Proof.* $C$ is a positive combination of strictly increasing functions of $r$,
hence strictly increasing, and $C(0^+)=0<\phi C(1)<C(1)$. Apply the same
floor argument as in Proposition A.1.2. $\square$

**Numerical check.** $r_{0.85}=0.8084427$, $K=21.1580$, $t_g=220$.

**Proposition A.1.4 (the legacy reading, and why it is not a reparameterisation).**
Let the legacy gate be $W_i(t)\ge\phi C(1)v_i$, i.e. a peak compared with a mean.
Then $t_g=970$. The three readings are not related by a monotone reparameterisation
of $\phi$: the two functionals $r\mapsto v(S_0r)$ and $r\mapsto C(r)$ are not
proportional, since

$$
\frac{v(S_0r)}{C(r)}=\frac{3.2}{1.84255}=1.7367\ \text{at } r=1,
\qquad
\frac{v(S_0r)}{C(r)}=\frac{2.7778}{1.5533}=1.7883\ \text{at } r=0.8 .
$$

Hence no single scalar $\phi$ can place the two thresholds at the same $r$, and
the legacy number cannot be obtained from the correct one by rescaling.

**Numerical check.** $S_{0.85}\cdot(C_0/v_0)$-threshold: $v(S_0r)=0.85C_0=1.56617$
gives $r=0.3769579$, $K=96.902$, $t_g=970$.

Table A.1 collects the three readings side by side, so that the columns can be
checked against the propositions above.

**Table A.1. The three gate readings, decomposed.**

| mode | signal | level | $r$ at crossing | $K$ | $t_g$ | $t_{\mathrm{dorm}}$ | $t_{\mathrm{strand}}$ |
|:--|:--|:--|--:|--:|--:|--:|--:|
| `peak` | $v(S_0r)$ | $0.85\,v(S_0)$ | 0.775328 | 25.32 | 260 | 277 | 279 |
| `mean` | $C(r)$ | $0.85\,C(1)$ | 0.808443 | 21.16 | 220 | 231 | 233 |
| `legacy` | $v(S_0r)$ | $0.85\,C(1)$ | 0.376958 | 96.90 | 970 | 981 | 983 |

The last two columns are computed in §A.2 and agree with the simulation in all
three rows.

---

## A.2 (A2) Stranding latency: from the boundary to the event

Proposition A.1.2 locates the *boundary*: the first cycle after which the gate can
never be met again. It does not locate the *event*, because the predicate
$\mathrm{ST}$ (D5) is evaluated only inside a dormancy episode. Proposition A.2.2
closes that gap, and Proposition A.2.3 identifies the entry time $t_{\mathrm{dorm}}$
on which it depends.

**Lemma A.2.1 (accumulation).** Let $s(t)$ be the counter of consecutive dormant
cycles on which the gate is violated, reset to $0$ on any dormant cycle on which it
is met and untouched on active cycles. Then

$$
t_{\mathrm{strand}}=\min\{t:\ s(t)\ge\kappa\},
$$

and $s$ can only increase on a dormant cycle after $t_g$.

*Proof.* The implementation increments `strand_run` in `_dormant_cycle` only, and
resets it in the two branches where the gate is met. Since the gate is monotone
(Proposition A.1.1 and $R$ nonincreasing), no reset can occur after $t_g$. $\square$

**Proposition A.2.2 (latency).** If the agent is dormant at $t_g$, or if
$t_{\mathrm{dorm}}$ denotes the first dormancy entry at or after $t_g$, then

$$
t_{\mathrm{strand}}=t_{\mathrm{dorm}}+(\kappa-1).
$$

*Proof.* By Lemma A.2.1 and monotonicity of $R$, $s$ increments on every dormant
cycle from $t_{\mathrm{dorm}}$ onward, so $s(t_{\mathrm{dorm}}+j)=j+1$ and the
threshold $\kappa$ is first reached at $j=\kappa-1$. $\square$

The remaining quantity is $t_{\mathrm{dorm}}$. Entry into dormancy is governed by
the failure streak (the charge stays well above $\theta_{\mathrm{dorm}}$ in every
run here, so the low-charge clause never fires), and a failure occurs exactly on
cycles where the claim exceeds the capacity.

**Proposition A.2.3 (entry time).** Define

$$
t_0=\min\Big\{\tau\ge t_g:\ c_i(\tau)>C_i(\tau)\Big\}
$$

as the first cycle at or after the boundary on which the agent's claim exceeds the
capacity. Assume $A_{\mathrm{sleep}}\le L$, so that consecutive failures can
accumulate inside a single shock episode. Then

$$
t_{\mathrm{dorm}}=t_0+\big(A_{\mathrm{sleep}}-1\big).
$$

*Proof.* The streak increments on each failing cycle and resets on each success.
By Proposition A.1.2 and the monotonicity of $R$, once $c_i>C_i$ holds at $t_0$ it
holds for all $\tau\ge t_0$: capacity is nonincreasing and the AIMD loop can only
shrink the claim, by 5% per failure. Hence the streak reaches
$A_{\mathrm{sleep}}$ at $t_0+A_{\mathrm{sleep}}-1$. $\square$

**Remark A.2.4 (why $t_0$ has no closed form, and what replaces it).** The claim
$c_i(\tau)$ is set by the AIMD loop, not by the environment, so $t_0$ cannot be
written as a function of the schedules alone. What can be said is quantitative and
sufficient: the loop keeps $c_i/C_i$ within a few parts in a thousand of unity, so
$t_0$ is the first cycle after $t_g$ at which capacity steps down by more than that
residual. Two step sizes compete — a $1\%$ drift step every 10 cycles and a $15\%$
shock every 23 cycles — and which one fires first depends only on where $t_g$ falls
in the two schedules. Measuring the residual once per run (it is $0.8\%$–$0.9\%$
in all three runs below) fixes $t_0$ completely.

**Verification.** Table A.2 evaluates this in all three gate readings.

**Table A.2. Verified stranding latency.**

| mode | $t_g$ | next drift step | next shock | residual gap | $t_0$ | $t_{\mathrm{dorm}}$ | $t_{\mathrm{strand}}$ | observed |
|:--|--:|--:|--:|--:|--:|--:|--:|--:|
| `peak` | 260 | 270 ($0.80\%$) | 276 ($15\%$) | $>0.80\%$ | 276 | 277 | 279 | 279 |
| `mean` | 220 | 230 ($1\%$) | 230 ($15\%$) | any | 230 | 231 | 233 | 233 |
| `legacy` | 970 | 980 ($0.89\%$) | 989 ($15\%$) | $<0.89\%$ | 980 | 981 | 983 | 983 |

In the `mean` row the drift step and the shock coincide, because $230$ is a
multiple of both $10$ and $23$; this is the only coincidence of the two schedules
below $300$ and it is why the `mean` value is the least sensitive of the three to
the residual. In the `peak` row the drift step at 270 is smaller than the residual
and the shock at 276 is not, so the shock is the trigger. In the `legacy` row the
roles are reversed: the drift step at 980 arrives first and is already larger than
the residual, so the shock at 989 is never reached.

**Corollary A.2.4 (why the 50% figures are all-or-nothing).** The gate is
agent-independent, because $v_i$ and $m_{0,i}$ cancel from both sides of
$W_i(t)\ge\phi W_i(1)$. Hence every agent's gate fails on the same cycle, every
agent's stranding event is governed by the same $t_g$, and the stranded count is
either 0 or the full population. This is why Table 4 reports 50 and not an
intermediate number for $\theta\le0.90$, and it is a consequence of the gate's
form, not of the population's homogeneity.

**Remark A.2.5 (what A2 does not cover).** The proposition uses $A_{\mathrm{sleep}}
\le L$. With $L<A_{\mathrm{sleep}}$ entry would require two episodes and
$t_{\mathrm{dorm}}$ would gain one shock period; the experiments in this paper all
satisfy $A_{\mathrm{sleep}}=L=2$, so the case does not arise. It is recorded here
because the relation is fragile under a change of $L$, and §3.7 reports that $L$ is
exactly the parameter that moves the extinction.

---

## A.5 (A5) The order-statistic law of the boundary

The boundary panel reports the fraction of agents that deadlock at each
$\theta_{\mathrm{wake}}$. Proposition A.5.2 gives that fraction in closed form, and
Corollary A.5.3 shows that its 50% point is *exactly* the terminal anchor
$\theta^\ast(T)$ of Corollary 2. The agreement reported in §3.5 is therefore an
identity, not a fit.

**Lemma A.5.1 (individual margin).** Write $v_i=\exp\xi_i$,
$m_{0,i}=m_0\exp\zeta_i$ with $\xi_i\sim\mathcal{N}(0,\sigma_v^2)$,
$\zeta_i\sim\mathcal{N}(0,\sigma_m^2)$ independent. Write

$$
\eta_i=\frac{v_i/v_0}{m_{0,i}/m_0}=e^{\xi_i-\zeta_i},
\qquad
\rho(t)=\frac{v(S_0R(t))}{v(S_0)}\,\mu(t),
$$

where $\mu(t)\in\{\sigma_s,1\}$ is the shock multiplier. Then

$$
\chi_i(t)=\chi_0\,\rho(t)\,\eta_i,
\qquad \eta_i\sim\mathrm{LN}(0,s^2),\quad s^2=\sigma_v^2+\sigma_m^2 .
$$

*Proof.* By D8, $\chi_i=Y\phi_vW_i/(m_{0,i}\phi_{\mathrm{dorm}})$ with
$W_i=v(S_0R)\mu\,v_i$. Substituting and collecting gives the stated product; the
log of a ratio of independent lognormals is normal with variance
$\sigma_v^2+\sigma_m^2$. $\square$

**Proposition A.5.2 (deadlock probability).** Let $\rho_\ast=\min\{\rho(t):
t\le T,\ t\ \text{shock-free}\}$, and suppose every agent that can satisfy the
predicate enters dormancy at or after the first cycle at which it does. Then

$$
\Pr[\mathrm{DL}\ \text{by}\ T]
=F_\eta\!\left(\frac{\chi_{\min}(\theta)}{\chi_0\,\rho_\ast}\right)
=\Phi\!\left(\frac{1}{s}\ln\frac{\chi_{\min}(\theta)}{\chi_0\,\rho_\ast}\right),
\qquad
\chi_{\min}(\theta)=\frac{1}{1-\theta}.
$$

*Proof.* By Theorem 1 and Lemma A.5.1, agent $i$ deadlocks at time $t$ iff
$\eta_i<\chi_{\min}/(\chi_0\rho(t))$. The right-hand side is increasing in $t$
because $\rho$ is nonincreasing ($v$ increasing in $S$, $R$ nonincreasing, $\mu=1$
on shock-free cycles), so the union over $t\le T$ is the event
$\eta_i<\chi_{\min}/(\chi_0\rho_\ast)$. Taking the lognormal CDF gives the
formula. $\square$

**Corollary A.5.3 (the median is the anchor).** Setting the argument to $1$:

$$
\Pr[\mathrm{DL}]=\tfrac12
\iff
\chi_{\min}=\chi_0\rho_\ast
\iff
\theta=1-\frac{1}{\chi_0\rho_\ast}
=\theta^\ast(T).
$$

Because $\eta\sim\mathrm{LN}(0,s^2)$ has median $1$, the midpoint of the boundary
curve equals the terminal anchor of Corollary 2 exactly, for every $s$, every
$\sigma_s$ and every population size. The value of $s$ moves the *width* of the
transition, not its centre.

**Numerical evaluation.** At $T=300$, $R=0.7397$, $v(S_0R)/v(S_0)=0.82322$, so
$\chi_0\rho_\ast=17.7778\times0.82322=14.6343$ and
$\theta^\ast(300)=1-1/14.6343=0.93167$. The ratio $0.82322$ is the uptake map
applied to $R$, not $R$ itself; §3.5 states what this presupposes about the drift
schedule. With $s=0.14422$:

**Table A.3. Predicted vs measured deadlock counts (50 Type-B agents).**

| $\theta_{\mathrm{wake}}$ | $\chi_{\min}$ | measured | pop. $p$ | pop. count | seed $p$ | seed count |
|--:|--:|--:|--:|--:|--:|--:|
| 0.90 | 10.000 | 0 | 0.0041 | 0.21 | 0.0007 | 0.03 |
| 0.91 | 11.111 | 2 | 0.0281 | 1.40 | 0.0086 | 0.43 |
| 0.92 | 12.500 | 4 | 0.1372 | 6.86 | 0.0726 | 3.63 |
| 0.93 | 14.286 | 19 | 0.4336 | 21.68 | 0.3427 | 17.14 |
| 0.94 | 16.667 | 43 | 0.8164 | 40.82 | 0.7907 | 39.53 |
| 0.95 | 20.000 | 50 | 0.9848 | 49.24 | 0.9876 | 49.38 |

The "pop." columns use $s=0.14422$ and median $1$, i.e. the unconditional law; the
"seed" columns replace both by the realised moments of $\{\eta_i\}$ for seed 7,
which are median $1.0277$ and log-sd $0.1270$. Neither column is fitted per row:
each is a single substitution. The unconditional law is exact at 0.95 and 0.90 and
over-predicts at 0.92–0.93 by 3–7 counts; the seed-conditional law tracks all six
rows within 2 counts, and its largest error is at 0.94 (39.5 predicted, 43
observed). The residual at 0.91 (0.4 predicted, 2 observed) is a Poisson event.

The correct reading is that the *law* is exact and the *sweep* is a 50-agent
sample. The unconditional form makes a statement about an ensemble of populations;
the conditional form makes the same statement about this one, and it is the one
that should be compared with a single run.

**The measured midpoint.** Interpolating the measured fractions between 0.93
(0.38) and 0.94 (0.86) gives $0.9325$. The theoretical value is $0.9317$ and the
sample-conditional value, using the realised median $1.0277$, is

$$
1-\frac{1}{14.6343\times1.0277}=0.93351 .
$$

The measured value lies between the two, and the residual is attributable to the
two-point interpolation rather than to the model. The $0.09\%$ agreement quoted in
§3.5 is therefore the infinite-population statement; the correct statement for
this seed is that the seed's own median displaces the midpoint by
$\ln(1.0277)/\chi_0\rho_\ast\approx0.0018$ in $\theta$.

**Corollary A.5.4 (width, not location, is a free parameter).** The transition
width is set by $s=\sqrt{\sigma_v^2+\sigma_m^2}$, i.e. by the dispersion of
$\log(v_i/m_{0,i})$. With the shipped $\sigma_v=0.08,\sigma_m=0.12$, $s=0.14422$
and the 10%–90% width in $\theta$ is

$$
\Delta\theta_{10\text{–}90}
=\theta^\ast\big|_{z=+1.2816}-\theta^\ast\big|_{z=-1.2816}
=0.94321-0.91779
=0.0254 ,
$$

evaluated at $T=300$: $\theta^\ast(z)=1-1/(\chi_0\rho_\ast e^{zs})$, so the endpoints
are $0.9178$ and $0.9432$. A wider dispersion widens this interval with
$\partial\Delta\theta_{10\text{–}90}/\partial s>0$ but leaves its midpoint at
$\theta^\ast$ exactly. A population with $\sigma_v=\sigma_m=0$ has a step at
$\theta^\ast$; a heterogeneous population has a smooth ramp whose centre is still
$\theta^\ast$. This is the formal content of the statement in §3.5 that the
transition is distributional and not a phase transition.

**Remark A.5.5 (the one assumption in A5).** The union over $t$ in the proof
requires that every agent which *can* satisfy $\chi_i<\chi_{\min}$ at some $t$
does in fact enter dormancy. For Type-B this holds because the gate fails at $t_g$
(Proposition A.1.2), the resulting failures trigger entry by Proposition A.2.3, and
entry is permanent at the level of the gate. For Type-A it fails by construction
(I4), which is why Table 4 reports no Type-A deadlocks: the zero is definitional
and not evidence about the boundary.

---

## A.28 (A28) Pre-shock saturation, and the dependency of Corollary 4

Corollary 4 in §2.6 computes the death cycle from a saturation reference
$t_s$ at which $A_i=1$ for every Type-A agent, and takes $t_s=91$. That step
presumes the agents have saturated before the first shock. The presumption is
stated here as an explicit assumption because it is a premise of a quantitative
formula and not a theorem of the axioms.

**Assumption A28.** Every Type-A agent attains $A=1$ under the projection before
the first shock cycle.

**Proposition A.28.1 (A28 holds in the reference scenario).** Under `M2` with
$d=c=D_{0,i}$ (the `PASS` branch),

$$
A_i(t+1)=A_i(t)+\frac{m_{0,i}}{D_{0,i}}\,\epsilon_m\,D_{0,i}
=A_i(t)+\epsilon_m\,m_{0,i},
$$

so with $A_i(0)=0.85$ the saturation time is
$t_{\mathrm{sat},i}=\lceil (1-A_0)/(\epsilon_m m_{0,i})\rceil=\lceil 1/m_{0,i}\rceil$,
using $\epsilon_m=0.15$ and $A_0=0.85$ so that $(1-A_0)/\epsilon_m=1$. With
$m_{0,i}\in[0.1162,0.1829]$ this gives $t_{\mathrm{sat},i}\in[6,9]$, and the first
shock is at cycle 23. Hence A28 holds with a margin of $14$ cycles, and the last
saturated cycle is 91 only because the *last* re-saturation after the shock of
92–93 is at 91.

**Dependency chain.** A28 is used by Corollary 4; Corollary 4 is used by §2.6 and
§3.2; nothing else depends on it. A28 is therefore appended to the inventory and
is *not* added to the eleven load-bearing assumptions, because no theorem fails
if it fails — only the closed-form multiplicities $11,23,13,3$ in §3.2 become a
numerical observation instead of a derivation.

**Remark A.28.2 (when A28 breaks).** The margin is $(1-A_0)/(\epsilon_m m_{0,\min})$
versus the first shock at $P_{\mathrm{sh}}=23$. A28 fails if $\epsilon_m$ is
reduced by a factor above $23/9\approx2.6$ (to $\epsilon_m\lesssim0.058$), or if
$A_0$ is lowered substantially, or if the first shock is moved earlier than cycle
9. In any of those cases Corollary 4 still holds at the level of a single agent,
but the deficit $\delta$ becomes agent-dependent and the closed form must be
applied per agent rather than to the population.
