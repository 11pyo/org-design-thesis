# Empirical analysis scaffold

Three scripts operationalize the Phase 2 strategy from `paper/proposal-en.md`.

## Files

| File | Role |
|---|---|
| `synthetic_data.py` | Generates 500-firm × 8-year panel with a known DGP that embeds H1–H4. Used to validate the regression pipeline before real-data deployment. |
| `regression.py` | Runs the four hypothesis tests: subsample OLS for H1/H2, moderation for H3, triple interaction for H4. Estimates implied τ\*(K). |
| `did_template.py` | Difference-in-differences scaffold for firms that flattened after an exogenous event. Treatment identification on synthetic data is intentionally ad hoc — replace `build_treatment_table` with a real treatment list. |

## Synthetic-data validation results

Running the pipeline on the shipped synthetic data recovers the hypothesized patterns:

| Test | Coefficient | p-value | Support |
|---|---|---|---|
| H1 low-τ subsample | flat = **−0.027** | 0.036 | ✓ |
| H2 high-τ subsample | flat = **+0.051** | <0.001 | ✓ |
| H3 full-sample moderation | flat × τ = **+0.136** | <0.001 | ✓ |
| H4 triple interaction | flat × τ × K = **+0.021** | 0.089 | marginal |

Implied τ\*(K) from the regression: **0.63 → 0.43 → 0.36** as K goes 3 → 6 → 9. Correct H4 direction (τ\* decreasing in K).

This validates that the pipeline can recover the target signal at realistic sample sizes when the DGP holds.

## Moving to real data

Replace `synthetic_data.py` with a loader that produces the same schema:

```
firm_id, year, industry, log_size, log_age, flat, tau, K, ROA
```

Recommended real-data sources (all free or low-cost):

1. **SEC EDGAR 10-K filings** — `sec-edgar-downloader` on PyPI; parse the "Executive Officers" and "Organization" sections for layer count (→ `flat`).
2. **Compustat via WRDS** — if university access available; gives `log_size`, `ROA`, industry.
   - Free fallback: `yfinance` + manual cleanup for a smaller S&P 500 subset.
3. **LinkedIn** — public profiles (respect ToS; use rate limits); count data/analytics job titles as share of total headcount (→ `tau` component).
4. **10-K narrative** — keyword frequency of "data-driven", "analytics", "AI", "dashboard" (→ `tau` component).
5. **USPTO patent data** — Fleming-Sorenson industry ruggedness index (→ `K`).
6. **IT spending** — proxies available in 10-K R&D + technology capex disclosures.

## Identification notes

- **OLS in `regression.py`** — clustered SEs at firm level. Adequate for descriptive evidence but does not establish causality.
- **DiD** — the template shown is only suggestive; real identification requires a legitimate exogenous treatment (merger, CEO turnover, industry shock) and a parallel-trends diagnostic.
- **Instrumental variables** are a natural next step: use trade-liberalization or broadband-rollout shocks as instruments for τ (following Guadalupe-Wulf 2010).

## Run

```bash
cd empirical
python synthetic_data.py     # writes synthetic_firms.csv
python regression.py         # prints hypothesis-test table, writes regression_summary.csv
python did_template.py       # DiD scaffolding
```
