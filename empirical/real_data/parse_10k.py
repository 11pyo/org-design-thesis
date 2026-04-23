"""
Parse downloaded 10-Ks to extract:

- flat      : organizational flatness proxy
              Currently: 1 / (1 + n_executive_officers_named)
              (Rajan-Wulf approach: more separately-named officers reporting
              to CEO = broader span = flatter. Inverse count gives
              compact [0,1] score where larger = flatter.)
- tau       : information-accessibility proxy
              keyword frequency in the 10-K narrative. Normalised per
              10,000 words.
- K_rd      : task complexity proxy
              R&D expense as fraction of revenue, Winsorized.

Output: real_data/firm_year_panel.csv with columns:
  cik, symbol, sector, year, flat, tau_raw, K_rd, n_exec_officers,
  doc_wordcount
"""

from __future__ import annotations
import os, re, json, sys
from pathlib import Path
import pandas as pd

HERE = Path(__file__).parent
FILINGS = HERE / "filings"
INDEX = HERE / "filings_index.csv"

TAU_KEYWORDS = [
    "data-driven", "data driven", "analytics", "artificial intelligence",
    "machine learning", "ai-enabled", "ai enabled", "dashboard",
    "real-time", "real time", "cloud-based", "cloud based",
    "automation", "digital transformation", "internet of things",
    "predictive", "self-service", "self service", "api",
]
EXEC_SECTION_HEADINGS = [
    r"executive officers of the registrant",
    r"information about our executive officers",
    r"our executive officers",
    r"executive officers",
]


_SCRIPT_STYLE_RE = re.compile(
    r"<(script|style|noscript|head)[^>]*>.*?</\1>",
    re.DOTALL | re.IGNORECASE,
)
_TAG_RE = re.compile(r"<[^>]+>")
_WS_RE = re.compile(r"\s+")
_ENTITY_RE = re.compile(r"&(?:nbsp|amp|lt|gt|quot|apos|#\d+|#x[0-9a-fA-F]+);")


def clean_text(html: str) -> str:
    html = _SCRIPT_STYLE_RE.sub(" ", html)
    text = _TAG_RE.sub(" ", html)
    text = _ENTITY_RE.sub(" ", text)
    text = _WS_RE.sub(" ", text)
    return text


def extract_exec_officers(text: str) -> int:
    """Return count of distinct executive officer names in the exec section.
    Crude but robust — counts 'Age XX' lines which is the canonical
    one-per-officer row in the S-K Item 401(b) listing.
    """
    text_l = text.lower()
    section_start = -1
    for h in EXEC_SECTION_HEADINGS:
        m = re.search(h, text_l)
        if m:
            section_start = m.end()
            break
    if section_start == -1:
        return 0
    section = text_l[section_start:section_start + 15000]
    ages = re.findall(r"\bage\s*[:\-]?\s*\d{2}\b", section)
    if not ages:
        ages = re.findall(r"\b(\d{2})\s+(?:years\s+old|mr\.|ms\.|mrs\.)", section)
    return len(ages)


def extract_rd_revenue(text: str) -> tuple[float, float]:
    text_l = text.lower().replace(",", "").replace("$", "")
    rd_m = re.search(
        r"research and development(?: expenses?| expenditures?)?[^0-9]{0,80}(\d+\.?\d*)\s*(million|billion)?",
        text_l,
    )
    rev_m = re.search(
        r"\b(?:total revenues?|net revenues?|revenues?)\b[^0-9]{0,80}(\d+\.?\d*)\s*(million|billion)?",
        text_l,
    )
    def _value(m):
        if not m:
            return float("nan")
        v = float(m.group(1))
        unit = m.group(2) or ""
        if "billion" in unit: v *= 1_000
        return v
    return _value(rd_m), _value(rev_m)


def keyword_freq(text: str) -> dict:
    text_l = text.lower()
    counts = {}
    for kw in TAU_KEYWORDS:
        counts[kw] = len(re.findall(r"\b" + re.escape(kw) + r"\b", text_l))
    return counts


def parse_one(path: str) -> dict:
    try:
        html = Path(path).read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        return {"error": str(e)}
    text = clean_text(html)
    words = len(text.split())
    n_exec = extract_exec_officers(text)
    rd, rev = extract_rd_revenue(text)
    kw = keyword_freq(text)
    total_kw = sum(kw.values())
    tau_raw = (total_kw / max(1, words)) * 10_000
    flat = 1.0 / (1.0 + max(0, n_exec))
    if n_exec == 0:
        flat = float("nan")
    K_rd = (rd / rev) if (rev and rev == rev and rev > 0 and rd == rd) else float("nan")
    if K_rd != K_rd:
        pass
    elif K_rd > 1.0:
        K_rd = float("nan")
    return {
        "doc_wordcount": words,
        "n_exec_officers": n_exec,
        "flat": flat,
        "tau_raw": tau_raw,
        "K_rd": K_rd,
        "rd_reported": rd,
        "rev_reported": rev,
        "keywords_total": total_kw,
    }


def main():
    idx = pd.read_csv(INDEX, dtype={"cik": str})
    print(f"Parsing {len(idx)} filings...", flush=True)
    rows = []
    ckpt_path = HERE / "_parse_checkpoint.csv"
    for i, r in idx.iterrows():
        try:
            parsed = parse_one(r["path"])
        except Exception as e:
            parsed = {"error": str(e)[:100]}
        rows.append({**r.to_dict(), **parsed})
        if (i + 1) % 25 == 0:
            print(f"  {i+1}/{len(idx)}", flush=True)
            pd.DataFrame(rows).to_csv(ckpt_path, index=False)
    out = pd.DataFrame(rows)
    out.to_csv(HERE / "firm_year_panel.csv", index=False)
    if ckpt_path.exists():
        ckpt_path.unlink()
    print(f"Wrote firm_year_panel.csv: {len(out)} rows", flush=True)
    keep = out.dropna(subset=["flat"])
    if len(keep) > 0:
        print(keep[["symbol", "year", "flat", "tau_raw", "K_rd", "n_exec_officers"]]
              .describe().round(3), flush=True)
    return out


if __name__ == "__main__":
    main()
