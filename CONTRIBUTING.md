# Contributing / Reviewing

Thanks for engaging with this working paper. Contributions, critiques, and independent verifications are all welcome.

## If you want to verify a specific claim

Start with [`AUDIT_CHECKLIST.md`](AUDIT_CHECKLIST.md). It walks through six steps — roughly 90–120 minutes — that independently reproduce the main findings and rule out the specific bug that was caught and corrected during development. Running the checklist on your machine is the most informative thing you can do.

If a step in the checklist fails on your machine, please [open an issue](https://github.com/11pyo/org-design-thesis/issues) with:
- which step failed
- the command you ran
- the full output (attach as a file if >50 lines)
- your Python version (`python --version`) and NumPy version (`python -c "import numpy; print(numpy.__version__)"`)

## If you spot a substantive problem

Open an issue describing:
- the specific claim you believe is wrong
- the minimal change that would test your concern (e.g. "re-run `experiment_volatility.py` with `SHOCK_EVERY=15` added to the grid")
- any reference that supports your critique

Substantive critiques are more helpful than stylistic ones at this stage. The paper is a working paper; peer review has not begun; most decisions are still revisable.

## If you want to extend the work

Good candidates for extension that the author would find useful:
1. **Real-data test of H5.** See [`PRE_ANALYSIS_PLAN.md`](PRE_ANALYSIS_PLAN.md) — the archival-test design is pre-specified and the pipeline scaffolding is in [`empirical/real_data/`](empirical/real_data/). Compustat / WRDS access required.
2. **Alternative hybrid forms.** The paper's negative hybrid result is specific to a five-agent-cluster-with-council configuration. Matrix, federated, and network-of-teams forms are not modeled.
3. **Alternative shock operationalizations.** We test four (periodic, Poisson-timed, continuous drift, correlated-block). Regime-switching shocks, adversarial shocks, and shocks correlated with org actions are open.
4. **Theoretical positioning.** The author is actively seeking an organization-theory co-author who can frame the result relative to Siggelkow-Rivkin, Puranam-Alexy-Reitzig, Lee-Edmondson, and the turbulence-adaptation literature.

## If you want to collaborate

Email `pk102h@naver.com` with:
- your institutional affiliation (or independent-researcher status)
- a one-paragraph statement of what you'd contribute
- the most relevant paper you've published (or GitHub project you've released)

The author's own stated collaboration need is on the theoretical-framing side; computational extensions are welcome but secondary.

## Code-style expectations

- Python 3.9+ only.
- Stick to NumPy / pandas / SciPy / matplotlib / tqdm. No new heavy dependencies without discussion.
- Every experiment script must (a) set a seed, (b) write its output to `results/results_{name}.csv`, and (c) be idempotent on reruns.
- Every new experiment must also appear in [`AUDIT_CHECKLIST.md`](AUDIT_CHECKLIST.md) with verification steps and expected outputs.

## What the maintainer will NOT merge

- Changes that break deterministic reproducibility (removing seed fixing, non-deterministic parallelization, version-unlocked dependencies).
- Silent bug fixes. If a bug is caught, the fix must be accompanied by an update to the manuscript's transparency note.
- Rewrites of the audit checklist that weaken verification coverage.

## License

By contributing you agree that your contribution is licensed under the repository's [CC BY 4.0 license](LICENSE).
