"""
Re-extract flat and K_rd proxies from existing downloaded 10-Ks using
improved regex patterns. Faster — reads checkpoint for filing paths,
re-processes only the text extraction stage.
"""
from __future__ import annotations
import re, sys
from pathlib import Path
import pandas as pd

HERE = Path(__file__).parent

_SCRIPT_STYLE_RE = re.compile(r"<(script|style|noscript|head)[^>]*>.*?</\1>", re.DOTALL | re.IGNORECASE)
_TAG_RE = re.compile(r"<[^>]+>")
_WS_RE = re.compile(r"\s+")
_ENTITY_RE = re.compile(r"&(?:nbsp|amp|lt|gt|quot|apos|#\d+|#x[0-9a-fA-F]+);")

EXEC_START_RE = re.compile(
    r"(information about our executive officers|executive officers of the registrant|executive officers of [a-z]+|our executive officers|executive officers)",
    re.IGNORECASE,
)

OFFICER_ROW_RE = re.compile(
    r"""
    [A-Z][A-Za-z\.\-']{1,20}                              # first name
    (?:\s+[A-Z][A-Za-z\.\-']{1,20})?                      # optional middle
    (?:\s+[A-Z][A-Za-z\.\-']{1,20})?                      # optional middle 2
    \s+[A-Z][A-Za-z\-']{1,25}(?:,\s*(?:Jr|Sr|III|II|IV)\.?)?  # last name
    ,\s*
    (\d{2})                                               # age
    \s                                                    # terminator
    """, re.VERBOSE,
)

RD_RE = re.compile(
    r"research\s+and\s+development\s+expenses?\s*(?:of|were|was|totaled|amounted\s+to)?\s*(?:approximately\s+)?\$?\s*([\d,]+\.?\d*)\s*(million|billion|thousand)?",
    re.IGNORECASE,
)
REV_RE = re.compile(
    r"(?:total\s+revenues?|net\s+revenues?|total\s+net\s+revenues?|net\s+sales)\s*(?:of|were|was|totaled|amounted\s+to|reached)?\s*(?:approximately\s+)?\$?\s*([\d,]+\.?\d*)\s*(million|billion)?",
    re.IGNORECASE,
)

TAU_KEYWORDS = [
    "data-driven", "data driven", "analytics", "artificial intelligence",
    "machine learning", "ai-enabled", "ai enabled", "dashboard",
    "real-time", "real time", "cloud-based", "cloud based",
    "automation", "digital transformation", "internet of things",
    "predictive", "self-service", "self service", "api",
]


def clean_text(html: str) -> str:
    html = _SCRIPT_STYLE_RE.sub(" ", html)
    t = _TAG_RE.sub(" ", html)
    t = _ENTITY_RE.sub(" ", t)
    t = _WS_RE.sub(" ", t)
    return t


def extract_n_officers(text: str) -> int:
    """Count distinct name+age pattern matches across the filing.
    Relies on the 10-K canonical executive-officer listing format:
       "Name[, Middle] Last, ## ...".
    We take the full-text count, because section-bounding is brittle
    (exec-officer headings appear in TOC as well as in the body).
    Range-filter to plausible officer ages [30, 80]."""
    matches = OFFICER_ROW_RE.findall(text)
    ages = [int(a) for a in matches if 30 <= int(a) <= 80]
    if len(ages) == 0:
        loose = re.compile(r"[A-Z][a-zA-Z\.\-']+,\s*(\d{2})\s")
        ages = [int(a) for a in loose.findall(text) if 30 <= int(a) <= 80]
    return min(len(ages), 40)


def extract_rd_rev(text: str) -> tuple[float, float]:
    text_l = text.lower().replace(",", "")
    rd_m = RD_RE.search(text_l)
    rev_m = REV_RE.search(text_l)
    def _val(m):
        if not m: return float("nan")
        try:
            v = float(m.group(1))
        except Exception:
            return float("nan")
        unit = (m.group(2) or "").lower()
        if "billion" in unit: v *= 1000
        elif "thousand" in unit: v /= 1000
        return v
    return _val(rd_m), _val(rev_m)


def keyword_freq(text: str) -> int:
    tl = text.lower()
    return sum(tl.count(kw) for kw in TAU_KEYWORDS)


def parse_one(path: str) -> dict:
    try:
        html = Path(path).read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        return {"error": str(e)[:80]}
    text = clean_text(html)
    words = len(text.split())
    n_exec = extract_n_officers(text)
    rd, rev = extract_rd_rev(text)
    kw = keyword_freq(text)
    tau_raw = (kw / max(1, words)) * 10_000
    flat = 1.0 / (1.0 + max(0, n_exec)) if n_exec > 0 else float("nan")
    K_rd = (rd / rev) if (rev == rev and rev > 0 and rd == rd and rd > 0) else float("nan")
    if K_rd == K_rd and (K_rd > 0.8 or K_rd < 0):
        K_rd = float("nan")
    return {
        "doc_wordcount": words,
        "n_exec_officers": n_exec,
        "flat": flat,
        "tau_raw": tau_raw,
        "K_rd": K_rd,
        "rd_reported": rd,
        "rev_reported": rev,
        "keywords_total": kw,
    }


def main():
    idx = pd.read_csv(HERE / "filings_index.csv", dtype={"cik": str})
    print(f"Parsing {len(idx)} filings with improved regex...", flush=True)
    rows = []
    for i, r in idx.iterrows():
        parsed = parse_one(r["path"])
        rows.append({**r.to_dict(), **parsed})
        if (i + 1) % 50 == 0:
            print(f"  {i+1}/{len(idx)}", flush=True)
    out = pd.DataFrame(rows)
    out.to_csv(HERE / "firm_year_panel.csv", index=False)
    print(f"Wrote firm_year_panel.csv: {len(out)} rows", flush=True)
    keep = out.dropna(subset=["flat"])
    print(f"With flat: {len(keep)}", flush=True)
    if len(keep) > 0:
        print(keep[["flat","tau_raw","K_rd","n_exec_officers","doc_wordcount"]].describe().round(3), flush=True)


if __name__ == "__main__":
    main()
