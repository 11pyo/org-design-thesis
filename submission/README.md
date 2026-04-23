# Submission package

This folder contains everything you need to submit the paper. **Claude cannot submit for you — all uploads require your account credentials and legal authorship attestation.** Below, each file is ready to use.

## Files in this folder

| File | Purpose | When to use |
|---|---|---|
| `UPLOAD_GUIDE.md` | Step-by-step instructions for each venue | Read first |
| `manuscript.md` / `manuscript.html` / `manuscript.pdf` | The paper itself (3 formats) | Upload the PDF to SSRN/arXiv |
| `report.md` / `report.html` / `report.pdf` | Integrated results write-up | Reference supplement |
| `ssrn_metadata.txt` | Copy-paste fields for SSRN submission form | During SSRN submission |
| `arxiv_metadata.txt` | Copy-paste fields for arXiv submission form | During arXiv submission |
| `COVER_LETTER_template.md` | Journal cover letter (NOT for preprints) | Only for Organization Science / SMJ / ASQ |
| `build_pdf.py` | Regenerate PDFs from Markdown if manuscript changes | After editing manuscript.md |

## Recommended order of operations

1. Read `UPLOAD_GUIDE.md`
2. Quick scan of `manuscript.pdf` — read the abstract, Introduction (§1), and Conclusion (§7) to make sure the claims are ones you're willing to put your name on
3. If yes → upload to SSRN using `ssrn_metadata.txt` (3 minutes)
4. Create GitHub public repo of the entire project folder (2 minutes)
5. Enable Zenodo on the GitHub repo; cut a release; copy the DOI
6. (Optional) Upload to arXiv using `arxiv_metadata.txt` — requires endorsement if first submission in econ.GN
7. (Recommended) Pre-register on OSF before running real-data analysis on expanded sample
8. DO NOT submit to a journal yet — find a co-author first

## Things I did NOT do

- Submit anywhere (cannot authenticate as you)
- Create your ORCID (takes 2 minutes at orcid.org)
- Create your GitHub repo (I only prepared the local contents)
- Attach any real-name affiliation (I left those fields blank for you)

## If you change the manuscript

Edit `paper/manuscript.md` in the parent folder, then:

```bash
cd submission
python build_pdf.py
```

PDFs regenerate in a few seconds. Chrome/Edge headless is used under the hood.

## Caveats

The manuscript currently contains placeholders where real-data results go (marked "TBD"). Claude ran the real-data pipeline but the regression results are being finalized as of this packaging. If you see TBD entries, check `results/report.md` for the latest numbers and update the manuscript before uploading.
