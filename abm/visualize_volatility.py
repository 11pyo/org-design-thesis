"""
Visualize the volatility-gradient experiment.

Headline figure: V-minus-H fitness gap vs environmental volatility.
Static-regime: H > V at high tau (negative gap). Dynamic-regime: V > H
uniformly (positive gap). The crossover is the main result.

Writes:
 - fig_VH_gap_by_volatility.png  (main finding)
 - fig_vol_by_tau.png            (by-tau detail)
 - fig_structure_fitness_vol.png (all three structures by volatility)
"""
from __future__ import annotations
import os, sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid", context="paper")
plt.rcParams["figure.dpi"] = 140
plt.rcParams["savefig.dpi"] = 200

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.normpath(os.path.join(HERE, "..", "results"))
FIG = os.path.join(RESULTS, "figures")

STRUCT_COLORS = {"V": "#d62728", "H": "#2ca02c", "Hy": "#1f77b4"}


def main():
    df = pd.read_csv(os.path.join(RESULTS, "results_volatility.csv"))

    g = (df.groupby(["shock_every", "K", "tau", "structure"])["final_fitness"]
         .mean().unstack("structure").reset_index())
    g["V_minus_H"] = g["V"] - g["H"]
    g["volatility"] = 1.0 / g["shock_every"]

    summary = (g.groupby("shock_every")["V_minus_H"]
               .agg(["mean", "std", "count"]).reset_index())
    summary["sem"] = summary["std"] / np.sqrt(summary["count"])
    summary["volatility"] = 1.0 / summary["shock_every"]
    summary = summary.sort_values("volatility")

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.errorbar(summary["volatility"], summary["mean"],
                yerr=1.96 * summary["sem"],
                marker="o", markersize=10, lw=2.5, capsize=5,
                color="#c0392b", label="V - H (main)")
    ax.axhline(0, color="black", lw=0.8, alpha=0.6)
    for _, r in summary.iterrows():
        ax.annotate(f"shock/{int(r['shock_every'])}",
                    xy=(r["volatility"], r["mean"]),
                    xytext=(10, -6), textcoords="offset points",
                    fontsize=9, alpha=0.8)
    ax.set_xlabel("Environmental volatility (shocks per step)")
    ax.set_ylabel(r"$\pi_V - \pi_H$  (positive = Vertical wins)")
    ax.set_title("Volatility reverses the Horizontal advantage")
    ax.set_xscale("log")
    ax.legend()
    fig.tight_layout()
    out = os.path.join(FIG, "fig_VH_gap_by_volatility.png")
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    print("  wrote", out)

    fig, axes = plt.subplots(1, 3, figsize=(13, 4), sharey=True)
    for ax, K in zip(axes, sorted(g["K"].unique())):
        sub = g[g["K"] == K]
        for tau, c in zip(sorted(sub["tau"].unique()),
                          ["#1f77b4", "#ff7f0e", "#2ca02c"]):
            s = sub[sub["tau"] == tau].sort_values("shock_every")
            s = s.assign(vol=1.0 / s["shock_every"])
            agg = s.groupby("vol")["V_minus_H"].mean().reset_index()
            ax.plot(agg["vol"], agg["V_minus_H"], "o-", lw=2,
                    label=rf"$\tau$ = {tau}", color=c)
        ax.axhline(0, color="black", lw=0.6, alpha=0.4)
        ax.set_xscale("log")
        ax.set_xlabel("Volatility")
        ax.set_title(f"K = {K}")
        if K == sorted(g["K"].unique())[0]:
            ax.set_ylabel(r"$\pi_V - \pi_H$")
    axes[0].legend(frameon=True, loc="lower right")
    fig.suptitle(r"V $-$ H gap vs volatility, by K and $\tau$", y=1.02)
    fig.tight_layout()
    out = os.path.join(FIG, "fig_vol_by_tau.png")
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    print("  wrote", out)

    by_struct = (df.groupby(["shock_every", "structure"])["final_fitness"]
                 .agg(["mean", "std", "count"]).reset_index())
    by_struct["sem"] = by_struct["std"] / np.sqrt(by_struct["count"])
    by_struct["volatility"] = 1.0 / by_struct["shock_every"]

    fig, ax = plt.subplots(figsize=(8, 5))
    for s in ["V", "H", "Hy"]:
        sub = by_struct[by_struct["structure"] == s].sort_values("volatility")
        ax.errorbar(sub["volatility"], sub["mean"], yerr=1.96 * sub["sem"],
                    marker="o", markersize=8, lw=2, capsize=4,
                    color=STRUCT_COLORS[s],
                    label={"V": "Vertical", "H": "Horizontal", "Hy": "Hybrid"}[s])
    ax.set_xscale("log")
    ax.set_xlabel("Environmental volatility (shocks per step)")
    ax.set_ylabel("Mean terminal fitness (averaged over τ, K)")
    ax.set_title("How each structure adapts to environmental volatility")
    ax.legend()
    fig.tight_layout()
    out = os.path.join(FIG, "fig_structure_fitness_vol.png")
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    print("  wrote", out)

    print("\nVolatility summary (V - H):")
    print(summary[["shock_every", "volatility", "mean", "sem"]].round(4).to_string(index=False))
    spearman = summary[["volatility", "mean"]].corr(method="spearman").iloc[0, 1]
    print(f"\nSpearman rho(volatility, V_minus_H) = {spearman:+.3f}")


if __name__ == "__main__":
    main()
