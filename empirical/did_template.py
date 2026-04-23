"""
Difference-in-Differences template for firms that flattened after an
exogenous event. Requires a real treatment table listing (firm_id, treat_year).

On synthetic data we simulate a treatment by designating firms whose flatness
crossed a threshold in a given year as "treated" and the rest as controls.

Run: python did_template.py
"""

from __future__ import annotations
import os
import pandas as pd
import numpy as np
import statsmodels.formula.api as smf

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "synthetic_firms.csv")


def build_treatment_table(df: pd.DataFrame, flatness_jump: float = 0.15) -> pd.DataFrame:
    dfs = df.sort_values(["firm_id", "year"]).copy()
    dfs["flat_prev"] = dfs.groupby("firm_id")["flat"].shift(1)
    dfs["jump"] = dfs["flat"] - dfs["flat_prev"]
    jumps = (dfs[dfs["jump"] >= flatness_jump]
             .sort_values(["firm_id", "year"])
             .drop_duplicates(subset=["firm_id"]))
    treat_tbl = jumps[["firm_id", "year"]].rename(columns={"year": "treat_year"})
    print(f"Identified {len(treat_tbl)} synthetically-treated firms "
          f"(flatness jump >= {flatness_jump}).")
    return treat_tbl


def run_did(df: pd.DataFrame, treat_tbl: pd.DataFrame):
    df = df.merge(treat_tbl, on="firm_id", how="left")
    df["treated_ever"] = df["treat_year"].notna().astype(int)
    df["post"] = ((df["year"] >= df["treat_year"]) & df["treated_ever"].astype(bool)).astype(int)
    df["did"] = df["treated_ever"] * df["post"]

    m = smf.ols(
        "ROA ~ did + treated_ever + post + log_size + log_age + C(industry) + C(year) + C(firm_id)",
        data=df,
    ).fit(cov_type="cluster", cov_kwds={"groups": df["firm_id"]})

    coef = m.params["did"]
    pv = m.pvalues["did"]
    print(f"\n[DiD] Post-flattening ROA delta: {coef:+.4f}  p = {pv:.4g}")
    print("     (flattening effect, averaged across tau levels)")

    hi = df[df["tau"] >= df["tau"].quantile(0.66)]
    lo = df[df["tau"] <= df["tau"].quantile(0.33)]

    if len(hi) > 100 and hi["did"].sum() > 0:
        m_hi = smf.ols(
            "ROA ~ did + treated_ever + post + log_size + log_age + C(industry) + C(year) + C(firm_id)",
            data=hi,
        ).fit(cov_type="cluster", cov_kwds={"groups": hi["firm_id"]})
        print(f"[DiD|hi-tau] coef = {m_hi.params['did']:+.4f}  p = {m_hi.pvalues['did']:.4g}")

    if len(lo) > 100 and lo["did"].sum() > 0:
        m_lo = smf.ols(
            "ROA ~ did + treated_ever + post + log_size + log_age + C(industry) + C(year) + C(firm_id)",
            data=lo,
        ).fit(cov_type="cluster", cov_kwds={"groups": lo["firm_id"]})
        print(f"[DiD|lo-tau] coef = {m_lo.params['did']:+.4f}  p = {m_lo.pvalues['did']:.4g}")
        print("     Expected: hi-tau DiD > lo-tau DiD (conditional flattening payoff)")

    return m


def main():
    if not os.path.exists(DATA):
        print("Missing synthetic_firms.csv -- run synthetic_data.py first.")
        return
    df = pd.read_csv(DATA)
    treat_tbl = build_treatment_table(df)
    run_did(df, treat_tbl)


if __name__ == "__main__":
    main()
