# arXiv endorsement request — template

> Draft email to send after registering on arXiv and attempting first submission.
> arXiv will issue you a **6-character endorsement code** at that point; paste it into the `{{ENDORSEMENT_CODE}}` slot below.

---

## Who to ask (priority order)

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

## Email template

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

    {{ENDORSEMENT_CODE}}

If you judge the paper to meet the scholarly standard for econ.GN and
you are willing to endorse, the one-click process is at:
https://arxiv.org/auth/need-endorsement

You would enter the endorsement code above and my email
(pk102h@naver.com). The endorsement does not imply agreement with
the paper's claims — only that it is a legitimate scholarly submission.

If this isn't a fit, a one-line "not for me" is entirely fine. Thank
you in advance for considering.

With thanks,
Wonpyo Han
ORCID 0009-0002-7528-2228
pk102h@naver.com
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
