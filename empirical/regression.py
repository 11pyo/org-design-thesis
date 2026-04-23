"""
Moderation regression pipeline for H1-H4 on (synthetic) firm-year data.

Model:
    ROA = beta0 + b1*flat + b2*tau + b3*(flat*tau)
                 + b4*(flat*tau*K_centered) + controls + FE + eps

Expected if hypotheses hold:
    b3 > 0  (tau moderates flatness: higher tau -> flatness pays more)   --> H3
    b4 > 0  (effect of tau is amplified by complexity)                    --> H4
    At low tau subsample: b1 < 0                                          --> H1
    At high tau subsample: b1 > 0                                         --> H2

Run: python regression.py
Requires synthetic_firms.csv (from synthetic_data.py) or real data with the
same columns: firm_id, year, industry, log_size, log_age, flat, tau, K, ROA.
"""

from __future__ import annotations
import os
import pandas as pd
import numpy as np
import statsmodels.formula.api as smf

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "synthetic_firms.csv")


def ensure_data():
    if not os.path.exists(DATA):
        print("No synthetic_firms.csv found -- generating via synthetic_data.py")
        import synthetic_data
        synthetic_data.generate(DATA)


def run_h1(df: pd.DataFrame):
    sub = df[df["tau"] <= df["tau"].quantile(0.25)].copy()
    m = smf.ols("ROA ~ flat + log_size + log_age + C(industry) + C(year)",
                data=sub).fit(cov_type="cluster", cov_kwds={"groups": sub["firm_id"]})
    coef = m.params["flat"]
    pv = m.pvalues["flat"]
    print(f"\n[H1] Low-tau subsample (n={len(sub)}): "
          f"flat coef = {coef:+.4f}  p = {pv:.4g}")
    print("     H1 prediction: coef < 0 (vertical > horizontal when info scarce)")
    return m


def run_h2(df: pd.DataFrame):
    sub = df[df["tau"] >= df["tau"].quantile(0.75)].copy()
    m = smf.ols("ROA ~ flat + log_size + log_age + C(industry) + C(year)",
                data=sub).fit(cov_type="cluster", cov_kwds={"groups": sub["firm_id"]})
    coef = m.params["flat"]
    pv = m.pvalues["flat"]
    print(f"\n[H2] High-tau subsample (n={len(sub)}): "
          f"flat coef = {coef:+.4f}  p = {pv:.4g}")
    print("     H2 prediction: coef > 0 (horizontal > vertical when info abundant)")
    return m


def run_h3_moderation(df: pd.DataFrame):
    d = df.copy()
    d["flat_x_tau"] = d["flat"] * d["tau"]
    m = smf.ols(
        "ROA ~ flat + tau + flat_x_tau + log_size + log_age + C(industry) + C(year)",
        data=d,
    ).fit(cov_type="cluster", cov_kwds={"groups": d["firm_id"]})
    coef = m.params["flat_x_tau"]
    pv = m.pvalues["flat_x_tau"]
    print(f"\n[H3] Full sample (n={len(d)}): "
          f"flat x tau coef = {coef:+.4f}  p = {pv:.4g}")
    print("     H3 prediction: coef > 0 (threshold/crossover exists)")
    return m


def run_h4_three_way(df: pd.DataFrame):
    d = df.copy()
    d["K_c"] = d["K"] - d["K"].mean()
    d["flat_x_tau"] = d["flat"] * d["tau"]
    d["flat_x_K"] = d["flat"] * d["K_c"]
    d["tau_x_K"] = d["tau"] * d["K_c"]
    d["flat_x_tau_x_K"] = d["flat"] * d["tau"] * d["K_c"]
    m = smf.ols(
        "ROA ~ flat + tau + K_c + flat_x_tau + flat_x_K + tau_x_K "
        "+ flat_x_tau_x_K + log_size + log_age + C(industry) + C(year)",
        data=d,
    ).fit(cov_type="cluster", cov_kwds={"groups": d["firm_id"]})
    coef = m.params["flat_x_tau_x_K"]
    pv = m.pvalues["flat_x_tau_x_K"]
    print(f"\n[H4] Triple interaction (n={len(d)}): "
          f"flat x tau x K coef = {coef:+.4f}  p = {pv:.4g}")
    print("     H4 prediction: coef > 0 (more complex tasks lower tau* bar)")
    return m


def estimate_tau_star(df: pd.DataFrame):
    d = df.copy()
    d["K_c"] = d["K"] - d["K"].mean()
    d["flat_x_tau"] = d["flat"] * d["tau"]
    d["flat_x_K"] = d["flat"] * d["K_c"]
    d["flat_x_tau_x_K"] = d["flat"] * d["tau"] * d["K_c"]
    m = smf.ols(
        "ROA ~ flat + tau + K_c + flat_x_tau + flat_x_K + flat_x_tau_x_K "
        "+ log_size + log_age + C(industry) + C(year)",
        data=d,
    ).fit()
    b_flat = m.params["flat"]
    b_flat_tau = m.params["flat_x_tau"]
    b_flat_K = m.params["flat_x_K"]
    b_flat_tau_K = m.params["flat_x_tau_x_K"]

    print("\n[tau*] Implied tau*(K) where d(ROA)/d(flat) = 0")
    print(f"  d(ROA)/d(flat) = {b_flat:+.3f} + {b_flat_tau:+.3f}*tau "
          f"+ {b_flat_K:+.3f}*K_c + {b_flat_tau_K:+.3f}*tau*K_c")
    for K in [3.0, 6.0, 9.0]:
        K_c = K - d["K"].mean()
        num = -(b_flat + b_flat_K * K_c)
        den = b_flat_tau + b_flat_tau_K * K_c
        if abs(den) > 1e-9:
            t = num / den
            print(f"    K = {K:.1f} -> tau* = {t:.3f}")
        else:
            print(f"    K = {K:.1f} -> no crossover (den=0)")


def main():
    ensure_data()
    df = pd.read_csv(DATA)
    print(f"Loaded {len(df)} firm-year observations.")
    print(f"  N firms: {df['firm_id'].nunique()}, "
          f"years: {df['year'].min()}-{df['year'].max()}")

    m1 = run_h1(df)
    m2 = run_h2(df)
    m3 = run_h3_moderation(df)
    m4 = run_h4_three_way(df)

    estimate_tau_star(df)

    print("\n" + "=" * 60)
    print("Summary table (key coefficients only)")
    print("=" * 60)
    rows = []
    for name, mod, coef_name in [
        ("H1 low-tau", m1, "flat"),
        ("H2 high-tau", m2, "flat"),
        ("H3 moderation", m3, "flat_x_tau"),
        ("H4 triple", m4, "flat_x_tau_x_K"),
    ]:
        rows.append({
            "test": name, "coef_name": coef_name,
            "coef": mod.params[coef_name],
            "se": mod.bse[coef_name],
            "p": mod.pvalues[coef_name],
            "n": int(mod.nobs),
        })
    print(pd.DataFrame(rows).to_string(index=False,
          formatters={"coef": "{:+.4f}".format,
                      "se": "{:.4f}".format,
                      "p": "{:.4g}".format}))

    out_json = os.path.join(HERE, "regression_summary.csv")
    pd.DataFrame(rows).to_csv(out_json, index=False)
    print(f"\nWrote {out_json}")


if __name__ == "__main__":
    main()
