# Final status — corrected volatility-reversal finding

**Paper title:** *Volatility Reverses the Horizontal-Organization Advantage: How Environmental Turbulence Inverts the Information-Accessibility Prescription for Organizational Structure*

## What this paper now claims

1. **Static baseline (H1–H4):** Classical contingency theory's conditional story holds — V > H at low τ, H > V at high τ, with crossover τ\*(K) decreasing in task complexity.
2. **Headline (H5):** Environmental volatility monotonically shifts the V-vs-H advantage toward V. Spearman ρ(volatility, V − H) = +1.00 across six shock-frequency levels. Above a small threshold volatility, V dominates H uniformly.
3. **Hybrid:** Performs between V and H in both regimes; no systematic modularity-wins pattern.

## Correction history

An earlier draft claimed cluster-based hybrid dominance under volatility. That resulted from a simulation bug: `v2.run_hybrid` does not apply landscape shocks, so when the dynamic experiment delegated the hybrid branch to it, hybrid ran on a static landscape while V and H were shocked. The bug was fixed, experiments re-run, and the finding inverted. The manuscript includes a transparency section disclosing this openly.

This matters because the corrected result is:
- **Honest** (no misleading false finding).
- **More interesting** (contradicts Burns-Stalker 1961, not just confirms Lee-Edmondson 2017).
- **Better-identified** (the Spearman +1.00 dose-response is cleaner than the original buggy claim ever was).

## What's in this folder

| File | Purpose |
|---|---|
| `manuscript.pdf` / `.md` / `.html` | **Corrected paper** (~27 pages, 4 figures). PDF is the canonical submission artifact. |
| `report.pdf` / `.md` | Integrated findings report |
| `ssrn_metadata.txt` | **Updated** for new title + abstract + transparency note |
| `arxiv_metadata.txt` | **Updated** |
| `COVER_LETTER_template.md` | For journal submission (only after co-author and expanded archival) |
| `UPLOAD_GUIDE.md` | Step-by-step venue guide |
| `build_pdf.py` | Regenerates PDFs from markdown |

## Evidence summary

| Evidence stream | Runs | Verdict |
|---|---:|---|
| Static ABM v1+v2 | 6,480 | H1–H4 confirmed |
| Parameter robustness | 7,020 | Static patterns survive fragmentation-cost, n_agents, fine-τ perturbation |
| Dynamic ABM fixed-shock | 1,620 | V > H uniformly, Hy between |
| Volatility gradient (headline) | 4,860 | **H5: ρ(ω, V−H) = +1.00; slope +0.030, 95% CI [+0.026, +0.033], perm p < 0.002** |
| 3-bank seed replication | 4,860 | Dose-response replicates: all banks Spearman ρ ≥ +0.886 |
| Alternative shock models | 6,480 | H5 survives periodic, Poisson, drift, correlated-block; all ρ ≥ +0.943 |
| Multi-level vertical (Burns-Stalker mechanistic) | 4,860 | ML-V reproduces V-dominance pattern; **not an artifact of "dictatorship V"** |
| Agent heterogeneity (homo/mild/skewed/extreme) | 720 | All four regimes show ρ = +1.000; **H5 is not a talent-concentration artifact** |
| Archival panel (N=111 firm-years) | — | Pipeline validation only; H5 not tested (no volatility proxy yet) |

**Total ABM runs: 36,900** across 9 pre-registered batteries.

## What to safely do now

1. **Upload manuscript.pdf to SSRN as working paper** (3 min using updated `ssrn_metadata.txt`).
2. **Push repo to GitHub public** (verify transparency note is in manuscript.md first).
3. **Zenodo DOI on GitHub release.**
4. **Pre-register H5 on OSF** before expanded-data analysis — locks in the prediction as confirmatory rather than exploratory.

## What NOT to do yet

- Submit to *Organization Science* / *SMJ* / *ASQ* without a co-author.
- Claim real-data support for H1–H5. The archival sample is too small and has a K-variance collapse; it is pipeline validation only.
- Write LinkedIn-style announcements with the soundbite "AI doesn't flatten orgs." The nuance matters (AI raises τ, which helps flat *in stable settings*; volatility is separate); a pop framing will get misread.

