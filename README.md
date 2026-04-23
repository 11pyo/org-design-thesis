# Volatility Reverses the Horizontal-Organization Advantage

*How Environmental Turbulence Inverts the Information-Accessibility Prescription for Organizational Structure*

**Working paper** · Wonpyo Han · 2026

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

---

## TL;DR

In agent-based simulation on Kauffman NK fitness landscapes, environmental volatility does **not** favor horizontal structures — it *reverses* the horizontal advantage. Across **36,900 simulated firm-level runs** spanning nine pre-registered batteries, the Spearman correlation between shock frequency ω and the V−H performance gap is **+1.00**; the slope on log(ω) is +0.030 (95% CI [+0.026, +0.033], permutation p < 0.002). Above a small threshold volatility, vertical dominates horizontal across all information-accessibility levels τ. The result survives three independent seed banks (all ρ ≥ +0.88), four alternative shock-model specifications (all ρ ≥ +0.94), four agent-heterogeneity regimes (all ρ = +1.00), and a multi-level vertical structure that rules out a "dictatorship V" artifact.

This inverts Burns & Stalker's (1961) prediction that organic structures fit turbulent environments, and directly challenges the popular "AI + volatility → flat organizations" argument.

---

## What this repository contains

```
org-design-thesis/
├── README.md                       ← you are here
├── LICENSE                         ← CC BY 4.0
├── AUDIT_CHECKLIST.md              ← independent verification steps (90–120 min)
├── paper/
│   ├── manuscript.md               ← full manuscript (~10k words, 8 figures)
│   ├── hypotheses.md               ← H1–H5 pre-registered statements
│   ├── proposal-en.md              ← initial proposal (superseded by manuscript)
│   └── proposal-ko.md              ← 초안 (한국어)
├── literature/
│   ├── literature-review.md
│   ├── theoretical-gap.md
│   └── references.bib
├── abm/                            ← agent-based model (Python 3.9+)
│   ├── nk_landscape.py             ← Kauffman (1993) NK fitness landscape
│   ├── agents.py, organizations.py ← V / H / Hy structure classes
│   ├── experiment.py               ← v1 static baseline
│   ├── experiment_v2.py            ← v2 static with fragmentation cost
│   ├── experiment_dynamic.py       ← fixed-shock dynamic
│   ├── experiment_volatility.py    ← ★ headline: 6-level volatility gradient
│   ├── experiment_densegrid.py     ← 15-level dense grid
│   ├── robustness.py               ← parameter sensitivity (frag-cost, n_agents, fine-τ)
│   ├── experiment_replication.py   ← 3-bank seed replication (Critique 1)
│   ├── experiment_shocks.py        ← 4 shock-model variants (Critique 2)
│   ├── experiment_multilevel.py    ← multi-level V / Burns-Stalker form (Critique 3)
│   ├── experiment_heterogeneous.py ← 4 talent-distribution regimes (Critique 5)
│   ├── bootstrap_analysis.py       ← 95% CIs + permutation tests
│   ├── visualize*.py               ← figure generation
│   ├── fill_manuscript.py          ← injects numeric results into manuscript.md
│   └── final_assembly.py           ← end-to-end pipeline driver
├── empirical/                      ← archival regression pipeline (pipeline-validation only)
│   ├── real_data/                  ← SEC EDGAR + yfinance panel build
│   ├── synthetic_data.py
│   ├── regression.py, did_template.py
│   └── README.md
├── results/                        ← all simulation outputs + figures
│   ├── results.csv                 ← v1 baseline (3,240 runs)
│   ├── results_v2.csv              ← v2 baseline (3,240 runs)
│   ├── results_dynamic.csv         ← fixed-shock (1,620 runs)
│   ├── results_volatility.csv     ← ★ headline gradient (4,860 runs)
│   ├── results_robustness.csv      ← param sensitivity (7,020 runs)
│   ├── results_replication.csv     ← 3-bank (4,860 runs)
│   ├── results_shocks.csv          ← alt shocks (6,480 runs)
│   ├── results_multilevel.csv      ← multi-level V (4,860 runs)
│   ├── results_heterogeneous.csv   ← heterogeneity (720 runs)
│   ├── bootstrap_summary.json      ← 95% CIs + slope + perm p
│   ├── figures/                    ← 8 PDF-embedded + auxiliary figures
│   └── report.md                   ← integrated findings report
└── submission/
    ├── manuscript.pdf              ← ★ canonical submission artifact
    ├── manuscript.html             ← web-readable version
    ├── report.pdf                  ← findings report
    ├── ssrn_metadata.txt           ← copy-paste fields for SSRN
    ├── arxiv_metadata.txt          ← copy-paste fields for arXiv (econ.GN)
    ├── COVER_LETTER_template.md
    ├── UPLOAD_GUIDE.md
    ├── FINAL_STATUS.md
    └── build_pdf.py                ← regenerates PDFs from markdown
```

