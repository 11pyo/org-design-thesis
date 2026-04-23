# Code Audit Checklist — for the user

**Purpose:** The research assistant that built this codebase introduced one bug that produced a false "hybrid dominates under volatility" finding. The bug was caught during a follow-up experiment. This checklist exists so you — the human author — can independently verify that the *corrected* codebase is sound before making any public claims.

**Do this BEFORE uploading to SSRN, arXiv, GitHub, OSF, or any other public venue.**

Estimated time: **90–120 minutes** total (includes the 4 extension experiments added 2026-04-23).

---

## Step 1 — verify the bug is actually fixed (20 min)

### 1a. Confirm `experiment_dynamic.py` now shocks the hybrid branch

Open `abm/experiment_dynamic.py`. The Hy branch (the `else:` clause in `run_single_dyn`) should contain an explicit shock call inside its time loop:

```python
for t in range(T):
    if (t + 1) % SHOCK_EVERY == 0:
        shock(landscape, rng)        # <-- this line must exist
    ...
```

**Expected:** you see `shock(landscape, rng)` inside the Hy loop.
**Red flag:** if the Hy branch delegates to `v2.run_hybrid(...)` (which is the STATIC hybrid implementation), the bug has returned — **do not proceed**.

### 1b. Confirm `experiment_volatility.py` shocks all three structures symmetrically

Open `abm/experiment_volatility.py`. Find the `run_one` function. The V, H, and Hy branches should each call `ed.shock(landscape, rng)` inside their own time loop (not just one of them).

**Expected:** three branches, three shock calls, all inside `if (t + 1) % shock_every == 0:` guards.
**Red flag:** any branch missing a shock call.

### 1c. Run a quick smoke test

```bash
cd abm
python -c "
import experiment_volatility as ev
# Run one cell per structure at high volatility
r_V  = ev.run_one('V',  0.5, 5, 1, shock_every=3)
r_H  = ev.run_one('H',  0.5, 5, 1, shock_every=3)
r_Hy = ev.run_one('Hy', 0.5, 5, 1, shock_every=3)
print('V:',  r_V['final_fitness'])
print('H:',  r_H['final_fitness'])
print('Hy:', r_Hy['final_fitness'])
"
```

**Expected:** V generally highest under high volatility (shock_every=3). Exact numbers depend on seed but **V should not be dramatically lower than Hy**.
**Red flag:** Hy appears dramatically higher than both V and H at shock_every=3 — that would suggest the shock-bug has returned.

---

## Step 2 — verify the headline dose-response (15 min)

### 2a. Reproduce the +1.00 Spearman on your machine

```bash
cd abm
python experiment_volatility.py        # takes ~15 min
```

The last lines of output should include a Spearman correlation between volatility and V-H. You should see a value **close to +1.00** (not exactly, because RNG state may differ across machines, but **definitely positive and above +0.8**).

**Red flag:** Spearman negative or near zero.

### 2b. Check the CSV manually

```bash
python -c "
import pandas as pd
df = pd.read_csv('../results/results_volatility.csv')
g = df.groupby(['shock_every','structure'])['final_fitness'].mean().unstack()
g['V_minus_H'] = g['V'] - g['H']
print(g.sort_index())
"
```

**Expected pattern:**
- `shock_every=100`: V − H negative (H beats V — near-static regime)
- `shock_every=3`: V − H strongly positive (V beats H by 0.05 to 0.10)
- Monotone progression between.

### 2c. Re-run with dense grid for extra confidence

```bash
cd abm
python experiment_densegrid.py    # takes ~20 min
```

This produces THREE independent seed banks. All three should give Spearman ρ > +0.8. If bank A gives +1.00 but banks B and C give 0 or negative, something is very wrong.

---

## Step 3 — verify the alternative shock models (20 min)

```bash
cd abm
python experiment_shocks.py    # takes ~20 min
```

Output prints Spearman correlations for four shock types:
- **periodic** (baseline): expected ρ > +0.8
- **poisson** (random timing): expected ρ > +0.5
- **drift** (continuous small perturbations): expected ρ > +0.3
- **correlated** (correlated blocks): expected ρ > +0.5

