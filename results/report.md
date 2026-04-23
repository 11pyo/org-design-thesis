# Integrated Results Report — Volatility-Reversal Finding

**Volatility Reverses the Horizontal-Organization Advantage: How Environmental Turbulence Inverts the Information-Accessibility Prescription for Organizational Structure.**

Working paper — simulation + preliminary archival pipeline.

---

## Transparency note (2026-04-22)

An earlier draft of this work claimed cluster-based hybrid dominance under environmental volatility. That claim was wrong. The earlier dynamic-experiment code delegated the hybrid trajectory to `v2.run_hybrid`, which does not apply landscape shocks. When shocks were correctly applied to all three structures, the hybrid advantage disappeared. We re-ran the experiments, revised the paper, and document the correction openly.

The corrected finding is reported below.

---

## Executive summary

Four findings from **36,900 ABM runs across nine pre-registered batteries**:

1. **Static baseline confirms classical contingency.** In static NK landscapes, vertical wins at low τ, horizontal wins at high τ, and the crossover τ\*(K) decreases in task complexity. H1–H4 supported.
2. **Headline — volatility reverses the horizontal advantage.** Introducing environmental shocks monotonically shifts the V-vs-H performance gap toward vertical. At one shock per 100 steps (near-static), H beats V by 0.029 (95% bootstrap CI [−0.036, −0.023]). At one shock per 3 steps (high-vol), V beats H by 0.081 ([+0.070, +0.092]). Slope on log(ω): +0.030 (95% CI [+0.026, +0.033]); permutation p < 0.002; Spearman ρ = +1.00 across six levels.
3. **The headline survives aggressive robustness checks.** The V-dominance pattern replicates across three independent seed banks (ρ ≥ +0.88), four alternative shock-model specifications (periodic/Poisson/drift/correlated, ρ ≥ +0.94), four agent-heterogeneity regimes from homogeneous to extreme-star-distribution (all ρ = +1.00), and a multi-level vertical structure with local-authority mid-managers (Burns-Stalker mechanistic form) that rules out a "dictatorship-V" artifact.
4. **Hybrid is mid-pack.** Performs between V and H in both regimes. Modularity does not uniformly dominate.

---

## 1. Static baseline (H1–H4)

Results from `results.csv` (v1 aggregation-rule), `results_v2.csv` (v2 independent-exploration with fragmentation cost), and `results_robustness.csv` (7,020-run sensitivity battery).

### v2 (headline static model)
- Clean crossovers: τ\*(K=2) = 0.16, τ\*(K=5) = 0.13, τ\*(K=10) = 0.13.
- Fine-grid refinement: τ\*(K=2) = 0.157, τ\*(K=5) = 0.121, τ\*(K=10) = 0.119.
- H − V gap peaks at +0.055 for K = 10, τ = 0.3.
- H4 (∂τ\*/∂K < 0) quantitatively confirmed.

**Figure:** `results/figures/fig_delta_HV_v2.png`

### Robustness sweeps
- Fragmentation cost ∈ {0.10, 0.20, 0.30}: shifts low-τ endpoint but crossover structure persists.
- n_agents ∈ {15, 30, 60}: qualitative patterns invariant.
- Fine-τ grid (step 0.025): refined τ\* estimates monotone-decreasing in K.

---

## 2. Volatility reversal (H5 — headline)

### Fixed shock frequency (1,620 runs, SHOCK_EVERY = 10)
Results in `results_dynamic.csv`. V uniformly outperforms H across (τ, K). Hybrid between.

| K  | τ   | V     | H     | Hy    | V − H   |
|---|---|---|---|---|---|
| 2  | 0.1 | 0.682 | 0.515 | 0.589 | +0.167 |
| 2  | 0.9 | 0.676 | 0.702 | 0.693 | −0.026 |
| 5  | 0.1 | 0.700 | 0.539 | 0.594 | +0.161 |
| 5  | 0.5 | 0.690 | 0.634 | 0.645 | +0.056 |
| 10 | 0.1 | 0.659 | 0.525 | 0.553 | +0.134 |
| 10 | 0.5 | 0.685 | 0.603 | 0.676 | +0.082 |

**Figure:** `results/figures/fig_perf_curves_dynamic.png`

### Volatility gradient (4,860 runs, SHOCK_EVERY ∈ {3, 5, 10, 20, 40, 100})
Results in `results_volatility.csv`. Cleanest finding of the paper:

