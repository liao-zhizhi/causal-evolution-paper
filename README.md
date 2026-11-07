# Causal Evolution Dynamics & AI Reliability Limits

This repository contains the source code, formal verification artifacts, and audit logs for two preprints on AI reliability and causal grounding.

> 📝 **Blog Post**: [Why Your AI Evaluator Is Structurally Blind (and how to mathematically prove it)](https://dev.to/liaozhizhi/why-your-ai-evaluator-is-structurally-blind-and-how-to-mathematically-prove-it-3mn0)
>
> 🚀 **Live Interactive Demo**: [https://demo.silicon-probe.com](https://demo.silicon-probe.com)
> *(Read-only access is anonymous. Write access for the "Simulate False Completion" button requires a demo key.)*

## Publications
- **Paper 1**: Causal Evolution Dynamics: Formalizing the Boundaries of Grounding and Hysteresis in Complex Systems. [DOI: 10.5281/zenodo.24032997](https://doi.org/10.5281/zenodo.24032997)
- **Paper 2**: The Mathematical Limits of AI Reliability: Inevitable Failure under Strong Causality. [DOI: 10.5281/zenodo.24041061](https://doi.org/10.5281/zenodo.24041061)

## Verification
The core discrete logic is machine-checked in Lean 4. See `Formal_Verification/Core_Theorems.lean`.
Audit logs are available in the `audits/` directory.

To compile the papers, navigate to `paper1_source/` or `paper2_source/` and run `python build.py`.
