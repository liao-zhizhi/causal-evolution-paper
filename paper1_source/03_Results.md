# 3. Results

## 3.1 Reporting conventions

Every number in this section is produced by `evolution_sim.py` and reproduced by
`--audit-doc`, which recomputes all 28 quoted quantities from the CSVs and prints
`MISMATCH` for any that no longer hold. Three conventions apply throughout.

1. **Two different ratios are never reported as one.** The *lifespan* ratio is
   $t_{\mathrm{strand},B}/t_{\mathrm{extinct},A}$; the *output* ratio is
   $D_B/D_A$ at a common horizon. They are 2.607 and 2.401 respectively in the
   base run and they measure different things.
2. **A threshold is reported with its horizon.** By Corollary 2 of Theorem 1 the
   boundary is $\theta^\ast(t)=1-1/\chi(t)$; a number without a $t$ is a stopping
   rule.
3. **Structural zeros are labelled.** A count of zero is reported together with
   the mechanism that forces it, because several zeros in this section are
   consequences of the classifier rather than evidence about the system.

The base configuration is the one tabulated in §2.9: 50 Type-A and 50 Type-B
agents, seed 7, horizon 300, $U=0.93$, $\epsilon_m=0.15$, drift $-1\%$ per 10
cycles, shocks with $P=23$, $L=2$, $\sigma_s=0.85$, and $\theta_{\mathrm{wake}}=0.65$.

## 3.2 The base run

Figure 6(a) plots the functional population (alive and not stranded), 6(b) the
cumulative delivered and recorded output, and 6(c) the deadlock boundary. The
event sequence is deterministic and can be read off the capacity series before
any agent is instantiated.

| event | cycle | evidence |
|:--|--:|:--|
| day-1 claim / capacity, $U$ | — | $0.930$ |
| last cycle with full delivery | 99 | $\rho(99)=0.9342\ge U$ |
| delivery ceases permanently | 100 | $\rho(100)=0.9271<U$ |
| flow break-even $\rho^\ast=U/(1+\epsilon_m)$ | — | $0.8087$ |
| first death (11 agents) | 104 | Corollary 4, largest $m_{0,i}$ |
| further deaths (23, 13, 3) | 105, 106, 107 | Proposition 3 |
| Type-A extinct | 107 | Corollary 1 |
| Type-B crossover in cumulative delivery | 108 | $7685.5>7676.9$ |
| Type-B stranded | 279 | `stranded_b = 50` |
| horizon | 300 | $\rho(300)=0.673$ |

![The sandbox, three panels on one capacity trajectory. (a) Functional population: Type-A self-assessed (red), Type-A with the verdict channel (green dash-dot), Type-B causally grounded (blue). (b) Cumulative output: claimed versus landed. The gap between the red solid and red dashed traces is the virtual delivery of §3.4. (c) The deadlock boundary: confirmed deadlocks against the wake threshold, with the day-1 and horizon anchors marked.](figures/fig6_unified_evolution.png){width=100%}

Three observations follow directly from the table.

First, the onset at cycle 100 is not fitted. Proposition 2 makes it the first
cycle with $\rho(t)<U$, and the capacity series is fixed by the drift schedule
alone. Second, the four death cycles 104–107 are not a shock effect: the nearest
shocks are at 92–93 and 115–116, and Corollary 4 gives the death cycle as
$100+\lceil1/m_{0,i}-2.1\rceil$ with $m_{0,i}\in[0.1162,0.1829]$. Evaluating the
corollary on the sampled $m_{0,i}$ reproduces the multiplicities of the four
cycles exactly: 11 agents at 104, 23 at 105, 13 at 106, 3 at 107. The dispersion
of the extinction is therefore a deterministic consequence of the upkeep
distribution, not a stochastic effect. Third, Type-A is still above flow
break-even at the onset: $1.15\times0.9271-0.93=+0.1362$ per unit claim. The
extinction is a discontinuity, not a slow insolvency.

## 3.3 The lifespan gap

