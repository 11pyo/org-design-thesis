"""
Run the moderation regression on REAL firm-year data from real_panel.csv.

Mirrors the structure of ../regression.py (which runs on synthetic data)
but adds: robust standard errors, industry x year FEs, firm FEs,
and a within-firm variation check.

Run: python regression_real.py
"""
from __future__ import annotations
from pathlib import Path
import pandas as pd
import numpy as np
import statsmodels.formula.api as smf

HERE = Path(__file__).parent
PANEL = HERE / "real_panel.csv"


def print_coef(mod, coef_name, test_name, expected_sign):
    if coef_name not in mod.params:
        print(f"  [{test_name}] coef {coef_name} not in model")
        return
    coef = mod.params[coef_name]
    pv = mod.pvalues[coef_name]
    se = mod.bse[coef_name]
    sign = "+" if coef >= 0 else "-"
    ok = "OK" if ((expected_sign == "+" and coef > 0) or (expected_sign == "-" and coef < 0)) else "  "
    print(f"  [{test_name}]  {coef_name:24s} = {coef:+.4f}  (se={se:.4f}, p={pv:.4g})  "
          f"expected {expected_sign}  {ok}")


def run_h1(df):
    sub = df[df["tau"] <= df["tau"].quantile(0.33)].copy()
    if len(sub) < 20:
        print("  [H1] sample too small"); return None
    m = smf.ols("ROA ~ flat + log_size + log_age + C(sector) + C(year)",
                data=sub).fit(cov_type="cluster",
                              cov_kwds={"groups": sub["firm_id"]})
    print_coef(m, "flat", f"H1 low-tau n={len(sub)}", "-")
    return m


def run_h2(df):
    sub = df[df["tau"] >= df["tau"].quantile(0.67)].copy()
    if len(sub) < 20:
        print("  [H2] sample too small"); return None
    m = smf.ols("ROA ~ flat + log_size + log_age + C(sector) + C(year)",
                data=sub).fit(cov_type="cluster",
                              cov_kwds={"groups": sub["firm_id"]})
    print_coef(m, "flat", f"H2 high-tau n={len(sub)}", "+")
    return m


def run_h3(df):
    d = df.copy()
    d["flat_x_tau"] = d["flat"] * d["tau"]
    m = smf.ols("ROA ~ flat + tau + flat_x_tau + log_size + log_age "
                "+ C(sector) + C(year)",
                data=d).fit(cov_type="cluster",
                            cov_kwds={"groups": d["firm_id"]})
    print_coef(m, "flat_x_tau", f"H3 moderation n={len(d)}", "+")
    return m


def run_h4(df):
    d = df.copy()
    d["K_c"] = d["K"] - d["K"].mean()
    d["flat_x_tau"] = d["flat"] * d["tau"]
    d["flat_x_K"] = d["flat"] * d["K_c"]
    d["tau_x_K"] = d["tau"] * d["K_c"]
    d["flat_x_tau_x_K"] = d["flat"] * d["tau"] * d["K_c"]
    m = smf.ols(
        "ROA ~ flat + tau + K_c + flat_x_tau + flat_x_K + tau_x_K "
        "+ flat_x_tau_x_K + log_size + log_age + C(sector) + C(year)",
        data=d,
    ).fit(cov_type="cluster", cov_kwds={"groups": d["firm_id"]})
    print_coef(m, "flat_x_tau_x_K", f"H4 triple n={len(d)}", "+")
    return m


def implied_tau_star(df):
    d = df.copy()
    d["K_c"] = d["K"] - d["K"].mean()
    d["flat_x_tau"] = d["flat"] * d["tau"]
    d["flat_x_K"] = d["flat"] * d["K_c"]
    d["flat_x_tau_x_K"] = d["flat"] * d["tau"] * d["K_c"]
    m = smf.ols(
        "ROA ~ flat + tau + K_c + flat_x_tau + flat_x_K + flat_x_tau_x_K "
        "+ log_size + log_age + C(sector) + C(year)",
        data=d).fit()
    b_flat = m.params["flat"]
    b_flat_tau = m.params["flat_x_tau"]
    b_flat_K = m.params["flat_x_K"]
    b_flat_tau_K = m.params["flat_x_tau_x_K"]

    print("\n[tau*] d(ROA)/d(flat) zero-crossing by K:")
    qs = np.quantile(d["K"], [0.25, 0.50, 0.75])
    for K in qs:
        K_c = K - d["K"].mean()
        num = -(b_flat + b_flat_K * K_c)
        den = b_flat_tau + b_flat_tau_K * K_c
        if abs(den) > 1e-9:
            t = num / den
            print(f"    K={K:.4f} -> tau* = {t:.3f}")


def main():
    if not PANEL.exists():
        print(f"Missing {PANEL}; run merge_panel.py first")
        return
    df = pd.read_csv(PANEL, dtype={"cik": str, "firm_id": str})
    print(f"Loaded real_panel.csv: {len(df)} firm-years, "
          f"{df['firm_id'].nunique()} firms")
    print("Variable summary:")
    print(df[["flat", "tau", "K", "ROA", "log_size", "log_age"]].describe().round(3))

    print("\n" + "=" * 70)
    print("Hypothesis tests on REAL data")
    print("=" * 70)
    m1 = run_h1(df)
    m2 = run_h2(df)
    m3 = run_h3(df)
    m4 = run_h4(df)
    implied_tau_star(df)

    summary = []
    for name, mod, coef in [
        ("H1", m1, "flat"), ("H2", m2, "flat"),
        ("H3", m3, "flat_x_tau"), ("H4", m4, "flat_x_tau_x_K"),
    ]:
        if mod is not None and coef in mod.params:
            summary.append({
                "test": name, "coef": coef,
                "estimate": float(mod.params[coef]),
                "se": float(mod.bse[coef]),
                "p": float(mod.pvalues[coef]),
                "n": int(mod.nobs),
            })
    out = pd.DataFrame(summary)
    out.to_csv(HERE / "regression_real_summary.csv", index=False)
    print(f"\nSaved regression_real_summary.csv")


if __name__ == "__main__":
    main()
