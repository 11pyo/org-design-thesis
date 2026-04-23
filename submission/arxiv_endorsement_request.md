# arXiv endorsement requests — two parallel papers

> **Author profile:** Wonpyo Han, Department of Industrial and Management Engineering, Hansung University, Seoul, South Korea · ORCID 0009-0002-7528-2228 · pk102h@naver.com

| Paper | arXiv submission | Category | Endorsement code |
|---|---|---|---|
| **Paper 1** — *Volatility Reverses the Horizontal-Organization Advantage* | 7513080 | **econ.GN** | **`ZYYTDF`** |
| **Paper 2** — *Adaptive Limits of Algorithmic Cryptocurrency Trading* | 7450889 | **cs.AI** | **`EEZQQM`** |

Each category needs its own endorser. A single endorsement unlocks *all future submissions in that category* but does not transfer between categories.

## arXiv's endorser qualification rule

An endorser for **econ.GN** must have **submitted ≥ 3 papers to econ.EM / econ.GN / econ.TH** with the earliest between **3 months and 5 years ago**. Most strategy / organization-theory researchers use SSRN, not arXiv, so not everyone we'd naturally ask will qualify. The email template below includes a polite out-clause ("if you don't meet that criterion, a recommendation would be appreciated") so non-qualifying candidates can redirect us instead of ghosting.

**How to pre-check a candidate** (10 seconds each): open any of their papers on arxiv.org; scroll to the abstract-page bottom; click "Which of the authors of this article can endorse?" — if the candidate's name appears, they qualify for the relevant category.

---

---

## PAPER 1 — econ.GN endorsement (`ZYYTDF`)

### Who to ask (priority order)

All three below regularly publish to `econ.GN` and handle organizational-design / firm-level computational work. Odds of response are broadly similar; pick one, send, wait 48–72 h, move to the next if no reply.

### 1. Phanish Puranam (INSEAD)
- Email: `phanish.puranam@insead.edu`
- Why: author of the "universal organizational problems" frame cited in our paper; actively uses ABM; has posted to `econ.GN`.
- Risk: also on our reserved co-authorship list, so the endorsement ask may read as overlapping. Keep this ask strictly about endorsement (do *not* mention co-authorship in the endorsement email).

### 2. Nicolai J. Foss (Copenhagen Business School)
- Email: `njf.si@cbs.dk`
- Why: cited in our paper (wrote the canonical Oticon-spaghetti-organization account, Foss 2003); strong `econ.GN` presence via TMR / strategy papers.
- Risk: lowest — he's not on our co-authorship list, so endorsement is an uncomplicated ask.

### 3. Sendil Ethiraj (London Business School)
- Email: `sethiraj@london.edu`
- Why: NK-landscape organizational-design work; responsive to unaffiliated researchers; frequent arXiv / SSRN poster.
- Risk: low; he's not in our cold-email queue.

**Recommendation:** email **Foss first** (lowest awkwardness), then Ethiraj, then Puranam.

---

### Email template (econ.GN, Paper 1)

```
Subject: arXiv endorsement request — econ.GN — NK-landscape paper

Dear Professor {{Foss | Ethiraj | Puranam}},

I'm an independent researcher seeking arXiv endorsement for a first
submission to the econ.GN category.

The paper ("Volatility Reverses the Horizontal-Organization Advantage")
is an NK-landscape ABM study of organizational contingency theory
under environmental volatility. 36,900 simulated runs across nine
pre-registered robustness batteries; headline Spearman ρ(ω, V−H) = +1.00
with slope +0.030 on log(ω) (95% CI [+0.026, +0.033], permutation
p < 0.002). Result inverts the Burns-Stalker prediction: vertical
dominates horizontal above a small threshold volatility.

Full artifact available for your review:
- SSRN abstract: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6634219
- Code + data (CC BY 4.0, Zenodo DOI): https://doi.org/10.5281/zenodo.19707964
- GitHub: https://github.com/11pyo/org-design-thesis
- Audit checklist (6 independently-verifiable steps, all signed off):
  https://github.com/11pyo/org-design-thesis/blob/main/AUDIT_CHECKLIST.md

arXiv gave me the following endorsement code:

    ZYYTDF

If you judge the paper to meet the scholarly standard for econ.GN and
you are willing to endorse, the one-click process is at:
https://arxiv.org/auth/endorse

(arXiv requires endorsers to have submitted >= 3 papers to econ.EM /
econ.GN / econ.TH between 3 months and 5 years ago. If you don't meet
that specific criterion, a one-line recommendation of someone who does
would be enormously helpful.)

You would enter the endorsement code above and my email
(pk102h@naver.com). The endorsement does not imply agreement with
the paper's claims — only that it is a legitimate scholarly submission.

If this isn't a fit, a one-line "not for me" is entirely fine. Thank
you in advance for considering.

With thanks,
Wonpyo Han
Department of Industrial and Management Engineering, Hansung University
ORCID 0009-0002-7528-2228 · pk102h@naver.com
```