Type-A is extinct at cycle 107. Type-B is alive at 107 and remains alive at the
horizon; it ceases to be functional at cycle 279, when all 50 agents satisfy the
stranding predicate D5 (alive, dormant, wake gate unreachable). The lifespan
ratio is

$$
\frac{t_{\mathrm{strand},B}}{t_{\mathrm{extinct},A}}=\frac{279}{107}=2.607 .
$$

The gap is not a free parameter of the scenario. It is fixed by two crossings of
the same capacity trajectory: Type-A stops delivering when $\rho<U$, and Type-B
stops waking when $W(t)<0.85\,W(1)$. Both are computed before the run, at cycles
100 and 260 respectively; the observed Type-B event is at 279 because stranding
is defined on a dormancy episode, and the agent is not dormant at 260. The agent
must first enter dormancy — which happens at cycle 277, the second cycle of the
shock episode 276–277 — before three consecutive weak cycles (277–279) can
accumulate. The distinction between 260 (boundary) and 279 (event) is not noise;
it is the latency of the verdict rule I5, together with the requirement that
stranding be assessed inside a dormancy episode. Appendix A.1 derives 260 in closed
form from the monotone inversion of $v$, and Appendix A.2 derives
$t_{\mathrm{strand}}=t_{\mathrm{dorm}}+(\kappa-1)$ and evaluates it for all three
gate readings: 279, 233 and 983, each matching the simulation.

The ratio is not constant across drift rates. Table 2 reports the same statistic
for the drift sweep, horizon 400.

**Table 2. Lifespan ratio versus drift.**

| drift per 10 cycles | A extinct | B stranded | ratio | B alive at 400 | B deadlocked |
|--:|--:|--:|--:|--:|--:|
| 0.0% | — | — | — | 50 | 0 |
| 0.5% | 208 | $>400$ | $>1.92$ | 50 | 0 |
| 1.0% | 107 | 279 | **2.61** | 50 | 0 |
| 1.5% | 77 | 187 | 2.43 | 50 | 0 |
| 2.0% | 56 | 133 | 2.38 | 50 | 0 |
| 3.0% | 48 | 96 | 2.00 | 50 | 0 |
| 5.0% | 28 | 52 | 1.86 | 46 | 4 |

The ratio decreases monotonically with the drift rate, from 2.61 at the reference
rate to 1.86 at 5%. This is consistent with the algebra: both events scale as
$1/\varepsilon$, but Type-A's death carries an additive
$A(t_c)/m_0\approx5$ cycles that does not scale, so the ratio tends to 1 as the
drift accelerates. Reporting "Type-B lives 2.6 times longer" without the drift
rate would repeat the error that this paper is correcting.

At 5% the drift is fast enough that four Type-B agents deadlock before the
horizon; at 0.5% neither boundary is reached within 400 cycles. The regime in
which the comparison is defined is therefore $0.5\%\lesssim\varepsilon\lesssim
4\%$ per 10 cycles.

## 3.4 The ledger discrepancy

Type-A accumulates 7676.93 delivered and 8871.71 recorded over the 300 cycles, a
difference of 1194.78, or 15.563% of the delivered total. By the ledger identity
of §2.7, this equals the sum of the claimed scope over all cycles classified
`INVALID`. Figure 6(b) plots both series; the recorded series is monotone by
construction and the delivered series is flat after cycle 100.

The verdict budget is given in Table 3. Each live agent emits exactly one verdict
per cycle (I1), so the totals are agent-cycles, not population times horizon.

**Table 3. Verdict budget, base run, horizon 300.**

| verdict | Type-A | Type-B |
|:--|--:|--:|
| `PASS` | 4550 | 7500 |
| `FAIL` | **0** | 4250 |
| `INVALID` | **708** | **0** |
| `NOT_RUN` | 0 | 3250 |
| total agent-cycles | 5258 | 15000 |

Both zeros are structural and both have different causes.

