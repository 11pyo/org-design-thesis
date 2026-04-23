"""
Merge parsed 10-K data and yfinance financial data into a single
firm-year panel ready for regression.

Input:
  - firm_year_panel.csv  (from parse_10k.py)  — flat, tau_raw, K_rd
  - yf_firm_year.csv     (from fetch_yfinance.py) — ROA, employees, etc.
  - sp500_list.csv       (Wikipedia) — founded year, sector

Output:
  - real_panel.csv  ready for regression.py

Transformations:
- tau_raw standardized to [0,1] within year (cross-sectional percentile)
- K_rd Winsorized at 99th percentile
- log_size = log(employees) or log(total_assets) fallback
- log_age = log(current_year - founded)
- firm_id = CIK

QC: drop rows where any of (flat, tau, K, ROA) is missing.
"""
from __future__ import annotations
import re
from pathlib import Path
import pandas as pd
import numpy as np

HERE = Path(__file__).parent


def _founded_to_year(x) -> int | None:
    if pd.isna(x): return None
    s = str(x)
    m = re.search(r"\b(1[89]\d{2}|20\d{2})\b", s)
    return int(m.group(1)) if m else None


def main():
    p10k = pd.read_csv(HERE / "firm_year_panel.csv", dtype={"cik": str})
    yf_df = pd.read_csv(HERE / "yf_firm_year.csv", dtype={"cik": str})
    sp = pd.read_csv(HERE / "sp500_list.csv")

    sp["founded_year"] = sp["Founded"].apply(_founded_to_year)
    sp["cik"] = sp["CIK"].astype(str).str.zfill(10)
    sp_small = sp[["cik", "Symbol", "GICS Sector", "GICS Sub-Industry", "founded_year"]].rename(
        columns={"Symbol": "symbol", "GICS Sector": "sector", "GICS Sub-Industry": "sub_industry"})

    p10k["year"] = p10k["year"].astype(int)
    yf_df["year"] = pd.to_numeric(yf_df["year"], errors="coerce")
    yf_df = yf_df.dropna(subset=["year"])
    yf_df["year"] = yf_df["year"].astype(int)

    merged = p10k.merge(
        yf_df[["cik", "year", "net_income", "total_assets", "ROA",
               "employees", "market_cap"]],
        on=["cik", "year"], how="left")
    merged = merged.merge(sp_small, on="cik", how="left", suffixes=("", "_sp"))

    if "symbol" not in merged.columns and "symbol_sp" in merged.columns:
        merged["symbol"] = merged["symbol_sp"]

    for col in ("flat", "tau_raw", "K_rd", "ROA"):
        merged[col] = pd.to_numeric(merged[col], errors="coerce")

    def winsorize(s, lower=0.01, upper=0.99):
        if s.notna().sum() < 10: return s
        lo, hi = s.quantile(lower), s.quantile(upper)
        return s.clip(lower=lo, upper=hi)

    merged["K_rd_w"] = winsorize(merged["K_rd"])
    merged["ROA_w"] = winsorize(merged["ROA"])

    merged["tau_norm"] = (
        merged.groupby("year")["tau_raw"]
        .transform(lambda x: x.rank(pct=True))
    )

    merged["log_size"] = np.log(
        pd.to_numeric(merged["employees"], errors="coerce")
        .fillna(
            pd.to_numeric(merged["total_assets"], errors="coerce")
        )
        .replace(0, np.nan)
    )
    merged["log_age"] = np.log(
        (merged["year"] - merged["founded_year"]).clip(lower=1)
    )

    merged["K_rd_w"] = merged["K_rd_w"].fillna(merged["K_rd_w"].median())

    keep = merged.dropna(subset=["flat", "tau_norm", "ROA_w"]).copy()
    keep["firm_id"] = keep["cik"]

    keep = keep.rename(columns={"K_rd_w": "K", "tau_norm": "tau", "ROA_w": "ROA"})

    cols = ["firm_id", "cik", "symbol", "year", "sector", "sub_industry",
            "flat", "tau", "K", "ROA",
            "log_size", "log_age",
            "n_exec_officers", "doc_wordcount", "keywords_total",
            "employees", "total_assets", "market_cap", "founded_year"]
    cols = [c for c in cols if c in keep.columns]
    out = keep[cols].copy()

    out.to_csv(HERE / "real_panel.csv", index=False)
    print(f"real_panel.csv: {len(out)} firm-years, "
          f"{out['firm_id'].nunique()} firms, "
          f"years {out['year'].min()}-{out['year'].max()}")
    print("\nSummary:")
    print(out[["flat", "tau", "K", "ROA", "log_size", "log_age"]]
          .describe().round(3))
    print("\nSector counts:")
    print(out["sector"].value_counts())
    return out


if __name__ == "__main__":
    main()
