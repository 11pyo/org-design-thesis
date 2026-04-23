# Agent-Based Model

Two models, both testing the same four hypotheses (H1–H4) on NK fitness landscapes.

## Why two models

The theory in `paper/hypotheses.md` can be operationalized in more than one way. We ship two to show the hypotheses survive a meaningful perturbation of modeling choices — and to be transparent about where each model "buys" the finding.

### v1 — aggregation-rule model (`experiment.py`)

- Single firm state; all agents propose one-bit flips from it.
- Vertical: CEO picks best from reports; firm moves.
- Horizontal: firm moves only if ≥33% of agents agree on the same flip.
- Hybrid: within-cluster majority → cross-cluster majority.

What this model captures well: **decision-aggregation friction**. The consensus requirement means horizontal stalls when tau is low and proposals don't converge.

What it doesn't capture: **search diversity**. All agents search from the same state.

### v2 — independent-search with coordination cost (`experiment_v2.py`)

- Agents maintain their own states, searching in parallel.
- Vertical: agents follow CEO's trajectory.
- Horizontal: agents search independently, share with partners at rate τ.
- Fragmentation cost applied to horizontal: firm fitness = modal state fitness − 0.20 × (1 − concentration). Rewards convergence.

What this model captures: **Lazer-Friedman (2007)** — parallel search finds better peaks but needs convergence to realize value.

## Run

```bash
pip install -r requirements.txt
python experiment.py          # v1, ~3 min
python experiment_v2.py       # v2, ~3 min
python visualize.py           # generates figures in ../results/figures/
```

Outputs:
- `../results/results.csv`, `../results/results_v2.csv` — one row per run (3,240 each)
- `../results/figures/*.png` — performance curves, Δπ(τ) plots, heatmaps, τ\* vs K
- `../results/tau_star_estimates.json` — estimated crossover thresholds

## Parameters

| Parameter | Value | Justification |
|---|---|---|
| N (locus count) | 15 | Allows exhaustive precompute (2^15 states) for fast lookup |
| K (complexity) | {2, 5, 10} | Low / medium / high ruggedness; calibrate to Fleming-Sorenson (2001) industry quantiles in real work |
| τ | {0.1, 0.2, …, 0.9} | Evenly spaced grid; finer resolution in robustness check |
| n_agents | 30 | Large enough for horizontal aggregation; small enough for speed |
| T (time steps) | 40 | Empirically: convergence by T≈20 for simple landscapes, T≈40 for rugged |
| seeds | 40 | Balances statistical power and runtime |
| CEO τ boost (v1, v2) | 1.3× | Models dedicated information infrastructure at top |
| consensus_frac (v1 H) | 0.33 | Plurality threshold; robustness check with {0.25, 0.50} recommended |
| FRAGMENTATION_COST (v2) | 0.20 | Tunable; dominant sensitivity parameter (see robustness notes) |

## Robustness checks to run before publishing

1. Vary `FRAGMENTATION_COST` ∈ {0.1, 0.2, 0.3} — does τ\* shift monotonically?
2. Vary `consensus_frac` ∈ {0.25, 0.33, 0.50} — does H2 survive at 50%?
3. Finer τ grid (0.05 step) around each observed crossover.
4. Alternative landscape families: NKCS (Kauffman & Johnsen), random Boolean nets.
5. Larger n_agents (50, 100) — does horizontal's advantage scale?
6. Seeds ≥ 200 for tight CIs on τ\* estimates.

## Extending

- **Dynamic landscapes**: environmental shocks every τ_shock steps that redraw contributions. Expect horizontal advantage to widen (slower information arrival penalizes vertical more).
- **Role-specialized agents**: heterogeneous expertise attributes per agent. Current model treats all agents as interchangeable; a principled extension assigns agents to landscape subregions.
- **Cost of being an agent**: add per-agent budget; horizontal orgs pay more for diversity. This tests whether the H advantage survives when head-count is priced.