- Type-A's `FAIL` count is zero because `FAIL` requires $C=0$ (the verdict table
  of §2.7), which never occurs on this trajectory; every $0<C<c$ cycle is `INVALID`. The absence of
  `FAIL` is a property of the classifier, not evidence that Type-A never failed.
- Type-B's `INVALID` count is zero because its scope is divisible and the AIMD
  loop shrinks the claim to the existing part; the residual scope is always
  non-empty. This is an implementation choice, not a theorem.

The 708 `INVALID` verdicts split into two populations with different status:
400 arise from the eight shock cycles (23, 24, 46, 47, 69, 70, 92, 93; 50 agents
each), and 308 from the terminal drought (cycles 100–107 with 50, 50, 50, 50, 50,
39, 16, 3 live agents). The shock `INVALID`s are recoverable and the agents
recover: production resumes at cycle 25 and again after each episode. The terminal
`INVALID`s are not recoverable, because the cause is monotone drift rather than a
transient ceiling.

This distinction matters for interpretation. A ledger gap of 15.6% accumulated
over 300 cycles is not by itself fatal: 56.5% of it was accumulated before cycle
100, during episodes from which the population recovered. What is fatal is that
the same classifier that records a transient ceiling as `INVALID` also records a
permanent one as `INVALID`, and Type-A's ledger map
$\mathcal{L}_{\mathrm{self}}$ books both as `PASS` and charges both in full. The
mechanism is the absence of a distinction between the two, not the magnitude of
the accumulated number.

## 3.5 The deadlock boundary

The sweep varies $\theta_{\mathrm{wake}}$ over 13 values from 0.55 to 0.99, with
50 Type-B agents per value and the same seed, horizon 300. Table 4 reports the
number of confirmed deadlocks. No Type-A agent deadlocks at any value, because
Type-A never enters dormancy (I4); the zero is definitional.

**Table 4. Confirmed deadlocks out of 50 Type-B agents.**

| $\theta_{\mathrm{wake}}$ | 0.55–0.90 | 0.91 | 0.92 | 0.93 | 0.94 | 0.95 | 0.96–0.99 |
|:--|--:|--:|--:|--:|--:|--:|--:|
| deadlocks | 0 | 2 | 4 | 19 | 43 | 50 | 50 |
| as % | 0 | 4 | 8 | 38 | 86 | 100 | 100 |

Figure 6(c) plots the same counts.

The measured half-saturation point, obtained by linear interpolation between the
0.93 and 0.94 rows, is $\theta=0.9325$. Theorem 1 with Corollary 2 gives two
analytic anchors:

$$
\theta^\ast(1)=1-\frac{1}{\chi(1)}=1-\frac{1}{17.7778}=0.9437,
\qquad
\theta^\ast(300)=1-\frac{1}{\chi(300)}=1-\frac{1}{14.6343}=0.9317 .
$$

Note which margin each line uses. $\chi(1)=17.7778$ is the operating-point margin
$f\chi_0$ with $f=0.32$, not $\chi_0=55.556$; the day-1 anchor is $1-1/\chi(1)$ and
the earlier draft printed $1-1/\chi_0$ with the numerical value of $\chi(1)$. The
numbers were right and the label was wrong, which is the kind of error that survives
a proofread and dies in a referee's calculator.

