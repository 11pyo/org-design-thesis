# Upload Guide — submit the paper yourself in ~5 minutes

**⚠️ Claude cannot submit on your behalf.** Submission requires your account credentials, legal authorship attestation, and permanent public record — actions that must be taken by you. Below is everything pre-filled so you just copy, paste, and click.

---

## Choice of venue

| Venue | Cost | Speed | Commitment | Recommended |
|---|---|---|---|---|
| **SSRN** (Social Science Research Network) | Free | Instant | Low (can revise freely) | ✅ **Start here** — best for management-science pre-prints |
| **arXiv** (econ.GN / cs.CY) | Free | 1–2 business days (moderated) | Medium (versioned, DOI) | Option B — good for reproducibility-focused audiences |
| **GitHub** + `zenodo.org` DOI | Free | Instant | Low | Option C — pairs well with SSRN; gives code a DOI |
| **OSF** (Open Science Framework) | Free | Instant | Low | Option D — good for pre-registration |
| **Journal direct submission** (e.g. *Organization Science*) | Free–$100 | Months of review | **High** — blocked for revision during review | ⏸️ **Not yet.** Do after SSRN + co-author feedback |

**Recommendation:** Do SSRN + GitHub + Zenodo today. Add a co-author next month. Submit to *Organization Science* after the co-author revises with you.

---

## Step 1 — SSRN submission (~3 minutes)

1. Create account at [ssrn.com](https://ssrn.com/) if you don't have one.
2. Click **"Submit a Paper"** at top right.
3. Network: pick **Management Research Network (MRN)** → **Organization Theory eJournal** and **Organizational Behavior eJournal** (pick 2 networks).
4. Copy-paste the fields below.

### Fields — copy from `submission/ssrn_metadata.txt`:

See the `ssrn_metadata.txt` file in this folder. Key fields pre-filled:

- **Title**, **abstract** (300 words, within SSRN 1,875-char limit)
- **Keywords** (≤10)
- **JEL classification codes**
- **Affiliation** (you'll add yours)

5. Upload `manuscript.pdf` from this folder.
6. Confirm you are the author.
7. Click **Submit**.

---

## Step 2 — GitHub public repo + Zenodo DOI (~2 minutes)

1. Create a new **public** GitHub repository named `org-design-thesis`.
2. From this folder, in a shell:
   ```bash
   cd "E:/원표/한원표 비즈니스/프로그램 개발/new folder"
   git init
   git add .
   git commit -m "Initial release: research scaffolding v1"
   git remote add origin https://github.com/<your-username>/org-design-thesis.git
   git branch -M main
   git push -u origin main
   ```
3. At [zenodo.org](https://zenodo.org/), log in with GitHub → enable the repo → cut a GitHub release (tag v0.1). Zenodo will auto-assign a DOI.
4. Paste the DOI into your SSRN submission (edit → add DOI under Links).

---

## Step 3 — arXiv (optional, ~10 minutes)

Only do this if you want an arXiv DOI in addition to Zenodo.

1. Register at [arxiv.org](https://arxiv.org/user/register) if new. Needs endorsement if this is your first arXiv paper in a given category — not blocking, but plan for 1–2 business days.
2. Category: **econ.GN** (General Economics) and **cross-list cs.CY** (Computers and Society).
3. Upload `manuscript.pdf` plus the `references.bib` and `manuscript.tex` (if you've converted) from this folder.
4. Copy-paste metadata from `submission/arxiv_metadata.txt`.

---

## Step 4 — OSF pre-registration (strongly recommended)

Pre-registering your predictions *before* you run the real-data analysis on an expanded sample is a requested best-practice. It also raises acceptance odds at journals that reward pre-registration (e.g. *Organizational Research Methods*, *Strategic Management Journal* under certain editors).

1. Go to [osf.io](https://osf.io/), create an account.
2. New Project → name `org-design-thesis-prereg`.
3. Click **"Register"** → **"OSF Preregistration"** template.
4. Paste the hypotheses H1–H4 from `paper/hypotheses.md`.
5. State the estimand (flat × τ interaction coefficient), data, and exclusion criteria.
6. Submit — timestamp is now immutable.

---

## Step 5 — LinkedIn / Twitter / personal blog announcement (optional)

If you want reach beyond the academic audience. Keep it crisp:

> **"When does horizontal beat vertical? A boundary-condition study of organizational structure in the AI era."**
> Pre-print + ABM + regression on SEC 10-K data. Free code and data. Would love feedback from anyone working in organization design, self-management, or computational management science.
> [SSRN link] [GitHub link]

---

## What NOT to do yet

- ❌ **Don't submit to a journal (*Organization Science*, *SMJ*) yet.** The scaffolding is defensible but one- to two-author review passes first will save you a desk reject.
- ❌ **Don't post full Holacracy takes on LinkedIn** until the real-data Phase 2 is finalized. The framing "it's conditional on τ" is subtle; premature pop-sci framings will bite you on reviewer reads.
- ❌ **Don't start a Reddit/HackerNews discussion** until you have a co-author and a stable story. The comment threads there will dominate your Google presence for the paper forever.

---

## After submission — next steps

1. **Find a co-author.** One email to an organization-theory professor whose recent papers cite Csaszar or Bernstein. Lead with: "I have a working paper on a conditional boundary between horizontal and vertical org structures, with ABM + archival evidence. Would you consider a read?"
2. **Iterate the ABM** with a calibrated NK using industry-level ruggedness from real patent-citation data (USPTO bulk once you have access).
3. **Expand the archival sample** to Russell 3000 for power on H4.
4. **Present at a workshop** — SMS special conference, AOM OMT division poster session, Wharton People Analytics Conference. The feedback will be worth more than three rounds of peer review.

Total estimated calendar time from today to a submission-ready *Organization Science* draft: **4–6 months** with one co-author and the Path A infrastructure already built.
