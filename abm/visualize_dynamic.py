"""
Generate figures for the dynamic-landscape extension.

Writes to ../results/figures/fig_*_dynamic.png
"""
from __future__ import annotations
import os, sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

sns.set_theme(style="whitegrid", context="paper")
plt.rcParams["figure.dpi"] = 140
plt.rcParams["savefig.dpi"] = 200

RESULTS = os.path.normpath(os.path.join(HERE, "..", "results"))
FIG = os.path.join(RESULTS, "figures")

STRUCT_COLORS = {"V": "#d62728", "H": "#2ca02c", "Hy": "#1f77b4"}
STRUCT_LABELS = {"V": "Vertical", "H": "Horizontal", "Hy": "Hybrid"}


def main():
    df = pd.read_csv(os.path.join(RESULTS, "results_dynamic.csv"))
    g = df.groupby(["K", "tau", "structure"])["final_fitness"].agg(["mean", "sem"]).reset_index()

    fig, axes = plt.subplots(1, 3, figsize=(13, 4), sharey=True)
    for ax, K in zip(axes, sorted(df["K"].unique())):
        sub = g[g["K"] == K]
        for s in ["V", "H", "Hy"]:
            s_sub = sub[sub["structure"] == s].sort_values("tau")
            ax.errorbar(s_sub["tau"], s_sub["mean"], yerr=1.96 * s_sub["sem"],
                        label=STRUCT_LABELS[s], color=STRUCT_COLORS[s],
                        marker="o", lw=2, capsize=3)
        ax.set_title(f"K = {K}")
        ax.set_xlabel(r"$\tau$")
        if K == sorted(df["K"].unique())[0]:
            ax.set_ylabel("Final firm fitness (mean ± 95% CI)")
    axes[0].legend(loc="lower right", frameon=True)
    fig.suptitle("Dynamic landscape (shock every 10 steps, 25% reshuffle)", y=1.02)
    fig.tight_layout()
    out = os.path.join(FIG, "fig_perf_curves_dynamic.png")
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    print("  wrote", out)

    piv = (df.groupby(["K", "tau", "structure"])["final_fitness"]
           .mean().unstack("structure"))
    piv["H_minus_V"] = piv["H"] - piv["V"]
    piv["Hy_minus_V"] = piv["Hy"] - piv["V"]
    piv["Hy_minus_H"] = piv["Hy"] - piv["H"]

    fig, ax = plt.subplots(figsize=(8, 4.5))
    colors_K = {2: "#1f77b4", 5: "#ff7f0e", 10: "#2ca02c"}
    for K in sorted(piv.index.get_level_values("K").unique()):
        sub = piv.xs(K).reset_index().sort_values("tau")
        ax.plot(sub["tau"], sub["Hy_minus_V"], "o-", color=colors_K[K],
                label=f"Hybrid − V, K = {K}", lw=2)
    ax.axhline(0, color="black", lw=0.8, alpha=0.5)
    ax.set_xlabel(r"$\tau$")
    ax.set_ylabel(r"$\pi_{Hy} - \pi_V$")
    ax.set_title("Hybrid's advantage over Vertical on dynamic landscapes")
    ax.legend(frameon=True, fontsize=9)
    fig.tight_layout()
    out = os.path.join(FIG, "fig_hybrid_dominance_dynamic.png")
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    print("  wrote", out)


if __name__ == "__main__":
    main()