**Where $\chi(300)$ comes from, and where it does not.** The terminal anchor is not
a closed-form consequence of the constant table, and the provenance should be
stated rather than assumed. The ratio $\chi(300)/\chi(1)=0.82322$ is *not* the
geometric drop $0.99^{30}=0.73970$ that a direct reading of the drift schedule
suggests: it is $v(S_0R)/v(S_0)$ evaluated at $R=0.99^{30}$, i.e. the concave
uptake law applied to the geometric drop. The factor $0.82322/0.73970=1.113$
between them is the local curvature of $v$ at $S_0=0.5$ and nothing else. Three
implementation choices therefore enter $14.6343$: the drift is one multiplicative
event per ten cycles applied to $R$; the schedule is read through the Michaelis
function rather than through $R$ directly; and $\rho_\ast$ is taken over shock-free
cycles, since cycle $300$ itself lies in the shock episode $299$–$300$, where the
recorded capacity ratio is $0.6734$ rather than $0.823$ (the analytic ratio
$0.7922$ depressed by $\sigma_s=0.85$). The sensitivity is small but not zero: a
linear uptake would give $\chi(300)=13.1502$ and
$\theta^\ast(300)=0.9240$ instead of $0.9317$, a shift of $0.008$ in $\theta$
against a sweep resolution of $0.01$. So $0.9317$ is an observation of *this*
environment's transition law — the specific drift schedule and the specific uptake
map — and must not be quoted as a universal constant. Theorem 1 and Corollary
3$'$ are independent of it: both compare $\chi$ with $\chi_{\min}$ at a fixed
time, whatever schedule produced $\chi$.

The measured midpoint lies $0.09\%$ above the terminal anchor, and Appendix A.5
shows that the agreement is an identity rather than a coincidence: the individual
margins factor as $\chi_i(t)=\chi_0\rho(t)\eta_i$ with
$\eta_i=e^{\xi_i-\zeta_i}\sim\mathrm{LN}(0,s^2)$ and $s^2=\sigma_v^2+\sigma_m^2$,
so by Theorem 1 the deadlock probability is
$\Phi\!\left(s^{-1}\ln[\chi_{\min}/(\chi_0\rho_\ast)]\right)$; its argument is zero
exactly at $\theta=\theta^\ast(T)$, and a lognormal has median one. The midpoint of
the curve *is* the terminal anchor for every dispersion, every population size and
every seed. Dispersion moves the width of the transition, not its centre.

For this seed the realised sample median of $\eta_i$ is $1.0277$ rather than
exactly $1$, which predicts a midpoint of $0.9335$; the measured $0.9325$ lies
between the two, the residual being the error of interpolating a smooth curve with
two points. The $0.09\%$ figure is the infinite-population statement, and the
seed-conditional figure is $0.0018$ in $\theta$. Both are reported because the
distinction between an identity and a fit is the difference between a theorem and
a coincidence.

The first cohort of deaths is not explained by the terminal anchor, and is
explained by the day-1 anchor: at $\theta=0.95$, 44 of 50 agents are confirmed at
cycle 27; at $\theta=0.94$, 17 of 43. These are the agents whose individual
$\chi_i=17.7778\,v_i/m_{0,i}$ lies below $\chi_{\min}$ before any drift has
accumulated, and cycle 27 is the first confirmation window after the shock
episode at 23–24. The remaining deaths at $\theta=0.94$ occur at 50, 73, 119,
142, 165, 188, 203, 234, 257, 280 and 292 — that is, at successive confirmation
windows, each three cycles after a shock episode. Both the onset and the midpoint
are therefore predicted by the same family $\theta^\ast(t)$ evaluated at the
appropriate time, and neither is predicted by a single constant. Table A.3 of the
appendix compares the predicted and measured counts at all six thresholds; the
largest discrepancy is at $\theta=0.91$, where the unconditional law predicts
$1.4$ and the seed-conditional law $0.4$, against $2$ observed.

**The left tail is clean.** The previous implementation confirmed deadlock on a
single cycle, using the shock-depressed peak; $\theta=0.90$ then produced 2
confirmed deadlocks out of 50 and $\theta=0.92$ produced 12, forming a
non-monotone shoulder driven entirely by transient shocks. Under I5, $\theta=0.90$
produces 0 and the sequence is monotone from 0.91 onward. The shoulder was an
artefact of the verdict rule, not a feature of the boundary.

**The boundary is not a step.** Between $\theta=0.90$ and $0.95$ the fraction
rises from 0 to 1 over a width of 0.05, and the two ends are governed by different
mechanisms: the onset by the lower tail of $\chi_i$, the saturation by
$\chi_i>\chi_{\min}$ for the whole population. This is a distributional transition,
not a phase transition in the sense of D11. With independent agents the fraction
is $1-F_\chi(\chi_{\min})$ for a smooth $F_\chi$, so no non-analytic point and no
diverging susceptibility exists at finite $N$; the width is set by the dispersion
of $\log(v_i/m_{0,i})$, i.e. by $\sqrt{\sigma_v^2+\sigma_m^2}=0.144$.