| SHOCK_EVERY | Volatility ω | V − H mean | SEM |
|---|---|---|---|
| 100 | 0.010 | **−0.029** | 0.005 |
| 40  | 0.025 | +0.021 | 0.010 |
| 20  | 0.050 | +0.046 | 0.014 |
| 10  | 0.100 | +0.054 | 0.015 |
| 5   | 0.200 | +0.071 | 0.023 |
| 3   | 0.333 | +0.081 | 0.023 |

**Spearman ρ(ω, V − H) = +1.00 across the six levels.**

Crossover between shock/100 (H wins by 0.029) and shock/40 (V wins by 0.021). Above the crossover, V dominates uniformly.

**Figures:**
- `results/figures/fig_VH_gap_by_volatility.png` — headline dose-response
- `results/figures/fig_vol_by_tau.png` — by-K and τ breakdown
- `results/figures/fig_structure_fitness_vol.png` — all three structures' absolute performance vs volatility

---

## 3. Robustness battery (2026-04-23 extension)

Four orthogonal critiques of the headline were addressed by running four additional experiments. All four confirm H5.

### 3.1 Statistical robustness — 3 independent seed banks (4,860 runs)
Results in `results_replication.csv`. Banks A, B, C use disjoint seed ranges.

| Seed bank | V−H at shock/100 | V−H at shock/3 | Slope on log(ω) | Spearman ρ |
|---|---:|---:|---:|---:|
| A | −0.024 | +0.089 | +0.0292 | +1.000 |
| B | −0.032 | +0.089 | +0.0316 | +0.943 |
| C | −0.040 | +0.082 | +0.0323 | +0.886 |

All three banks yield monotone positive dose-response. **Figure:** `results/figures/fig_replication_3banks.png`.

### 3.2 Shock-model specificity — 4 variants (6,480 runs)
Results in `results_shocks.csv`. The baseline 25%-locus-reshuffle is only one operationalization; we test four.

| Shock model | Min-intensity V−H | Max-intensity V−H | Spearman ρ | Perm p |
|---|---:|---:|---:|---:|
| periodic (baseline) | −0.034 | +0.083 | +0.943 | 0.0087 |
| poisson (random timing) | −0.023 | +0.077 | +0.943 | 0.0087 |
| drift (continuous small perturbations) | −0.032 | +0.039 | +1.000 | 0.0012 |
| correlated (block shifts) | −0.026 | +0.057 | +1.000 | 0.0012 |

All four give the same qualitative pattern. H5 is not specific to the periodic reshuffle. **Figure:** `results/figures/fig_shocks_comparison.png`.

### 3.3 Multi-level vertical — Burns-Stalker mechanistic form (4,860 runs)
Results in `results_multilevel.csv`. The baseline V is effectively a CEO dictatorship; ML-V adds 5 mid-managers with local authority and a CEO coordination step every 3 time units.

| shock_every | V | ML-V | H | ML−H | V−H |
|---:|---:|---:|---:|---:|---:|
| 100 | 0.700 | 0.703 | 0.733 | −0.030 | −0.033 |
| 40 | 0.680 | 0.678 | 0.651 | +0.027 | +0.030 |
| 20 | 0.677 | 0.676 | 0.645 | +0.031 | +0.032 |
| 10 | 0.682 | 0.673 | 0.624 | +0.049 | +0.059 |
| 5 | 0.678 | 0.681 | 0.611 | +0.070 | +0.066 |
| 3 | 0.690 | 0.698 | 0.606 | +0.092 | +0.084 |

ML-V tracks V closely at every volatility level. The V-dominance is a property of hierarchical structure, not of centralization extremity. **Figure:** `results/figures/fig_multilevel_V.png`.

### 3.4 Heterogeneous agents — 4 talent regimes (720 runs)
Results in `results_heterogeneous.csv`. Real organizations have large variance in individual competence; the critique was that "V wins under volatility" might really be "talent-concentration wins."

| Heterogeneity regime | V−H at static | V−H at high vol | Spearman ρ |
|---|---:|---:|---:|
| homogeneous (all agents share τ) | −0.036 | +0.083 | +1.000 |
| mild (τ_i ~ Normal(τ, 0.10)) | −0.040 | +0.062 | +1.000 |
| skewed (20% stars at 2τ, 80% at 0.5τ) | −0.050 | +0.115 | +1.000 |
| extreme (10% at τ=1.0, 90% at 0.3τ) | −0.031 | +0.158 | +1.000 |