---

## PAPER 2 — cs.AI endorsement (`EEZQQM`)

### Best candidate: a Hansung University faculty member

arXiv explicitly recommends asking your thesis advisor or a department professor. A Hansung Industrial and Management Engineering faculty member who has submitted ≥ 3 papers to any cs.* category within the last 5 years (but not within the last 3 months) is the ideal endorser — personal relationship lowers the ask, and the qualification check is simple.

**Action step:** ask the user to list 1–3 Hansung professors whose research touches AI, ML, computational finance, or algorithmic trading. Then check each person's most recent paper on arxiv.org — at the bottom of any abstract page, "Which of the authors of this article can endorse?" lists whether they qualify for cs.AI specifically.

### Backup candidates (if no Hansung prof qualifies)

Active cs.AI endorsers in Korea with related research interests:
- **Jaewoo Kang** (Korea University, AI/NLP) — prolific cs.AI poster
- **Jong-Hwan Kim** (KAIST, robotics/AI)
- **Sungroh Yoon** (Seoul National University, ML/AI)
- **Kibok Lee** (Yonsei, ML) — mid-career, higher response rate

### Email template (cs.AI, Paper 2)

```
Subject: arXiv endorsement request — cs.AI — algorithmic trading / complex adaptive systems paper

Dear Professor {{Name}},

I'm a researcher at the Department of Industrial and Management
Engineering, Hansung University, seeking arXiv endorsement for a
first submission to the cs.AI category.

The paper ("Adaptive Limits of Algorithmic Cryptocurrency Trading
from a Complex Adaptive Systems Perspective") is an empirical study
of why composite technical trading algorithms struggle in
cryptocurrency markets. 160+ backtesting experiments across 10
cryptocurrency assets and 45 months, with six complementary analyses
(walk-forward cross-validation, Q-Learning reinforcement learning,
sentiment integration, outlier robustness, fee sensitivity, and a
real-time regime detection test that eliminates retrospective bias).

The headline finding: a simple real-time EMA(50/200) regime detector
that activates the trading algorithm only during detected downtrends
significantly outperforms always-on deployment (p=0.036), providing
empirical support for a human-AI collaborative trading framework that
does not rely on hindsight.

Full manuscript on SSRN (submitted 2026-03-27, under staff review):
https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6477100

arXiv gave me the following endorsement code:

    EEZQQM

If you judge the paper to meet the cs.AI scholarly standard and you
are willing to endorse, the one-click process is at:
https://arxiv.org/auth/endorse

(arXiv requires endorsers to have submitted >= 3 papers to any cs.*
category between 3 months and 5 years ago. If you don't meet that
specific criterion, a one-line recommendation of someone who does
would be enormously helpful.)

With thanks,
Wonpyo Han
Department of Industrial and Management Engineering, Hansung University
ORCID 0009-0002-7528-2228 · pk102h@naver.com
```

---

## After endorsement is granted

1. Endorser clicks the link, enters the code + your email, confirms.
2. arXiv notifies you by email.
3. Return to your arXiv submission draft; the blocked submission can now proceed.
4. Paste `submission/arxiv_metadata.txt` fields into the arXiv submission form.
5. Upload `submission/manuscript.pdf`.
6. Submit.

---

## Known expected timeline

- Endorsement request → reply: 24–72 hours typical.
- arXiv moderation after submit: 1–2 business days.
- First appearance in econ.GN listings: next business day after acceptance (typically 20:00 UTC).

If all three candidates decline or don't respond within a week, alternatives to consider: Felix Creutzig (econ.GN regular), Dirk Bergemann (Yale, economics of information), or posting to the arXiv public moderators list for manual review.
