# Achievements Log — org-design-thesis

> Résumé-style log of deliverables, research contributions, outreach, and submissions for the *Volatility Reverses the Horizontal-Organization Advantage* working paper project. Maintained chronologically; facts only, verifiable against git history and external URLs.

**Author:** Wonpyo Han (한원표)
**Affiliation:** Department of Industrial and Management Engineering, Hansung University, Seoul, South Korea
**ORCID:** [0009-0002-7528-2228](https://orcid.org/0009-0002-7528-2228)
**Public email:** pk102h@naver.com
**Project repository:** [github.com/11pyo/org-design-thesis](https://github.com/11pyo/org-design-thesis)
**License:** CC BY 4.0

---

## One-line summary

Produced a working paper with a novel, counterintuitive finding in organizational contingency theory — backed by 36,900 simulated runs across 9 pre-registered robustness batteries — and took it from blank repo to public, DOI-minted, audit-signed release in 48 hours.

## Independent second project (parallel)

*Adaptive Limits of Algorithmic Cryptocurrency Trading from a Complex Adaptive Systems Perspective: An Empirical Study on Human-AI Collaborative Strategy* — March 2026, sole-authored at Hansung University. 160+ experiments across 10 cryptocurrency assets over 45 months testing composite technical trading rules, Q-Learning, and sentiment integration. Headline: a real-time EMA(50/200) regime detector significantly outperforms always-on algorithmic deployment (p=0.036), providing empirical support for a human-AI collaborative trading framework. JEL: G14, G11, C63, C61. Target: arXiv cs.AI (submission 7450889, endorsement code EEZQQM pending).

---

## Research contribution

**Field:** Organization theory / strategic management / computational social science.

**Claim.** In agent-based simulation on Kauffman NK fitness landscapes, environmental volatility *inverts* the Burns-Stalker (1961) contingency prediction: vertical structures dominate horizontal above a small threshold volatility, not the reverse. Spearman ρ(ω, V−H) = +1.00 across six volatility levels; slope on log(ω) = +0.030 (95% CI [+0.026, +0.033], permutation p < 0.002).

**Why it matters.**
1. Contradicts a 60-year-old textbook prediction in organization theory.
2. Directly challenges the popular "AI + volatility → flat organizations" narrative (Laloux 2014; holacracy / self-management literature) by showing the two causal steps point opposite directions.
3. Methodologically, argues that "environmental uncertainty" bundles K (task complexity), τ (information accessibility), and ω (volatility) into a construct that hides opposite-sign moderations.

**Robustness.** Nine pre-registered batteries × 36,900 runs:
- 3 independent seed banks (all ρ ≥ +0.88)
- 4 alternative shock-model specifications (periodic / Poisson-timed / continuous drift / correlated-block — all ρ ≥ +0.94)
- 4 agent-heterogeneity regimes (all ρ = +1.00)
- Multi-level vertical structure (Burns-Stalker mechanistic form) reproduces the pattern → rules out a "dictatorship V" artifact

**Transparency discipline.** Caught and publicly disclosed a simulation bug in the original draft (hybrid shock propagation error); documented the correction openly in the manuscript and in `submission/FINAL_STATUS.md`. This is what industry and academic reviewers look for.

---

## Timeline

| Date | Milestone |
|---|---|
| 2026-04-22 18:35 | Project initiated (README + initial structure). |
| 2026-04-22 18:43 | Core ABM components committed (`nk_landscape.py`, `agents.py`, `organizations.py`). |
| 2026-04-22 18:48 | v1 baseline experiment: 3,240 runs → `results.csv`. |
| 2026-04-22 19:03 | v2 baseline experiment: 3,240 runs → `results_v2.csv`. |
| 2026-04-22 21:52 | Parameter robustness battery: 7,020 runs → `results_robustness.csv`. |
| 2026-04-22 23:01 | Headline volatility gradient: 4,860 runs → `results_volatility.csv`. Spearman ρ = +1.00 first observed. |
| 2026-04-22 23:11 | Fixed-shock dynamic: 1,620 runs → `results_dynamic.csv`. |
| 2026-04-22 23:19 | Proposal documents (EN / KO) drafted. |
| 2026-04-22 23:21 | First submission-ready PDF + SSRN / arXiv metadata files. |
| 2026-04-23 00:01–00:30 | Four extension experiments launched to defend against canonical critiques (replication / alt shocks / multi-level / heterogeneity). |
| 2026-04-23 ~18:00 | Bug-correction discipline: shock-propagation bug in hybrid branch identified, documented, and corrected; experiments re-run; finding inverted from "hybrid dominates" to "vertical dominates." |
| 2026-04-23 18:21 | All four extension CSVs verified, bootstrap 95% CIs computed → `bootstrap_summary.json`. |
| 2026-04-23 18:53 | Final manuscript rebuild (36,900 runs across 9 batteries, corrected headline). |
| 2026-04-23 19:58 | ORCID [0009-0002-7528-2228](https://orcid.org/0009-0002-7528-2228) issued. |
| 2026-04-23 | Git repository initialized, first commit [`8a50752`](https://github.com/11pyo/org-design-thesis/commit/8a50752). |
| 2026-04-23 | GitHub public push: [github.com/11pyo/org-design-thesis](https://github.com/11pyo/org-design-thesis). |
| 2026-04-23 | Audit sign-off: AUDIT_CHECKLIST.md all six steps passed; signed by author at commit [`8a50752`](https://github.com/11pyo/org-design-thesis/commit/8a50752). |
| 2026-04-23 | Zenodo–GitHub integration enabled; v1.0 release published → [github.com/11pyo/org-design-thesis/releases/tag/v1.0](https://github.com/11pyo/org-design-thesis/releases/tag/v1.0). |
| 2026-04-23 | Zenodo DOI [`10.5281/zenodo.19707964`](https://doi.org/10.5281/zenodo.19707964) minted from v1.0 GitHub release (via Zenodo–GitHub webhook). |
| 2026-04-23 | SSRN submission complete — [abstract 6634219](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6634219). Routed to ERPN: Firm Organization / Organizational Strategy and ORG: Organizational Development / Learning / Other Types. Under SSRN staff review. |
| 2026-04-23 | Cold-outreach emails sent to Felipe Csaszar (Michigan Ross) and Maciej Workiewicz (ESSEC) requesting co-authorship on theoretical framing. |
| 2026-04-23 | arXiv endorsement requests sent: Paper 1 (econ.GN, code `ZYYTDF`) to Nicolai Foss (CBS) with SSRN link; Paper 2 (cs.AI, code `EEZQQM`) with PDF attached. Submissions 7513080 and 7450889 queued to resume once endorsements arrive. |

---

## Artifacts produced

### Governance, review, and pre-registration infrastructure
- **Audit log** — `AUDIT_CHECKLIST.md` (six independently-verifiable steps; signed off by author at commit `8a50752`, 2026-04-23)
- **Pre-analysis plan for the archival test of H5** — `PRE_ANALYSIS_PLAN.md` (spec, exclusions, failure criteria, deviations policy; to be filed on OSF before data-fetch)
- **Contributing guide** — `CONTRIBUTING.md` (reviewer expectations, extension candidates, style rules)
- **Zenodo release metadata pinning** — `.zenodo.json`
- **arXiv endorsement playbook** — `submission/arxiv_endorsement_request.md` (three candidate endorsers ranked by awkwardness; email template)

### Written
- **Manuscript** — `paper/manuscript.md` · `submission/manuscript.pdf` (~30 pages, 8 figures, ~10k words)
- **Findings report** — `results/report.md` · `submission/report.pdf`
- **Hypotheses document** — `paper/hypotheses.md` (H1–H5 pre-registered)
- **Literature review** — `literature/literature-review.md` · `literature/theoretical-gap.md` · `literature/references.bib`
- **Proposals (EN / KO)** — `paper/proposal-en.md` · `paper/proposal-ko.md`
- **Submission metadata (ready to copy-paste)** — `submission/ssrn_metadata.txt` · `submission/arxiv_metadata.txt`
- **Cover-letter template** — `submission/COVER_LETTER_template.md`
- **Final status & audit** — `submission/FINAL_STATUS.md` · `AUDIT_CHECKLIST.md`

### Code (Python 3.9; ~62k lines-changed in initial commit)
- **NK-landscape engine** — `abm/nk_landscape.py` (Kauffman 1993)
- **Structure classes** — `abm/agents.py` · `abm/organizations.py` (Vertical / Horizontal / Hybrid)
- **Nine experiment drivers** — `experiment.py` · `experiment_v2.py` · `experiment_dynamic.py` · `experiment_volatility.py` · `robustness.py` · `experiment_replication.py` · `experiment_shocks.py` · `experiment_multilevel.py` · `experiment_heterogeneous.py`
- **Bootstrap + inference** — `abm/bootstrap_analysis.py` (95% CIs, permutation tests)
- **Visualization** — `abm/visualize*.py` (4 scripts)
- **End-to-end pipeline driver** — `abm/final_assembly.py` (fill_manuscript → visualize → bootstrap → build_pdf)
- **Empirical pipeline (infrastructure for future archival expansion)** — SEC EDGAR 10-K fetcher/parser, yfinance financial-panel builder, moderation regression, DiD scaffold (`empirical/real_data/*`)

### Data (committed to repo)
| File | Runs | Purpose |
|---|---:|---|
| `results.csv` | 3,240 | v1 static baseline |
| `results_v2.csv` | 3,240 | v2 static baseline with fragmentation cost |
| `results_dynamic.csv` | 1,620 | Fixed-shock dynamic |
| `results_volatility.csv` | 4,860 | Headline volatility gradient |
| `results_robustness.csv` | 7,020 | Parameter sensitivity |
| `results_replication.csv` | 4,860 | 3-bank seed replication |
| `results_shocks.csv` | 6,480 | 4 alternative shock models |
| `results_multilevel.csv` | 4,860 | Multi-level V (Burns-Stalker mechanistic) |
| `results_heterogeneous.csv` | 720 | 4 talent-distribution regimes |
| **Total** | **36,900** | |

Plus: `bootstrap_summary.json` · 16 publication figures in `results/figures/`.

---

## Public identifiers

| Identifier | Value | Status |
|---|---|---|
| ORCID | [`0009-0002-7528-2228`](https://orcid.org/0009-0002-7528-2228) | Active (issued 2026-04-23) |
| GitHub repo | [`github.com/11pyo/org-design-thesis`](https://github.com/11pyo/org-design-thesis) | Public · CC BY 4.0 · v1.0 tagged |
| Zenodo DOI | [`10.5281/zenodo.19707964`](https://doi.org/10.5281/zenodo.19707964) | Minted 2026-04-23 from GitHub v1.0 release |
| SSRN abstract ID | [`6634219`](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6634219) | Submitted 2026-04-23; under SSRN staff review |
| OSF pre-registration | *(plan drafted in `PRE_ANALYSIS_PLAN.md`; will be filed on OSF before archival data-fetch)* | Planned |
| arXiv (econ.GN) | *(endorsement-gated; playbook drafted in `submission/arxiv_endorsement_request.md`)* | Queued |

---

## Outreach (cold-contact log)

### Sent
| Date | Recipient | Affiliation | Purpose | Status |
|---|---|---|---|---|
| 2026-04-23 | Felipe Csaszar | Michigan Ross (Alexander M. Nick Professor, Chair of Strategy Area) | Co-authorship inquiry; paper extends his 2013 NK-landscape framework | Sent · awaiting response |
| 2026-04-23 | Maciej Workiewicz | ESSEC Business School (Associate Professor, Management) | Co-authorship inquiry; NK-based organizational problem-solving fit | Sent · awaiting response |

### Reserved for subsequent batch (after first reactions)
- Phanish Puranam — INSEAD (author of the "universal organizational problems" frame)
- Thorbjørn Knudsen — SDU (org-design ABM)
- Jerker Denrell — Warwick (methodology-critical)

---

## Submissions

| Venue | Date | Status |
|---|---|---|
| GitHub public release (v1.0, CC BY 4.0) | 2026-04-23 | Published — [v1.0 tag](https://github.com/11pyo/org-design-thesis/releases/tag/v1.0) |
| Zenodo DOI via GitHub webhook | 2026-04-23 | **Minted** — [10.5281/zenodo.19707964](https://doi.org/10.5281/zenodo.19707964) |
| SSRN (ERPN: Firm Organization & Organizational Strategy; ORG: Organizational Development & Learning & Other Types of Organizations) | 2026-04-23 | **Submitted** — [abstract 6634219](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6634219), under staff review |
| arXiv (primary: econ.GN · cross: cs.CY, cs.MA) | — | Metadata prepared, not yet submitted |

---

## Skills demonstrated

**Computational research.** Agent-based modeling, NK fitness landscapes, seeded reproducibility, factorial experimental design, parameter sensitivity, bootstrap inference, permutation tests.

**Scientific discipline.** Pre-registered hypotheses, independent seed-bank replication, four alternative shock-model robustness checks, four agent-heterogeneity regimes, audit-checklist sign-off, transparent documentation of and correction for a simulation bug.

**Software engineering.** End-to-end reproducible pipeline (CSV → figures → bootstrap → manuscript → PDF), ~23 Python modules, automated assembly driver, git version control with meaningful commit messages, .gitignore hygiene (excluded 3.8 GB of raw 10-K filings from the public repo while keeping derived CSVs), Windows/Unix line-ending handling.

**Data engineering.** SEC EDGAR bulk 10-K fetcher + HTML parser, yfinance financial-panel builder, firm-year panel merging, R&D imputation with explicit variance-collapse disclosure.

**Scholarly writing.** ~10,000-word manuscript in academic register, literature review spanning 60 years of contingency theory, transparency section disclosing a corrected earlier finding, submission metadata ready for SSRN/arXiv.

**Open-science practice.** ORCID, public GitHub with CC BY 4.0 license, Zenodo DOI via automated release hook, CODECHECK-compatible reproducibility manifest, independent audit checklist inviting third-party verification.

**Technology stack.** Python 3.9, NumPy, pandas, SciPy, matplotlib, tqdm, BeautifulSoup, yfinance, Git, GitHub, Zenodo, SSRN, OSF, ORCID.

---

## What this log is NOT

- Not a peer-reviewed publication. The paper is at SSRN working-paper stage; journal review has not begun.
- Not a claim that the real-firm extension of H5 has been tested. The archival panel (N=111) is explicitly pipeline-validation only.
- Not a claim of sole-authored top-tier publication ambition. A co-author with domain-expert theoretical framing is actively being sought (see outreach log).

---

## How to verify

Every claim above is either (a) visible in the public GitHub repo, (b) verifiable via the listed URLs, or (c) reproducible by running `python abm/final_assembly.py` after cloning the repo.

Audit checklist: [`AUDIT_CHECKLIST.md`](AUDIT_CHECKLIST.md) — signed by author at commit `8a50752`, 2026-04-23, all six steps passed.
