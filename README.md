# Causal Evolution Dynamics & AI Reliability Limits

## The 7-Paper Progression: From Formal Verification to Physical Grounding

These are not seven parallel papers. They are one cognitive chain, from digital audit to physical fault, each step taking the previous result as a premise.

- **The Foundations (Papers 1–3).** From auditing what "PROVEN" means in EquivSVA (P1), to a bio-inspired immune runtime (P2), and then the method-transfer audit of "False Completion" in agent harnesses (P3).
- **The Physics of Emergence (Paper 4).** Fractal interfaces and bio-quantum decoherence: AI emergence as a mirage, and the demand for true physical grounding.
- **The Limits and Faults (Papers 5–7).** Formalizing deadlock boundaries in causal dynamics (P5); proving the information-theoretic limit of self-evaluation \(I(V;T \mid O,\Pi)=0\) (P6); exposing the structural faults that appear when a software sidecar is applied to an embodied agent (P7).

This repository holds the Lean 4 discrete skeleton, the audit logs, and the sources for Papers 5 and 6 (`paper1_source/`, `paper2_source/`). Paper 7 is archived at Zenodo.

> 📝 **Blog Post**: [Why Your AI Evaluator Is Structurally Blind (and how to mathematically prove it)](https://dev.to/liaozhizhi/why-your-ai-evaluator-is-structurally-blind-and-how-to-mathematically-prove-it-3mn0)
>
> 🚀 **Live Interactive Demo**: [https://demo.silicon-probe.com](https://demo.silicon-probe.com)
> *(Read-only access is anonymous. Write access for the "Simulate False Completion" button requires a demo key.)*

## Citation

Seven independent papers. Paper 4 uses the printed title on disk. Paper 6: cite the concept DOI; it always resolves to the latest version.

| No. | Title | DOI / Status | Core Question |
|:---|:---|:---|:---|
| 1 | Self-Consistency, Not Independent Verification | [10.5281/zenodo.23891927](https://doi.org/10.5281/zenodo.23891927) | What does "PROVEN" really mean in EquivSVA? |
| 2 | Agent Metabolism and Conditional Immunity | [10.5281/zenodo.23890403](https://doi.org/10.5281/zenodo.23890403) | How to build a bio-inspired immune runtime? |
| 3 | From Formal Verification to Agents | [10.5281/zenodo.23891527](https://doi.org/10.5281/zenodo.23891527) | How to transfer audit methods to Agent Harnesses? |
| 4 | Fractal Interfaces: A Quantitative Model of Cross-Scale Boundaries, Calibrated on Biological Quantum Coherence | [10.5281/zenodo.23949827](https://doi.org/10.5281/zenodo.23949827) | Why is AI emergence a strobing mirage? |
| 5 | Causal Evolution Dynamics | [10.5281/zenodo.24032997](https://doi.org/10.5281/zenodo.24032997) | When does a system reach its deadlock boundary? |
| 6 | The Mathematical Limits of AI Reliability | [10.5281/zenodo.24041060](https://doi.org/10.5281/zenodo.24041060) (v3: [24135951](https://doi.org/10.5281/zenodo.24135951)) | Why can't self-evaluation see the truth? |
| 7 | The Physical Grounding Fault | [10.5281/zenodo.24139787](https://doi.org/10.5281/zenodo.24139787) | Why do software sidecars structurally fail in embodied agents? |

## Verification

The core discrete logic is machine-checked in Lean 4. See `Formal_Verification/Core_Theorems.lean`.
Audit logs are available in the `audits/` directory.

To compile Papers 5 and 6, navigate to `paper1_source/` or `paper2_source/` and run `python build.py`.

## What This Project Does Not Claim

- It will not make an LLM suddenly reliable.
- It does not retire the watchdogs and shields that physical safety engineering already uses.
- It will not give a small team an airworthiness certificate for a complete aircraft.
- We do not invent new hardware. We define how *completion* and *safety* are to be audited: take self-reported success out of the trusted channel, keep digital audit on the ledger, and leave physical refusal on independent hardware.