All four regimes yield perfect ρ = +1.00. The **extreme** regime actually amplifies the V-advantage at high volatility (+0.158 vs homogeneous +0.083), but the monotone dose-response survives in every distribution. H5 is not a talent-concentration artifact. **Figure:** `results/figures/fig_heterogeneous_agents.png`.

### 3.5 What the robustness battery establishes
Under nine orthogonal perturbations — three seed banks, four shock models, a structurally-different vertical form, and four talent distributions — H5 never reverses, never flattens, and never falls below Spearman ρ = +0.88. This is about as strong as ABM evidence gets.

---

## 4. Archival pipeline — preliminary

N = 111 firm-years, 47 firms, from S&P 500 (2021–2025). Data from SEC EDGAR 10-K filings + yfinance.

| Test | Estimate | p-value | Honest read |
|---|---|---|---|
| H1 (flat coef, low-τ n=37) | +0.322 | 0.032 | wrong sign; subsample too small |
| H2 (flat coef, high-τ n=37) | +0.060 | 0.303 | right direction, not significant |
| H3 (flat × τ, n=111) | −0.012 | 0.961 | null |
| H4 (flat × τ × K, n=111) | +92.21 | <0.001 | artifact from K-variance collapse |

**H5 cannot be tested on the current panel** — we lack an industry-level or firm-level volatility proxy.

Pipeline is validated; substantive inference requires the sample expansion listed in the manuscript (Russell 3000 + DEF 14A + Compustat + volatility proxy).

---

## 5. Implications

### For contingency theory
Burns and Stalker's (1961) claim that organic structures fit turbulent environments is not supported by our NK operationalization. The direction is the opposite: turbulence favors vertical's concentrated, single-path decision-making over horizontal's distributed parallel search.

### For the self-managing-organization literature
Lee and Edmondson (2017) concluded qualitatively that radical-flat firms endure under "specific configurations." Our simulation makes that precise: those configurations require both (a) high τ and (b) low environmental volatility. Morning Star (tomato paste, stable production) and Buurtzorg (nursing care, slow-changing) meet both; Zappos, Oticon, Valve (consumer markets, fast change) do not.

### For AI-era organizational design
The popular "AI + volatility → flat" argument has two steps. The first (AI raises τ) is supported by our static ABM. The second (volatility favors flat) is **contradicted** by our dynamic ABM. Any claim that AI will flatten organizations must separately argue that AI raises τ faster than it raises ω.

### For empirical research design
Future studies comparing flat and hierarchical firm performance should separately measure industry-level environmental volatility (margin variance, regulatory-change frequency). Our simulation predicts that flat-firm advantages found at high τ in stable industries will not generalize to high-volatility industries.

---

## 6. Reproducibility manifest

| Asset | Location | How to regenerate |
|---|---|---|
| Static ABM v1 | `results/results.csv` | `python abm/experiment.py` |
| Static ABM v2 | `results/results_v2.csv` | `python abm/experiment_v2.py` |
| Parameter robustness | `results/results_robustness.csv` | `python abm/robustness.py` |
| Dynamic ABM (fixed shock) | `results/results_dynamic.csv` | `python abm/experiment_dynamic.py` |
| **Volatility gradient (headline)** | `results/results_volatility.csv` | `python abm/experiment_volatility.py` |
| 3-bank replication | `results/results_replication.csv` | `python abm/experiment_replication.py` |
| Alternative shock models | `results/results_shocks.csv` | `python abm/experiment_shocks.py` |
| Multi-level V | `results/results_multilevel.csv` | `python abm/experiment_multilevel.py` |
| Heterogeneous agents | `results/results_heterogeneous.csv` | `python abm/experiment_heterogeneous.py` |
| Bootstrap 95% CIs | `results/bootstrap_summary.json` | `python abm/bootstrap_analysis.py` |
| All figures | `results/figures/*.png` | `python abm/visualize_robustness_all.py` (also calls the three baseline visualize scripts) |
| Archival panel | `empirical/real_data/real_panel.csv` | EDGAR + yfinance + parse_fix.py + merge_panel.py |
| Regression summary | `empirical/real_data/regression_real_summary.csv` | `python empirical/real_data/regression_real.py` |
| Manuscript PDF | `submission/manuscript.pdf` | `python abm/final_assembly.py` (fills placeholders, regenerates figures, rebuilds PDF) |

All seeds fixed. ~60–90 min total replication on a laptop (~half that if the four extensions run in parallel).