---

## Reproducibility

All results are seed-fixed and bit-for-bit reproducible on the same NumPy version.

```bash
pip install -r abm/requirements.txt

# --- Baseline batteries ---
python abm/experiment.py                   # v1 static,    ~3 min
python abm/experiment_v2.py                # v2 static,    ~3 min
python abm/robustness.py                   # param sens,   ~15 min
python abm/experiment_dynamic.py           # fixed shock,  ~4 min
python abm/experiment_volatility.py        # ★ headline,   ~15 min

# --- Robustness extensions ---
python abm/experiment_replication.py       # 3-bank repl,  ~25 min
python abm/experiment_shocks.py            # alt shocks,   ~30 min
python abm/experiment_multilevel.py        # multi-level,  ~10 min
python abm/experiment_heterogeneous.py     # heterogen.,   ~7 min

# --- Assembly (figs + bootstrap + PDF) ---
python abm/final_assembly.py
```

Full replication: **~60–90 min** on a laptop (≈half that with the four extensions in parallel).

See [`AUDIT_CHECKLIST.md`](AUDIT_CHECKLIST.md) for step-by-step independent verification (6 mandatory steps, ~90–120 min).

---

## Reading order

1. [`paper/manuscript.md`](paper/manuscript.md) — the paper itself
2. [`results/report.md`](results/report.md) — integrated findings with all tables and figures
3. [`paper/hypotheses.md`](paper/hypotheses.md) — formal H1–H5 statements
4. [`literature/theoretical-gap.md`](literature/theoretical-gap.md) — why this matters
5. [`submission/FINAL_STATUS.md`](submission/FINAL_STATUS.md) — current status and limitations

---

## Transparency note

An earlier draft of this work claimed cluster-based hybrid dominance under environmental volatility. That claim resulted from a simulation bug: the dynamic-experiment hybrid branch delegated to a static-landscape helper and therefore did not receive landscape shocks while the V and H branches did. The bug was identified, fixed, experiments re-run, and the finding inverted. The corrected result is reported openly in the manuscript conclusion and in [`submission/FINAL_STATUS.md`](submission/FINAL_STATUS.md). The correction-culture discipline is why the final paper includes aggressive robustness verification.

---

## Suggested citation

```
Han, W. (2026). Volatility reverses the horizontal-organization advantage:
How environmental turbulence inverts the information-accessibility
prescription for organizational structure. Working paper.
```

- **SSRN:** [abstract 6634219](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6634219) (submitted 2026-04-23, under staff review)
- **Zenodo DOI:** [10.5281/zenodo.19707964](https://doi.org/10.5281/zenodo.19707964) (minted 2026-04-23 from v1.0 release)
- **ORCID:** [0009-0002-7528-2228](https://orcid.org/0009-0002-7528-2228)

---

## Contact

Wonpyo Han · `pk102h@naver.com` · ORCID [0009-0002-7528-2228](https://orcid.org/0009-0002-7528-2228)

Feedback, critique, and co-authorship inquiries welcome. Organization-theory expertise in framing/positioning for top-tier submission is the primary collaboration need.
