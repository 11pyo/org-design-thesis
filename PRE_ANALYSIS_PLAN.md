# Pre-Analysis Plan — Archival Test of H5

**Status:** DRAFT. Not yet filed on OSF. To be registered **before** the expanded archival sample is fetched, joined, or analyzed.

**Author:** Wonpyo Han · ORCID [0009-0002-7528-2228](https://orcid.org/0009-0002-7528-2228)
**Project:** *Volatility Reverses the Horizontal-Organization Advantage*
**Related working paper:** SSRN [6634219](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6634219) · Zenodo [10.5281/zenodo.19707964](https://doi.org/10.5281/zenodo.19707964)
**Repository commit at time of plan finalization:** to be recorded at OSF-filing time.

---

## 1. Why this plan exists

The ABM simulation reported in the working paper establishes H5 (volatility reverses the horizontal-organization advantage) with Spearman ρ = +1.00 across nine pre-registered robustness batteries. The next step is an archival test on real firm-level data. Because the ABM result is known, any archival analysis conducted *after* the fact risks being p-hacked to match. This plan commits the archival analysis design **before** data fetch, so the archival test is confirmatory rather than exploratory.

## 2. Pre-registered hypothesis (H5-archival)

> **H5-archival:** In a panel of public firms, the interaction between organizational flatness (`flat_i,t`) and information accessibility (`τ_i,t`) on firm performance is *weaker* (less positive or more negative) in industries with higher environmental volatility (`ω_j,t`). Formally, the triple-interaction coefficient β₃ in the specification below is *negative* and significant at p < 0.05 one-sided.

## 3. Data sources (declared in advance)

| Variable | Source | Measurement |
|---|---|---|
| Organizational flatness `flat_i,t` | SEC DEF 14A proxy statements + SEC 10-K Item 10 | Executive-officer count ÷ total employees (log-transformed) |
| Information accessibility `τ_i,t` | Compustat (via WRDS) | IT-capital / total-assets (Brynjolfsson-Hitt style) and R&D / sales |
| Environmental volatility `ω_j,t` | Compustat + GICS | Rolling 5-year industry (GICS-4-digit) operating-margin standard deviation, winsorized 1/99 |
| Firm performance `y_i,t` | Compustat | Return on assets (ROA); robustness with Tobin's Q and log-sales-growth |
| Firm controls | Compustat | log(assets), log(age), leverage, industry fixed effects (GICS-4), year fixed effects |

**Panel:** Russell 3000, 2017–2025, unbalanced.
**Expected N (firm-years):** 20,000 to 24,000 (post-exclusions).

## 4. Exclusions (declared in advance)

A firm-year observation is excluded if **any** of the following hold:
1. Missing executive-officer count (cannot construct `flat`).
2. Missing both IT-capital and R&D (cannot construct `τ`).
3. < 2 years of non-missing GICS-industry margin data in the preceding 5 years (cannot construct `ω`).
4. Financial firms (GICS sector 40) — different balance-sheet structure that breaks ROA comparability.
5. Firm-year has `total_assets` below the 1st percentile of the sample (shell companies).

No other exclusions. In particular, **outlier firms identified by the regression residuals are not excluded** — only the winsorization of `ω` (1/99) is applied.

## 5. Pre-registered analysis specification

```
y_i,t = β₀
      + β₁ · flat_i,t
      + β₂ · τ_i,t
      + β₃ · (flat_i,t × τ_i,t × ω_j,t)          # ← test of H5-archival
      + β₄ · (flat_i,t × τ_i,t)
      + β₅ · (flat_i,t × ω_j,t)
      + β₆ · (τ_i,t × ω_j,t)
      + β₇ · ω_j,t
      + γ · X_i,t                                 # controls
      + α_j + δ_t                                 # GICS-4 + year FE
      + ε_i,t                                     # clustered SE at firm × industry
```

- **Primary test:** β₃ < 0, one-sided p < 0.05 (Wald test).
- **Auxiliary test:** β₄ > 0, β₄ + (β₃ × ω̄_high) ≤ 0 at the 80th-percentile volatility (simple slopes test — confirms that flat×τ complementarity *vanishes* at high volatility).
- **Robustness:** Re-estimate with Tobin's Q and log-sales-growth as alternative DVs; re-estimate with industry-demand-shock shocks (Hoberg-Phillips) as alternative volatility proxy; re-estimate dropping 2020 (pandemic outlier).
- **Multiple testing correction:** primary + 3 robustness = 4 tests; Benjamini-Hochberg at q = 0.05 on the primary β₃ coefficient.

## 6. Sample-size justification

Given the expected panel size (20,000 firm-years) and typical effect sizes in organization-design archival work (β₃ standardized ≈ 0.02–0.06), the triple-interaction coefficient is powered to detect effects at ≥ 80% at α = 0.05 even under clustered errors (see Imbens & Kolesár 2016 for small-sample adjustments).

If post-exclusion N falls below 10,000, the analysis will be reported as "underpowered exploratory" rather than as a confirmatory test of H5-archival.

## 7. What counts as a failed replication

The archival test is considered to have **disconfirmed** H5-archival if any of the following hold after full preregistered analysis:
1. β₃ positive and p < 0.05 (opposite direction).
2. β₃ non-significant (p > 0.20) with SE tight enough to rule out the pre-specified effect size range.
3. Primary-analysis β₃ sign-flips in ≥ 2 of the 3 pre-specified robustness checks.

In case of disconfirmation, the working paper will be revised to report the null/opposite archival result alongside the confirmed ABM result.

## 8. What this plan deliberately does NOT commit to

- **Co-author selection** (ongoing cold-outreach) — pre-registration does not depend on it.
- **Alternative flatness measures** beyond the officer-count ratio. If those are added after data-fetch, they are labelled exploratory.
- **Cross-country extensions.** Pre-reg is US-public-firms only.
- **Pre-2017 panel depth.** We do not commit to back-filling earlier years; the 2017-start was chosen based on DEF 14A parsing reliability in the existing pipeline.

## 9. Timeline

- **T₀ (this plan finalized):** draft committed to repo.
- **T₀ + N (co-author onboarding + WRDS access):** plan reviewed with co-author, revised if warranted, **filed on OSF** with commit hash locked.
- **T₀ + N + M:** data fetched, joined, analysis run exactly as specified.
- **T₀ + N + M + P:** archival result added to manuscript as §5-archival.

## 10. Deviations policy

Any change to the pre-registered specification after OSF filing (including but not limited to: variable redefinitions, exclusion changes, analysis specification changes, DV changes) will be documented openly in a **Deviations Log** appended to this file, and the deviation will be reported explicitly in any future manuscript that uses the archival result.

---

**Signature block (to be completed at OSF-filing time):**

| | |
|---|---|
| Author: | Wonpyo Han |
| ORCID: | 0009-0002-7528-2228 |
| Repository commit: | [to be filled] |
| OSF pre-reg URL: | [to be filled] |
| Date filed: | [to be filled] |
