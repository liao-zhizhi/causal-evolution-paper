# Causal Evolution Dynamics & AI Reliability Limits

## The Three-Step Logic of Grounding Failure

The starting point is one sentence: a system reports success, but the report and the delivery do not occupy the same place. The four-valued verdict (`PASS` / `FAIL` / `INVALID` / `NOT_RUN`) is a statement about whether a claimed *scope* landed, not about whether the system felt successful.

These three papers are not parallel safety surveys. They are one continuous critical chain, from dynamics to information theory to physical embodiment.

1. **Paper 1 (dynamics).** At what boundary does a system that accounts, sleeps, and wakes stop waking up? The paper gives the failure a dynamical language: saturating rest versus linear activity kept as two laws, a hyperbolic deadlock boundary, hysteresis as mutual exclusion rather than a smear, and a four-valued lattice as collapse rather than a smooth score.
2. **Paper 2 (information theory).** Why can a digital agent, judging itself from its own observations, not see the truth? When evaluator and policy read one observation and share one prior, the verdict is a measurable function of that pair, so \(I(V;T \mid O,\Pi)=0\). The evaluator we measured was constant on this construction; its mutual information with the truth is zero *by definition*, not a universal theorem about every LLM self-evaluation. An external witness is the intervention that can move the bound.
3. **Paper 3 (physical fault).** Why does moving that digital audit onto a motor break at once on refusal, witness, and coverage? A software exception can roll back a file write; it cannot roll back a crash. A sidecar that already works for digital agents fails structurally once the effect is a state of a body: shared-scheduler refusal, physical-oracle substitution, and assurance-coverage collapse. The architecture that remains is a slow record layer and a fast enable layer whose default, on silence, is a predetermined safe state.

Each later paper takes the earlier result as a premise. It does not rewrite the earlier theorems, and it does not replace them.

This repository holds the source, the Lean 4 discrete skeleton, and the audit logs for Papers 1 and 2. Paper 3 is the next step of the same chain and has not yet been deposited on Zenodo.

> 📝 **Blog Post**: [Why Your AI Evaluator Is Structurally Blind (and how to mathematically prove it)](https://dev.to/liaozhizhi/why-your-ai-evaluator-is-structurally-blind-and-how-to-mathematically-prove-it-3mn0)
>
> 🚀 **Live Interactive Demo**: [https://demo.silicon-probe.com](https://demo.silicon-probe.com)
> *(Read-only access is anonymous. Write access for the "Simulate False Completion" button requires a demo key.)*

## Citation

Cite the concept DOI where one exists; it always resolves to the latest version. Paper 3 has no Zenodo record yet.

| Paper | Title | DOI | Core Question |
| --- | --- | --- | --- |
| Paper 1 | Causal Evolution Dynamics | [10.5281/zenodo.24032997](https://doi.org/10.5281/zenodo.24032997) | When does the system stop waking up? |
| Paper 2 | Mathematical Limits of AI Reliability | [10.5281/zenodo.24041060](https://doi.org/10.5281/zenodo.24041060) | Why can't self-evaluation see the truth? |
| Paper 3 | The Physical Grounding Fault | unpublished | Why do sidecars fail in embodied agents? |

Paper 2 version 3 (current) is [10.5281/zenodo.24135951](https://doi.org/10.5281/zenodo.24135951). The concept DOI above is the stable cite.

Full titles:

- Liao, Z. *Causal Evolution Dynamics: Formalizing the Boundaries of Grounding and Hysteresis in Complex Systems*. Zenodo. https://doi.org/10.5281/zenodo.24032997
- Liao, Z. *The Mathematical Limits of AI Reliability: Inevitable Failure under Strong Causality*. Zenodo. https://doi.org/10.5281/zenodo.24041060
- Liao, Z. *The Physical Grounding Fault: Why Software Audit Sidecars Fail in Embodied Agents*. Unpublished manuscript.

## Verification

The core discrete logic is machine-checked in Lean 4. See `Formal_Verification/Core_Theorems.lean`.
Audit logs are available in the `audits/` directory.

To compile the papers, navigate to `paper1_source/` or `paper2_source/` and run `python build.py`.

## What This Project Does Not Claim

- It will not make an LLM suddenly reliable.
- It does not retire the watchdogs and shields that physical safety engineering already uses.
- It will not give a small team an airworthiness certificate for a complete aircraft.
- We do not invent new hardware. We define how *completion* and *safety* are to be audited: take self-reported success out of the trusted channel, keep digital audit on the ledger, and leave physical refusal on independent hardware.