## 3.6 The ablation

Two arms are run with the same population, seed, capacity trajectory and shock
schedule. The only difference is the ledger map of §2.7. Table 5 reports the
comparison; both arms appear in Figure 6 as the green dash-dot trace, alongside
the `self` arm in red.

**Table 5. Ablation on the verdict channel.**

| arm | extinct | alive at 300 | delivered | recorded | gap | `INVALID` |
|:----------------|-------:|---------:|----------:|----------:|--------------:|---------:|
| `self` | 107 | 0 | 7676.93 | 8871.71 | 1194.78 (15.563%) | 708 |
| `r7` | — | 50 | 23602.92 | 23602.92 | **0.00** | 4950 |

At cycle 107, the cycle at which the `self` arm is extinct, the `r7` arm has
delivered 8892.11 against 7676.93 — a difference of 15.8%, which is the same
quantity as the ledger gap. By the horizon the `r7` arm has delivered 3.07 times
the `self` arm's total, and its recorded output equals its delivered output
exactly, by construction of $\mathcal{L}_{\mathrm{r7}}$.

Two features of Table 5 require comment rather than emphasis.

First, the `r7` arm's `INVALID` count is 4950, seven times the `self` arm's 708.
The channel does not reduce the number of partial-scope cycles; it classifies them
and charges only for the part that exists. Under $\mathcal{L}_{\mathrm{self}}$ the
same 4950 cycles would have been booked as `PASS` and charged in full. The
increase in `INVALID` is therefore the measure of the reclassification, not a
deterioration.

Second, and this constrains the claim, **the `r7` arm has no dormancy**. Type-A
never sleeps (I4), so the `r7` arm cannot strand; its survival at the horizon is
the joint consequence of the channel and the absence of a dormant phase. The
ablation therefore isolates one variable — the ledger map at the moment a cycle is
classified `INVALID` — and shows that this variable alone is sufficient to remove
the extinction at cycle 107 under an unchanged capacity trajectory. It does not
show that a system with both the channel and a dormant phase would survive, and
it does not support the reading "adding the verdict yields immortality". A system
with dormancy and the channel must still cross the stranding boundary of D5, and
that boundary is untouched by R7.

## 3.7 Sensitivity

**Wake-gate unit (A20).** The gate admits three readings, all implemented and
selectable. Table 6 reports the consequences; the legacy reading is retained only
to quantify the defect described in §2.7.

**Table 6. Wake-gate readings, same population and horizon.**

| mode | signal unit | level unit | B stranded | lifespan ratio |
|:--|:--|:--|--:|--:|
| `peak` (reported) | peak | $0.85\times$day-1 peak | 279 | 2.607 |
| `mean` | cycle mean | $0.85\times$day-1 mean | 233 | 2.178 |
| `legacy` | peak | $0.85\times$day-1 mean | 983 | 9.187 |

The first two are self-consistent and differ by 20%; the third mixes units and
differs from them by a factor of 3.5. No number in this paper depends on the
legacy reading, and the 9.2 reported in the earlier draft is withdrawn.

