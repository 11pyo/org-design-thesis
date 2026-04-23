"""
Bootstrap confidence intervals + permutation tests for the headline
H5 dose-response (resolves Critique 1 statistically).

Reads:
  - results_volatility.csv  (baseline 6-level grid)
  - results_densegrid.csv   (dense grid with 3 seed banks, once available)

Reports:
  1. V-H gap at each shock-frequency level with bootstrap 95% CI.
  2. Linear regression of V-H on log(volatility) with bootstrap CI on slope.
  3. Permutation test for monotonicity (is Spearman rho = +1.00 chance?).
  4. Cross-seed-bank replication on the dense grid.

Writes:
  - results/bootstrap_summary.json
  - results/figures/fig_bootstrap_CI.png
"""
from __future__ import annotations
import os, json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

sns.set_theme(style="whitegrid", context="paper")
plt.rcParams["figure.dpi"] = 140

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.normpath(os.path.join(HERE, "..", "results"))
FIG = os.path.join(RESULTS, "figures")

N_BOOT = 2000
RNG = np.random.default_rng(2026)


def bootstrap_mean_diff(df: pd.DataFrame, group_col: str, g1: str, g2: str,
                        value_col: str, n_boot: int = N_BOOT, rng=None):
    """Bootstrap CI for mean(g1) - mean(g2) stratified by seed (cluster bootstrap)."""
    rng = rng or RNG
    a = df[df[group_col] == g1][value_col].values
    b = df[df[group_col] == g2][value_col].values
    if len(a) == 0 or len(b) == 0:
        return np.nan, (np.nan, np.nan)
    diffs = np.empty(n_boot)
    for i in range(n_boot):
        aa = rng.choice(a, size=len(a), replace=True)
        bb = rng.choice(b, size=len(b), replace=True)
        diffs[i] = aa.mean() - bb.mean()
    return a.mean() - b.mean(), np.percentile(diffs, [2.5, 97.5])


def per_level_ci(df: pd.DataFrame):
    out = []
    for se, sub in df.groupby("shock_every"):
        mean, (lo, hi) = bootstrap_mean_diff(sub, "structure", "V", "H", "final_fitness")
        out.append({"shock_every": int(se), "volatility": 1.0 / se,
                    "V_minus_H": mean, "ci_lo": lo, "ci_hi": hi,
                    "n_V": int((sub["structure"] == "V").sum()),
                    "n_H": int((sub["structure"] == "H").sum())})
    return pd.DataFrame(out).sort_values("volatility")


def slope_with_bootstrap(summary: pd.DataFrame, df_raw: pd.DataFrame, n_boot=N_BOOT):
    """Regress V-H on log(vol). Bootstrap by resampling seeds within each cell.
    IMPORTANT: x and ys_b must be in the same shock_every order.
    """
    summary_sorted = summary.sort_values("shock_every", ascending=False)
    shock_levels = list(summary_sorted["shock_every"].values)
    x = np.log(1.0 / np.array(shock_levels, dtype=float))
    y = summary_sorted["V_minus_H"].values
    beta_obs, alpha_obs = np.polyfit(x, y, 1)
    betas = np.empty(n_boot)
    for b in range(n_boot):
        ys_b = []
        for se in shock_levels:
            sub = df_raw[df_raw["shock_every"] == se]
            V = sub[sub["structure"] == "V"]["final_fitness"].values
            H = sub[sub["structure"] == "H"]["final_fitness"].values
            V_b = RNG.choice(V, size=len(V), replace=True)
            H_b = RNG.choice(H, size=len(H), replace=True)
            ys_b.append(V_b.mean() - H_b.mean())
        betas[b] = np.polyfit(x, np.array(ys_b), 1)[0]
    lo, hi = np.percentile(betas, [2.5, 97.5])
    return {"slope": float(beta_obs), "intercept": float(alpha_obs),
            "ci_lo": float(lo), "ci_hi": float(hi)}