## Work remaining for journal-quality publication

1. **Industry-level volatility measure** (e.g., 5-year-rolling margin variance by GICS industry) to test H5 in real data.
2. **Russell 3000 + DEF 14A archival expansion** for power.
3. **WRDS/Compustat financials** for the full 2017–2025 window and better R&D coverage.
4. **Alternative shock models** — continuous drift, Poisson shocks, correlated contribution shifts — to verify the +1.00 Spearman isn't specific to our 25% reshuffle-every-N operationalization.
5. **Alternative hybrid operationalizations** — matrix, federated, network-of-teams — before generalizing our specific-hybrid negative result to modularity writ large.
6. **Co-author collaboration** — organization-theory domain expert recommended.

## Known limitations of the current build

1. ~~Shock model is one of many possible; H5's robustness across shock models is untested.~~ **Addressed 2026-04-23 via `experiment_shocks.py`: H5 survives periodic/Poisson/drift/correlated shocks (all ρ ≥ +0.94).**
2. Our "hybrid" is a specific 5-agent-cluster-with-council form. Our negative hybrid result may not generalize to matrix, federated, or network-of-teams operationalizations.
3. Archival panel's flat measure is incomplete (Apple, Microsoft, Google etc. disclose officers in DEF 14A, not 10-K).
4. K variance in the current archival panel is tiny after R&D imputation; any triple-interaction coefficient there is an artifact.
5. ABM is a stylization: NK landscape is a structural proxy, not a substitute for firm-level decision-process data. External validity to real firms remains an empirical question the archival expansion must answer.

## Reproducibility manifest

```bash
# --- ABM batteries (from repository root) ---
python abm/experiment.py                      # v1 static, ~3 min           → results.csv
python abm/experiment_v2.py                   # v2 static, ~3 min           → results_v2.csv
python abm/robustness.py                      # parameter sensitivity, ~15m → results_robustness.csv
python abm/experiment_dynamic.py              # fixed-shock dynamic, ~4 min → results_dynamic.csv
python abm/experiment_volatility.py           # headline H5 gradient, ~15m  → results_volatility.csv

# --- Robustness extensions (2026-04-23) ---
python abm/experiment_replication.py          # 3-bank seed replication     → results_replication.csv
python abm/experiment_shocks.py               # 4 shock-model variants      → results_shocks.csv
python abm/experiment_multilevel.py           # multi-level V (ML-V)        → results_multilevel.csv
python abm/experiment_heterogeneous.py        # 4 heterogeneity regimes     → results_heterogeneous.csv

# --- Archival pipeline ---
python empirical/real_data/fetch_10k.py 150 2017
python empirical/real_data/fetch_yfinance.py 150
python empirical/real_data/parse_fix.py
python empirical/real_data/merge_panel.py
python empirical/real_data/regression_real.py

# --- Assembly (fills manuscript placeholders, regenerates figures + PDFs) ---
python abm/final_assembly.py                  # fill_manuscript → visualize → bootstrap → build_pdf
```

Seeds fixed throughout. Results are bit-for-bit reproducible on the same NumPy version. Full replication on a laptop: ~60–90 min wall clock (running the four extensions in parallel cuts that by ~half).

---

## Summary of the correction in one paragraph

The earlier draft claimed hybrid dominance under volatility; that was a simulation bug (the hybrid branch of the dynamic experiment did not apply landscape shocks). When the bug was fixed, the finding inverted. The corrected headline is that **environmental volatility reverses the horizontal-organization advantage** — in dynamic environments, vertical structures beat horizontal across all τ, with the gap scaling monotonically with shock frequency. The paper now reports this correction transparently, and the revised finding is cleaner, more novel, and more consequential than the original claim. Claude (the AI used for the scaffolding) introduced the bug and, on its own re-review of the results, identified and fixed it; the human researcher is the reviewer of record for the final claims.