**Shock duration versus depth.** Varying $L$ at fixed depth moves the extinction
from 108 to 31 cycles; varying the depth over $0.35,0.50,0.70,0.85$ at fixed
$L=2$ leaves it at 107 at all four. The invariance has a mechanism rather than
being an accident of the four values: by Proposition 2 delivery is atomic, so a
struck cycle contributes the same deficit $m_0c/D_0$ at depth $0.35$ and at
$0.85$, and depth enters the Type-A death clock only through
$\mathbf{1}[\rho<U]$, which all four depths trip at every episode. (Depth does
enter $\chi$, hence the Type-B boundary, through $W=v(S_0R)\sigma$; that is
§3.5, a different question.) The claim is therefore scoped to
$0.35\le\text{depth}\le0.85$ at $P=23$ and to shocks deep enough to leave
$\rho<U$: a depth shallow enough to keep $\rho>U$ in the early, high-$\rho$
episodes is not covered by it. The duty-cycle threshold implied by the accounting
identity is $L/P<\epsilon_m/(1+\epsilon_m)=13.04\%$, i.e. $L<3.0$ at $P=23$; the
transition between $L=3$ (106) and $L=4$ (101) and the collapse at $L=6$ (51) are
consistent with it. Duration is decisive in the tested range and depth is
invisible there; neither statement is a theorem.

**Operating margin.** Type-A is extinct at every tested margin from $-5\%$ to
$+25\%$, at cycles 69, 93, 103, 107, 107 and 108. The extinction is not a
consequence of a thin margin; a larger margin delays it by at most one cycle,
because the onset is set by $\rho<U$, which the margin does not enter.

## 3.8 What these results do not show

1. **The 2.61 ratio is conditional on the drift rate** (Table 2) and on the gate
   reading (Table 6). It is not a constant of the framework.
2. **Type-B is not immortal.** It is alive at the horizon and non-functional from
   cycle 279. Its survival is bounded by the stranding boundary, and at 5% drift
   four agents deadlock before the horizon.
3. **Zero deadlocks at $\theta=0.65$ is arithmetic.** The margin to the day-1
   boundary is $0.9437-0.65=0.29$; no agent can cross it. The base run provides no
   evidence about the boundary's location, only about its non-triggering.
4. **The boundary sweep is truncated at 300 cycles.** By Corollary 2 the boundary
   moves left with the horizon; a sweep at 600 cycles would report higher counts
   at every $\theta$ above 0.90.
5. **One seed.** Population statistics have sampling error of order
   $1/\sqrt{50}=14\%$ in the counts of Table 4; the two entries at $\theta=0.91$
   and $0.92$ (2 and 4 agents out of 50) should be read as counts, not as rates.
6. **The `r7` arm conflates two changes** (channel, no dormancy), as stated in
   §3.6.

## 3.9 Summary of claims and their evidence class

Table 7 collects the claims established in this section, each with its evidence
class and the observation that would falsify it. Every row points back to a
theorem, a corollary or a reported number.

**Table 7. Each claim with its class and its falsifier.**

| claim | class | number | falsified if |
|:--|:--|:--|:--|
| $\mathrm{DL}\iff\chi<\chi_{\min}$ | Theorem 1 | $\chi(1)=17.78$, $\chi_{\min}=17.78$ at $\theta^\ast=0.9437$ | a dormant agent with $\chi>\chi_{\min}$ and $A(0)\le\theta$ fails to wake |
| boundary moves with horizon | Corollary 2 | $0.9437\to0.9317$ over 300 cycles | measured midpoint is horizon-independent |
| atomic stop at $\rho<U$ | Proposition 2 | cycle 100 | onset differs from the crossing of $\rho$ and $U$ |
| drought rate $m_0$ | Proposition 3 | deaths at 104–107 | the death interval does not scale as $1/m_0$ |
| lifespan gap | simulation | 2.607 | the peak reading is shown to be the wrong reading for this system, i.e. that the gate must compare cycle means rather than peaks |
| ledger gap | simulation | 1194.78 (15.563%) | recorded equals delivered under `self` |
| boundary midpoint | simulation | 0.9325 vs 0.9317 | the sweep is repeated at another horizon and does not move |
| channel is load-bearing | ablation | 107 vs none | `r7` arm dies, or `self` arm survives |
| closed systems have no loop | Proposition 4 | — | a closed batch system with a sustained loop is exhibited |

The first four rows are theorems and are parameter-free up to the stated
conditions. The fifth through eighth rows are simulation results at one
configuration; they are machine-checkable (`--selftest`, `--audit-doc`) but they
are not universal, and the paper does not present them as such.