def spearman_permutation(summary: pd.DataFrame, n_perm: int = 100_000):
    x = summary["volatility"].values
    y = summary["V_minus_H"].values
    rho_obs, _ = stats.spearmanr(x, y)
    perm_rhos = np.empty(n_perm)
    rng = np.random.default_rng(2027)
    for i in range(n_perm):
        perm = rng.permutation(y)
        perm_rhos[i], _ = stats.spearmanr(x, perm)
    p_one_sided = float((perm_rhos >= rho_obs).mean())
    p_two_sided = float((np.abs(perm_rhos) >= abs(rho_obs)).mean())
    return {"rho": float(rho_obs), "p_one_sided": p_one_sided, "p_two_sided": p_two_sided,
            "n_perm": n_perm, "n_points": len(x)}


def plot_ci(summary: pd.DataFrame, title: str, out: str):
    fig, ax = plt.subplots(figsize=(8, 5))
    summary = summary.sort_values("volatility")
    ax.errorbar(summary["volatility"], summary["V_minus_H"],
                yerr=[summary["V_minus_H"] - summary["ci_lo"],
                      summary["ci_hi"] - summary["V_minus_H"]],
                marker="o", markersize=10, lw=2.5, capsize=5, color="#c0392b")
    ax.axhline(0, color="black", lw=0.8, alpha=0.5)
    ax.set_xscale("log")
    ax.set_xlabel("Environmental volatility (shocks per step)")
    ax.set_ylabel(r"$\pi_V - \pi_H$  (95% bootstrap CI)")
    ax.set_title(title)
    fig.tight_layout()
    fig.savefig(out, bbox_inches="tight", dpi=200)
    plt.close(fig)
    print(f"  wrote {out}")


def main():
    out = {}

    vol_path = os.path.join(RESULTS, "results_volatility.csv")
    if os.path.exists(vol_path):
        df = pd.read_csv(vol_path)
        summary = per_level_ci(df)
        print("=== volatility baseline ===")
        print(summary.round(4).to_string(index=False))
        slope = slope_with_bootstrap(summary, df)
        print(f"Slope: {slope['slope']:+.3f}  95% CI [{slope['ci_lo']:+.3f}, {slope['ci_hi']:+.3f}]")
        perm = spearman_permutation(summary)
        print(f"Spearman rho = {perm['rho']:+.3f}, one-sided perm p = {perm['p_one_sided']:.4g}, "
              f"two-sided p = {perm['p_two_sided']:.4g}")
        out["volatility_baseline"] = {"summary": summary.to_dict(orient="records"),
                                      "slope": slope, "spearman_perm": perm}
        plot_ci(summary, "V - H gap with 95% bootstrap CI (baseline, 6 levels)",
                os.path.join(FIG, "fig_bootstrap_CI_baseline.png"))

    dg_path = os.path.join(RESULTS, "results_densegrid.csv")
    if os.path.exists(dg_path):
        df = pd.read_csv(dg_path)
        print("\n=== dense grid, 3 seed banks ===")
        out["densegrid_by_bank"] = {}
        for bank in sorted(df["bank"].unique()):
            sub = df[df["bank"] == bank]
            summary_b = per_level_ci(sub)
            slope_b = slope_with_bootstrap(summary_b, sub)
            perm_b = spearman_permutation(summary_b)
            print(f"Bank {bank}: "
                  f"slope = {slope_b['slope']:+.3f} "
                  f"[{slope_b['ci_lo']:+.3f}, {slope_b['ci_hi']:+.3f}]  "
                  f"rho = {perm_b['rho']:+.3f}  p = {perm_b['p_one_sided']:.4g}")
            out["densegrid_by_bank"][bank] = {
                "slope": slope_b, "spearman_perm": perm_b,
                "summary": summary_b.to_dict(orient="records"),
            }

        summary_all = per_level_ci(df)
        plot_ci(summary_all, "V - H gap with 95% bootstrap CI (dense grid, 15 levels)",
                os.path.join(FIG, "fig_bootstrap_CI_dense.png"))

    with open(os.path.join(RESULTS, "bootstrap_summary.json"), "w") as f:
        json.dump(out, f, indent=2, default=str)
    print("\nWrote bootstrap_summary.json")


if __name__ == "__main__":
    main()