**Red flag:** if any of these is strongly negative, the robustness claim in the manuscript is wrong — update the paper accordingly.

---

## Step 4 — spot-check the NK landscape implementation (10 min)

### 4a. Verify landscape determinism

```bash
python -c "
from abm.nk_landscape import NKLandscape
L1 = NKLandscape(N=10, K=3, seed=42)
L2 = NKLandscape(N=10, K=3, seed=42)
import numpy as np
assert np.allclose(L1._fitness_cache, L2._fitness_cache), 'DETERMINISM BROKEN'
print('landscape deterministic with same seed: OK')
"
```

### 4b. Verify fitness values are sensible

```bash
python -c "
from abm.nk_landscape import NKLandscape
L = NKLandscape(N=15, K=5, seed=1)
fits = L._fitness_cache
print(f'min fitness:  {fits.min():.3f}  (expect ~0.3)')
print(f'max fitness:  {fits.max():.3f}  (expect ~0.75)')
print(f'mean fitness: {fits.mean():.3f} (expect ~0.50)')
"
```

Any values outside [0, 1] or extreme outliers indicate a bug.

---

## Step 4.5 — verify the four extension experiments (30 min)

> Added 2026-04-23. These four experiments were run to defend the headline against the standard critiques. Each has a Spearman-ρ target that must reproduce.

### 4.5a. Verify all four extension CSVs exist and have expected row counts

```bash
cd results
for f in results_replication.csv results_shocks.csv results_multilevel.csv results_heterogeneous.csv; do
  echo "$f: $(($(wc -l < $f) - 1)) rows"
done
```

**Expected:**
- `results_replication.csv`: 4,860 rows
- `results_shocks.csv`: 6,480 rows
- `results_multilevel.csv`: 4,860 rows
- `results_heterogeneous.csv`: 720 rows

**Red flag:** any CSV missing, zero-byte, or wildly different row count.

### 4.5b. 3-bank seed replication — all banks must yield ρ > +0.8

```bash
python -c "
import pandas as pd
from scipy.stats import spearmanr
df = pd.read_csv('../results/results_replication.csv')
for b, sub in df.groupby('bank'):
    g = sub.groupby(['shock_every','structure'])['final_fitness'].mean().unstack()
    g['V_H'] = g['V'] - g['H']
    g = g.sort_index(ascending=False)  # shock_every 100 → 3 = ω increasing
    rho, _ = spearmanr(range(len(g)), g['V_H'])
    print(f'bank {b}: rho = {rho:+.3f}')
"
```

**Expected:** all three banks ρ ≥ +0.80, ideally ρ ≥ +0.88.
**Red flag:** any bank ρ ≤ 0 — indicates the dose-response is seed-specific and the headline is fragile.

### 4.5c. Alternative shock models — all four variants must yield ρ > +0.5

```bash
python -c "
import pandas as pd
from scipy.stats import spearmanr
df = pd.read_csv('../results/results_shocks.csv')
for st, sub in df.groupby('shock_type'):
    g = sub.groupby(['intensity','structure'])['final_fitness'].mean().unstack()
    g['V_H'] = g['V'] - g['H']
    g = g.sort_index()
    rho, _ = spearmanr(g.index, g['V_H'])
    print(f'{st:12s}: rho = {rho:+.3f}  min V-H = {g[\"V_H\"].min():+.3f}  max = {g[\"V_H\"].max():+.3f}')
"
```

**Expected:** periodic / poisson / drift / correlated all ρ ≥ +0.5; the first three should be ≥ +0.9.
**Red flag:** any shock model with ρ ≤ 0 — would mean the headline only holds for the baseline shock operationalization.

### 4.5d. Multi-level V — ML-V must track V, not H

```bash
python -c "
import pandas as pd
df = pd.read_csv('../results/results_multilevel.csv')
g = df.groupby(['shock_every','structure'])['final_fitness'].mean().unstack()
g = g.sort_index(ascending=False)
print(g[['V','ML','H']].to_string())
print()
print(f'V-ML mean abs diff: {(g[\"V\"] - g[\"ML\"]).abs().mean():.4f}')
print(f'V-H  mean abs diff: {(g[\"V\"] - g[\"H\"]).abs().mean():.4f}')
"
```

**Expected:** |V − ML| ≪ |V − H| at high volatility. ML-V tracks V closely (typically within 0.01); both dominate H above shock_every=40.
**Red flag:** ML sits closer to H than to V — would mean the V-advantage is a dictatorship-V artifact and the paper's Critique-3 defense collapses.

### 4.5e. Heterogeneous agents — all four regimes must yield ρ = +1.00

```bash
python -c "
import pandas as pd
from scipy.stats import spearmanr
df = pd.read_csv('../results/results_heterogeneous.csv')
for reg, sub in df.groupby('heterogeneity'):
    g = sub.groupby(['shock_every','structure'])['final_fitness'].mean().unstack()
    g['V_H'] = g['V'] - g['H']
    g = g.sort_index(ascending=False)
    rho, _ = spearmanr(range(len(g)), g['V_H'])
    print(f'{reg:12s}: rho = {rho:+.3f}  static V-H = {g[\"V_H\"].iloc[0]:+.3f}  high-vol V-H = {g[\"V_H\"].iloc[-1]:+.3f}')
"
```

**Expected:** all four regimes ρ = +1.000. The *extreme* regime should show the largest high-vol V−H (≈ +0.15); homogeneous baseline ≈ +0.08.
**Red flag:** any regime ρ < +0.8 — would mean the finding is regime-specific and the "it's really talent concentration" critique survives.

### 4.5f. Verify the shock operationalization is applied symmetrically in extension scripts

Open each of `experiment_replication.py`, `experiment_shocks.py`, `experiment_multilevel.py`, `experiment_heterogeneous.py`. For each structure branch (V, H, Hy, ML-V), confirm there is an explicit shock call:

```python
if (t + 1) % shock_every == 0:
    ed.shock(landscape, rng)      # or equivalent
```

or an alternative-shock-model call in `experiment_shocks.py`. **The original bug was that the hybrid branch delegated to a static-landscape helper. Grep each extension file for `v2.run_hybrid` — there should be no such calls inside a dynamic time loop.**

```bash
grep -n "v2\.run_hybrid" abm/experiment_{replication,shocks,multilevel,heterogeneous}.py
```

**Expected:** no matches.
**Red flag:** any match indicates the hybrid-shock bug has returned in an extension.

---

## Step 5 — reproduce the static baseline (5 min)

```bash
cd abm
python experiment_v2.py                # takes ~3 min
python -c "
import pandas as pd
df = pd.read_csv('../results/results_v2.csv')
g = df.groupby(['K','tau','structure'])['final_fitness'].mean().unstack()
g['H_minus_V'] = g['H'] - g['V']
print(g[['V','H','H_minus_V']])
"
```

**Expected:** H − V is negative at τ=0.1 (H1), positive at τ≥0.3 for K≥5 (H2). You should see the crossover.

---

## Step 6 — sign the audit (2 min)

When all 5 steps above pass, add the following to the top of the repository's `README.md` or equivalent manifest:

```
## Code audit
Audited personally by Wonpyo Han on YYYY-MM-DD at commit <hash>.
Verified: no assistant-only-written code remains unreviewed.
```

**If any step fails, do not upload.** Post an issue, ask the assistant (or a human collaborator) to investigate, and re-run the checklist.

---

## What this checklist does NOT cover

- **Substantive claims.** It verifies the code runs correctly and reproduces numbers. It does not verify that the theoretical framing is sound. For that, read `paper/manuscript.md` end-to-end.
- **Third-party review.** Even a passed audit is one person's verification. Find a co-author or submit to a replication community (e.g. `/r/AcademicReplication`, CODECHECK) for independent eyes.
- **Archival robustness.** The archival N=111 panel is explicitly labeled "pipeline validation" in the manuscript; this checklist doesn't try to rescue it.

---

## If something looks off

1. Do NOT delete or force-fix. Note what failed, screenshot it, and save the failing output to a file.
2. Re-run the failing step with a single seed (e.g. `seed=7`) to see if it's deterministic or flaky.
3. If deterministic failure: there is a real bug. Escalate.
4. If flaky: increase `seeds` and re-evaluate. Small samples of ABM can mislead.
